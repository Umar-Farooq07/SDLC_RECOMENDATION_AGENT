"""Local retrieval with citations, preferring Chroma and falling back to lexical search."""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from config import CHROMA_PATH, KB_PATH
from rag.ingest_kb import HashEmbeddingFunction, chunk_markdown


@dataclass
class CitationChunk:
    text: str
    metadata: dict[str, Any]
    score: float


class KnowledgeBaseRetriever:
    def __init__(self, kb_path: str | Path = KB_PATH, persist_path: str | Path = CHROMA_PATH) -> None:
        self.kb_path = Path(kb_path)
        self.persist_path = Path(persist_path)

    def _all_chunks(self) -> list[dict[str, Any]]:
        chunks: list[dict[str, Any]] = []
        for path in sorted(self.kb_path.glob("*.md")):
            chunks += chunk_markdown(path.read_text(encoding="utf-8"), path.name)
        return chunks

    def retrieve(self, query: str, k: int = 4, document_filter: str | None = None) -> list[CitationChunk]:
        try:
            import chromadb
        except ImportError:
            chromadb = None
        if chromadb is not None and self.persist_path.exists():
            client = chromadb.PersistentClient(path=str(self.persist_path))
            names = [item.name if hasattr(item, "name") else item for item in client.list_collections()]
            if "financial_requirements_kb" in names:
                collection = client.get_collection("financial_requirements_kb", embedding_function=None)
                where = {"source": document_filter} if document_filter else None
                results = collection.query(
                    query_embeddings=HashEmbeddingFunction()([query]),
                    n_results=max(k * 3, k), where=where,
                )
                query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
                scored = []
                for text, metadata, distance in zip(
                    results["documents"][0], results["metadatas"][0], results["distances"][0]
                ):
                    terms = set(re.findall(r"[a-z0-9]+", text.lower()))
                    lexical = len(query_terms & terms) / max(len(query_terms), 1)
                    semantic = max(0.0, 1.0 - float(distance) / 2.0)
                    scored.append(CitationChunk(text, metadata, 0.65 * semantic + 0.35 * lexical))
                return sorted(scored, key=lambda match: match.score, reverse=True)[:k]
        query_terms = set(re.findall(r"[a-z0-9]+", query.lower()))
        ranked: list[tuple[int, dict[str, Any]]] = []
        for item in self._all_chunks():
            if document_filter and item["metadata"]["source"] != document_filter:
                continue
            terms = set(re.findall(r"[a-z0-9]+", item["text"].lower()))
            ranked.append((len(query_terms & terms), item))
        ranked.sort(key=lambda pair: pair[0], reverse=True)
        return [
            CitationChunk(item["text"], item["metadata"], score / max(len(query_terms), 1))
            for score, item in ranked[:k] if score > 0
        ]
