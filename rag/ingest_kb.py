"""Ingest Markdown knowledge documents into a local Chroma collection."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from config import CHROMA_PATH, KB_PATH


class HashEmbeddingFunction:
    """Small deterministic local embedding; avoids external model downloads."""
    def __call__(self, input: list[str]) -> list[list[float]]:
        return self.embed_documents(input)

    def embed_documents(self, input: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in input]

    def embed_query(self, input: list[str]) -> list[list[float]]:
        return self(input)

    def is_legacy(self) -> bool:
        return False

    @staticmethod
    def _embed(text: str) -> list[float]:
        import hashlib
        vector = [0.0] * 96
        for token in re.findall(r"[a-z0-9]+", text.lower()):
            digest = hashlib.sha256(token.encode()).digest()
            index = int.from_bytes(digest[:2], "big") % len(vector)
            vector[index] += 1.0 if digest[2] % 2 else -1.0
        norm = sum(value * value for value in vector) ** 0.5 or 1.0
        return [value / norm for value in vector]

    def name(self) -> str:
        return "fin-req-hash-embedding-v1"

    def get_config(self) -> dict[str, Any]:
        return {}

    def default_space(self) -> str:
        return "cosine"

    def supported_spaces(self) -> list[str]:
        return ["cosine", "l2", "ip"]

    @staticmethod
    def build_from_config(config: dict[str, Any]) -> "HashEmbeddingFunction":
        return HashEmbeddingFunction()


def chunk_markdown(text: str, source: str, chunk_size: int = 900) -> list[dict[str, Any]]:
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else source
    section = "General"
    chunks: list[dict[str, Any]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                chunks.extend(_split_block("\n".join(current), title, section, source, chunk_size))
                current = []
            section = line[3:].strip()
        current.append(line)
    if current:
        chunks.extend(_split_block("\n".join(current), title, section, source, chunk_size))
    return chunks


def _split_block(block: str, title: str, section: str, source: str, size: int) -> list[dict[str, Any]]:
    sentences = re.split(r"(?<=[.!?])\s+", block.strip())
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) > size and current:
            parts.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        parts.append(current)
    return [
        {"text": part, "metadata": {
            "title": title, "section": section, "source": source, "jurisdiction": "India",
            "version": "2025", "effective_date": "2025-01-01",
        }}
        for part in parts if part
    ]


def ingest_documents(kb_path: str | Path = KB_PATH, persist_path: str | Path = CHROMA_PATH) -> int:
    documents: list[dict[str, Any]] = []
    for path in sorted(Path(kb_path).glob("*.md")):
        documents.extend(chunk_markdown(path.read_text(encoding="utf-8"), path.name))
    if not documents:
        raise FileNotFoundError(f"No Markdown knowledge documents found in {kb_path}")
    try:
        import chromadb
    except ImportError:
        # The retriever can use the same source documents directly when Chroma is unavailable.
        return len(documents)
    client = chromadb.PersistentClient(path=str(persist_path))
    collection = client.get_or_create_collection(
        "financial_requirements_kb", metadata={"hnsw:space": "cosine"}, embedding_function=None
    )
    existing = collection.get()
    if existing.get("ids"):
        collection.delete(ids=existing["ids"])
    collection.add(
        ids=[f"{item['metadata']['source']}::{index}" for index, item in enumerate(documents)],
        documents=[item["text"] for item in documents],
        metadatas=[item["metadata"] for item in documents],
        embeddings=HashEmbeddingFunction()([item["text"] for item in documents]),
    )
    return len(documents)


if __name__ == "__main__":
    print(f"Ingested {ingest_documents()} knowledge chunks.")
