# STATUS.md — kdp-cover-mockup-cli

## What was built

A local-first, no-keys Python CLI that computes KDP (Kindle Direct Publishing)
cover dimensions and spine width from page count, paper type, and trim size,
and outputs print-ready spec sheets.

Package: `kdp_cover` (installable via `pip install .`, provides the `kdp-cover`
console script; also runnable as `python3 -m kdp_cover.cli`).

### Modules
- `kdp_cover/dimensions.py` — spine/cover math: `spine = pages / PPI`; full
  cover wrap = trim + spine + 0.125 in bleed on all sides; height = trim +
  bleed. Loads paper types and trim sizes from JSON. Raises on negative page
  count or non-positive PPI.
- `kdp_cover/data/paper_types.json` — white/cream/color paper types (444 PPI
  baseline each).
- `kdp_cover/data/trim_sizes.json` — 17 KDP trim sizes (5x8 through 11x8.5,
  including A4/A5).
- `kdp_cover/storage.py` — append-only local JSON storage
  (`storage/specs.json` by default); load/save/clear records.
- `kdp_cover/spec_sheet.py` — plain-text spec sheet and an SVG cover-wrap
  diagram (bleed, trim, spine, safe zone, back|spine|front layout).
- `kdp_cover/csv_export.py` — export saved specs to CSV.
- `kdp_cover/cli.py` — argparse CLI: `compute`, `list-papers`, `list-trims`,
  `list-saved`, `clear-saved`, `export-csv`.

### Supporting files
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics,
  LLC`.
- `README.md` — usage, examples, data files, tests, credit to Asdale Dynamics,
  LLC, license.
- `pyproject.toml` — setuptools build, `kdp-cover` console script, package data
  (`data/*.json`).
- `tests/test_dimensions.py` — 10 tests for spine math, cover-wrap dimensions,
  edge cases, and data loading.
- `.gitignore` — excludes caches, build artifacts, `storage/*.json`, `specs/`.

Credit: built by Asdale Dynamics, LLC (Dylan Asdale, founder; Indiana, formed
October 2026).

## How to run it

```bash
# From the project folder (no install needed)
python3 -m kdp_cover.cli compute 300 --paper white --trim 6x9

# Save locally + write text + SVG spec sheet + append to CSV
python3 -m kdp_cover.cli compute 244 --paper cream --trim 5x8 \
  --save --spec-sheet specs/my_book --export-csv specs/export.csv

# List available data
python3 -m kdp_cover.cli list-papers
python3 -m kdp_cover.cli list-trims

# Manage saved specs
python3 -m kdp_cover.cli list-saved
python3 -m kdp_cover.cli export-csv specs.csv
python3 -m kdp_cover.cli clear-saved

# Or install as a command
pip install .
kdp-cover compute 300 --paper white --trim 6x9
```

Run tests: `python3 -m pytest`

## Verification results

- `python3 -m pytest`: **10 passed**.
- CLI `compute 300 --paper white --trim 6x9 --save --spec-sheet ... --export-csv ...`:
  prints spec sheet, writes `specs/*.txt` and `specs/*.svg`, saves to
  `storage/specs.json`, appends to CSV — all verified working.
- Console script `kdp-cover` (installed into an isolated venv from `pip install .`)
  runs correctly from a different working directory; package data (`data/*.json`)
  ships with the installed package.
- Example: 300 pages, white paper, 6x9 trim → spine 0.676 in (1.72 cm),
  cover 6.926 x 9.25 in (17.59 x 23.5 cm) with 0.125 in bleed.

No API keys, secrets, or personal data in any file. No network access. Local
JSON storage only.

## Known gaps

- Color-paper PPI (444) is a planning estimate; KDP color-press spine width
  varies with ink coverage. Always confirm with KDP's cover calculator before
  uploading a print-ready PDF.
- The SVG is a planning/layout diagram, not a KDP-validated print-ready PDF
  (KDP requires a PDF upload).
- No enforcement of KDP page-count minimum/maximum per trim size.
- Default storage path is relative (`storage/specs.json`); run from the project
  folder or pass `--storage`.
- System `pip install .` is blocked by PEP 668 on some environments; use a
  virtual environment or run via `python3 -m kdp_cover.cli`.
