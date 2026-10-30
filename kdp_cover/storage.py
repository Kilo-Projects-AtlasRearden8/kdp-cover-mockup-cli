"""Local JSON storage for saved cover specs.

Each saved spec is a JSON record written to a single storage file.
Records are append-only; the file holds a JSON array of spec objects.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

DEFAULT_STORAGE_PATH = os.path.join("storage", "specs.json")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def load_records(path: str = DEFAULT_STORAGE_PATH) -> list[dict[str, Any]]:
    """Load all saved spec records from the JSON storage file."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        return []
    return data


def save_record(
    record: dict[str, Any], path: str = DEFAULT_STORAGE_PATH
) -> dict[str, Any]:
    """Append a spec record to the JSON storage file and return it."""
    _ensure_parent(path)
    records = load_records(path)
    entry = dict(record)
    entry.setdefault("created_at", _now_iso())
    records.append(entry)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(records, handle, indent=2)
    return entry


def clear_records(path: str = DEFAULT_STORAGE_PATH) -> int:
    """Remove all saved records. Returns the number removed."""
    if not os.path.exists(path):
        return 0
    records = load_records(path)
    count = len(records)
    _ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump([], handle, indent=2)
    return count
