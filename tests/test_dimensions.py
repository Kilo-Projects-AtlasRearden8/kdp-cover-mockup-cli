"""Tests for KDP cover dimension math."""

import pytest

from kdp_cover.dimensions import (
    spine_width_inches,
    compute_cover_spec,
    load_paper_types,
    load_trim_sizes,
    find_paper,
    find_trim,
    BLEED_IN,
    IN_TO_CM,
)
DATA_DIR = "kdp_cover/data"


def test_spine_width_basic():
    # 300 pages at 444 ppi
    assert spine_width_inches(300, 444) == pytest.approx(300 / 444)


def test_spine_width_rounding():
    spec = compute_cover_spec(300, _paper("white", 444), _trim("6x9", 6.0, 9.0))
    expected_spine = 300 / 444
    assert spec.spine_in == pytest.approx(round(expected_spine, 3))
    assert spec.spine_cm == pytest.approx(round(expected_spine * IN_TO_CM, 2))


def test_cover_dimensions_include_bleed():
    spec = compute_cover_spec(300, _paper("white", 444), _trim("6x9", 6.0, 9.0))
    spine = 300 / 444
    assert spec.cover_width_in == pytest.approx(round(6.0 + spine + 2 * BLEED_IN, 3))
    assert spec.cover_height_in == pytest.approx(round(9.0 + 2 * BLEED_IN, 3))


def test_zero_pages():
    spec = compute_cover_spec(0, _paper("white", 444), _trim("6x9", 6.0, 9.0))
    assert spec.spine_in == 0.0
    assert spec.spine_cm == 0.0


def test_negative_pages_raises():
    with pytest.raises(ValueError):
        spine_width_inches(-1, 444)
    with pytest.raises(ValueError):
        compute_cover_spec(-1, _paper("white", 444), _trim("6x9", 6.0, 9.0))


def test_zero_or_negative_ppi_raises():
    with pytest.raises(ValueError):
        spine_width_inches(100, 0)
    with pytest.raises(ValueError):
        spine_width_inches(100, -5)


def test_known_values():
    # 244 pages at 444 ppi -> 0.5495... in spine
    spec = compute_cover_spec(244, _paper("white", 444), _trim("6x9", 6.0, 9.0))
    assert spec.spine_in == pytest.approx(round(244 / 444, 3))


def test_load_paper_types():
    papers = load_paper_types(f"{DATA_DIR}/paper_types.json")
    assert any(p.id == "white" for p in papers)
    assert all(p.ppi > 0 for p in papers)


def test_load_trim_sizes():
    trims = load_trim_sizes(f"{DATA_DIR}/trim_sizes.json")
    keys = {t.key for t in trims}
    assert "6x9" in keys
    assert "5x8" in keys
    assert all(t.width_in > 0 and t.height_in > 0 for t in trims)


def test_find_unknown_raises():
    papers = load_paper_types(f"{DATA_DIR}/paper_types.json")
    trims = load_trim_sizes(f"{DATA_DIR}/trim_sizes.json")
    with pytest.raises(KeyError):
        find_paper(papers, "nope")
    with pytest.raises(KeyError):
        find_trim(trims, "nope")


def _paper(pid, ppi):
    from kdp_cover.dimensions import PaperType
    return PaperType(id=pid, name=pid, ppi=ppi)


def _trim(key, w, h):
    from kdp_cover.dimensions import TrimSize
    return TrimSize(key=key, label=key, width_in=w, height_in=h)
