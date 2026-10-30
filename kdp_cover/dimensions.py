"""KDP cover dimension math.

Spine math follows the KDP baseline:

    spine width (in) = page count / pages-per-inch (PPI)

PPI values live in kdp_cover/data/paper_types.json. They are documented
estimates (KDP's color-press spine varies with ink coverage), so treat
results as a planning estimate and confirm against KDP's cover calculator
before uploading a print-ready PDF.

All measurements are in inches unless noted. 1 in = 2.54 cm.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

BLEED_IN = 0.125          # KDP bleed applied per edge (top, bottom, outside)
SAFE_ZONE_IN = 0.25       # keep live text this far inside the trim edge
IN_TO_CM = 2.54


@dataclass(frozen=True)
class TrimSize:
    key: str
    label: str
    width_in: float
    height_in: float

    def width_cm(self) -> float:
        return round(self.width_in * IN_TO_CM, 2)

    def height_cm(self) -> float:
        return round(self.height_in * IN_TO_CM, 2)


@dataclass(frozen=True)
class PaperType:
    id: str
    name: str
    ppi: float


@dataclass(frozen=True)
class CoverSpec:
    pages: int
    paper: PaperType
    trim: TrimSize
    spine_in: float
    spine_cm: float
    cover_width_in: float
    cover_height_in: float
    cover_width_cm: float
    cover_height_cm: float
    bleed_in: float = BLEED_IN
    safe_zone_in: float = SAFE_ZONE_IN

    def width_parts_in(self) -> tuple[float, float, float]:
        """(trim width, spine width, total bleed added) in inches."""
        return (self.trim.width_in, self.spine_in, 2 * self.bleed_in)

    def height_parts_in(self) -> tuple[float, float]:
        """(trim height, total bleed added) in inches."""
        return (self.trim.height_in, 2 * self.bleed_in)


def spine_width_inches(pages: int, ppi: float) -> float:
    """Return spine width in inches for a page count and paper PPI."""
    if pages < 0:
        raise ValueError("page count cannot be negative")
    if ppi <= 0:
        raise ValueError("PPI must be positive")
    return pages / ppi


def compute_cover_spec(pages: int, paper: PaperType, trim: TrimSize) -> CoverSpec:
    """Compute full cover spec: spine width and cover dimensions with bleed."""
    if pages < 0:
        raise ValueError("page count cannot be negative")
    spine_in = spine_width_inches(pages, paper.ppi)
    cover_width_in = trim.width_in + spine_in + 2 * BLEED_IN
    cover_height_in = trim.height_in + 2 * BLEED_IN
    return CoverSpec(
        pages=pages,
        paper=paper,
        trim=trim,
        spine_in=round(spine_in, 3),
        spine_cm=round(spine_in * IN_TO_CM, 2),
        cover_width_in=round(cover_width_in, 3),
        cover_height_in=round(cover_height_in, 3),
        cover_width_cm=round(cover_width_in * IN_TO_CM, 2),
        cover_height_cm=round(cover_height_in * IN_TO_CM, 2),
    )


def load_paper_types(path: str) -> list[PaperType]:
    import json

    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return [PaperType(id=p["id"], name=p["name"], ppi=float(p["ppi"])) for p in data["paper_types"]]


def load_trim_sizes(path: str) -> list[TrimSize]:
    import json

    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return [
        TrimSize(key=t["key"], label=t["label"], width_in=float(t["width_in"]), height_in=float(t["height_in"]))
        for t in data["trim_sizes"]
    ]


def find_paper(papers: Iterable[PaperType], paper_id: str) -> PaperType:
    for paper in papers:
        if paper.id == paper_id:
            return paper
    raise KeyError(f"unknown paper type: {paper_id}")


def find_trim(trims: Iterable[TrimSize], key: str) -> TrimSize:
    for trim in trims:
        if trim.key == key:
            return trim
    raise KeyError(f"unknown trim size: {key}")
