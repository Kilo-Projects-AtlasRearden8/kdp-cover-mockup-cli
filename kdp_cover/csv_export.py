"""CSV export for saved cover specs."""

from __future__ import annotations

import csv
import os
from typing import Any

FIELDNAMES = [
    "created_at",
    "pages",
    "paper_id",
    "paper_name",
    "ppi",
    "trim_key",
    "trim_label",
    "trim_width_in",
    "trim_height_in",
    "spine_in",
    "spine_cm",
    "cover_width_in",
    "cover_height_in",
    "cover_width_cm",
    "cover_height_cm",
    "bleed_in",
    "safe_zone_in",
]


def spec_to_row(record: dict[str, Any]) -> dict[str, Any]:
    flat: dict[str, Any] = {}
    flat["created_at"] = record.get("created_at", "")
    flat["pages"] = record.get("pages", "")
    paper = record.get("paper", {}) or {}
    flat["paper_id"] = paper.get("id", record.get("paper_id", ""))
    flat["paper_name"] = paper.get("name", record.get("paper_name", ""))
    flat["ppi"] = paper.get("ppi", record.get("ppi", ""))
    trim = record.get("trim", {}) or {}
    flat["trim_key"] = trim.get("key", record.get("trim_key", ""))
    flat["trim_label"] = trim.get("label", record.get("trim_label", ""))
    flat["trim_width_in"] = trim.get("width_in", record.get("trim_width_in", ""))
    flat["trim_height_in"] = trim.get("height_in", record.get("trim_height_in", ""))
    flat["spine_in"] = record.get("spine_in", "")
    flat["spine_cm"] = record.get("spine_cm", "")
    flat["cover_width_in"] = record.get("cover_width_in", "")
    flat["cover_height_in"] = record.get("cover_height_in", "")
    flat["cover_width_cm"] = record.get("cover_width_cm", "")
    flat["cover_height_cm"] = record.get("cover_height_cm", "")
    flat["bleed_in"] = record.get("bleed_in", "")
    flat["safe_zone_in"] = record.get("safe_zone_in", "")
    return flat


def export_csv(records: list[dict[str, Any]], path: str) -> str:
    """Write records to CSV at path. Returns the path written."""
    directory = os.path.dirname(os.path.abspath(path))
    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow(spec_to_row(record))
    return path
