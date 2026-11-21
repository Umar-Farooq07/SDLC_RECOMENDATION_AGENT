"""SQLite persistence for projects, requirements, decisions, and audit events."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SQLiteManager:
    def __init__(self, path: str | Path = "data/requirements.db") -> None:
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS projects (
                    project_id TEXT PRIMARY KEY, name TEXT NOT NULL, domain TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS requirements (
                    req_id TEXT PRIMARY KEY, project_id TEXT NOT NULL, data_json TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(project_id)
                );
                CREATE TABLE IF NOT EXISTS conflicts (
                    conflict_id TEXT PRIMARY KEY, project_id TEXT NOT NULL, data_json TEXT NOT NULL,
                    FOREIGN KEY(project_id) REFERENCES projects(project_id)
                );
                CREATE TABLE IF NOT EXISTS traceability_links (
                    link_id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT NOT NULL,
                    req_id TEXT NOT NULL, target_type TEXT NOT NULL, target_id TEXT NOT NULL,
                    evidence TEXT NOT NULL DEFAULT '',
                    FOREIGN KEY(project_id) REFERENCES projects(project_id)
                );
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT NOT NULL,
                    agent TEXT NOT NULL, action TEXT NOT NULL, confidence REAL,
                    evidence TEXT NOT NULL DEFAULT '', details_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS approvals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, project_id TEXT NOT NULL,
                    approval_type TEXT NOT NULL, target_id TEXT NOT NULL, status TEXT NOT NULL,
                    reviewer TEXT NOT NULL DEFAULT '', comments TEXT NOT NULL DEFAULT '',
                    decision_at TEXT NOT NULL
                );
            """)

    @staticmethod
    def timestamp() -> str:
        return datetime.now(timezone.utc).isoformat()

    def save_project(self, project_id: str, name: str, domain: str) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO projects VALUES (?, ?, ?, ?) ON CONFLICT(project_id) "
                "DO UPDATE SET name=excluded.name, domain=excluded.domain",
                (project_id, name, domain, self.timestamp()),
            )

    def save_requirements(self, project_id: str, requirements: list[Any]) -> None:
        with self.connect() as db:
            for requirement in requirements:
                data = requirement.model_dump(mode="json") if hasattr(requirement, "model_dump") else requirement
                db.execute(
                    "INSERT INTO requirements VALUES (?, ?, ?, ?) ON CONFLICT(req_id) "
                    "DO UPDATE SET data_json=excluded.data_json, updated_at=excluded.updated_at",
                    (data["req_id"], project_id, json.dumps(data), self.timestamp()),
                )

    def save_conflicts(self, project_id: str, conflicts: list[Any]) -> None:
        with self.connect() as db:
            for conflict in conflicts:
                data = conflict.model_dump(mode="json") if hasattr(conflict, "model_dump") else conflict
                db.execute(
                    "INSERT INTO conflicts VALUES (?, ?, ?) ON CONFLICT(conflict_id) "
                    "DO UPDATE SET data_json=excluded.data_json",
                    (data["conflict_id"], project_id, json.dumps(data)),
                )

    def save_traceability_links(self, project_id: str, requirements: list[Any]) -> None:
        with self.connect() as db:
            db.execute("DELETE FROM traceability_links WHERE project_id=?", (project_id,))
            for requirement in requirements:
                data = requirement.model_dump(mode="json") if hasattr(requirement, "model_dump") else requirement
                links = [("stakeholder_evidence", data["req_id"], data.get("source_quote", ""))]
                links.extend(
                    ("regulation", f"{citation['document_title']} § {citation['section']}",
                     citation["supporting_evidence"])
                    for citation in data.get("applicable_regulations", [])
                )
                links.extend(
                    ("security_control", control, control)
                    for control in data.get("security_controls", [])
                )
                test_ids = data.get("test_case_ids") or [f"TC-{data['req_id']}"]
                links.extend(
                    ("test_case", test_id, data["req_id"])
                    for test_id in test_ids
                )
                db.executemany(
                    "INSERT INTO traceability_links(project_id,req_id,target_type,target_id,evidence) "
                    "VALUES(?,?,?,?,?)",
                    [(project_id, data["req_id"], kind, target, evidence)
                     for kind, target, evidence in links],
                )

    def log(self, project_id: str, agent: str, action: str, confidence: float | None = None,
            evidence: str = "", details: dict[str, Any] | None = None) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO audit_logs(project_id,agent,action,confidence,evidence,details_json,created_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (project_id, agent, action, confidence, evidence, json.dumps(details or {}), self.timestamp()),
            )

    def save_approval(self, project_id: str, approval_type: str, target_id: str, status: str,
                      reviewer: str = "", comments: str = "") -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO approvals(project_id,approval_type,target_id,status,reviewer,comments,decision_at) "
                "VALUES(?,?,?,?,?,?,?)",
                (project_id, approval_type, target_id, status, reviewer, comments, self.timestamp()),
            )

    def rows(self, table: str, project_id: str | None = None) -> list[dict[str, Any]]:
        allowed = {"projects", "requirements", "conflicts", "traceability_links", "audit_logs", "approvals"}
        if table not in allowed:
            raise ValueError(f"Unsupported table: {table}")
        with self.connect() as db:
            if project_id and table != "projects":
                result = db.execute(f"SELECT * FROM {table} WHERE project_id=? ORDER BY rowid", (project_id,))
            else:
                result = db.execute(f"SELECT * FROM {table} ORDER BY rowid")
            return [dict(row) for row in result.fetchall()]
