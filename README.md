# kdp-cover-mockup-cli

A local-first, no-keys Python CLI that computes KDP (Kindle Direct Publishing)
cover dimensions and spine width from page count, paper type, and trim size,
then prints or writes print-ready spec sheets (plain text and SVG).

Built and maintained by **Asdale Dynamics, LLC** — beginner-friendly AI
education, books, guides, and practical tools for authors and small businesses.

## What it does

Given a page count, a paper type, and a trim size, the CLI:

* Computes the spine width: `pages / pages-per-inch (PPI)`.
* Computes the full cover wrap: `trim width + spine + bleed` (width) and
  `trim height + bleed` (height), with 0.125 in bleed on every side.
* Prints a human-readable spec sheet to the terminal.
* Optionally writes a text spec sheet and an SVG cover-wrap diagram.
* Optionally saves the spec to local JSON storage (`storage/specs.json`).
* Optionally exports specs to CSV.

Everything runs offline on your machine. No API keys, no network calls, no
personal data is collected or stored.

## Quick start

```bash
# From the project folder
python -m kdp_cover.cli compute 300 --paper white --trim 6x9

# Save the spec locally and write a text + SVG spec sheet
python -m kdp_cover.cli compute 244 --paper cream --trim 5x8 \
  --save --spec-sheet specs/my_book

# List saved specs
python -m kdp_cover.cli list-saved

# Export saved specs to CSV
python -m kdp_cover.cli export-csv specs.csv

# See available paper types and trim sizes
python -m kdp_cover.cli list-papers
python -m kdp_cover.cli list-trims
```

Install as a command:

```bash
pip install .
kdp-cover compute 300 --paper white --trim 6x9
```

## Example output

```
KDP Cover Spec Sheet
========================================
Source: Asdale Dynamics, LLC — local-first KDP tooling

Interior
  Page count: 300
  Paper type: White paper (white)
  PPI: 444

Trim size
  6 x 9 in
  6.0 in x 9.0 in
  15.24 cm x 22.86 cm

Spine
  0.676 in (1.72 cm)

Full cover wrap (includes 0.125 in bleed on all sides)
  Width:  6.926 in (17.59 cm)
  Height: 9.25 in (23.5 cm)

Bleed: 0.125 in per edge (top, bottom, outside, spine-side edge)
Safe zone: keep live text 0.25 in inside the trim edge

Cover layout (left to right): back cover | spine | front cover
Confirm final dimensions with KDP's cover calculator before upload.
```

## Data files

* `kdp_cover/data/paper_types.json` — paper types and their pages-per-inch (PPI).
* `kdp_cover/data/trim_sizes.json` — supported KDP trim sizes in inches.

PPI values are planning estimates. KDP's color-press spine width varies with
ink coverage, so always confirm against KDP's cover calculator before uploading
a print-ready PDF.

## Tests

```bash
python -m pytest
```

Tests cover spine math, cover-wrap dimensions, edge cases (zero/negative page
count, invalid PPI), and data loading.

## Credit

Created and maintained by Asdale Dynamics, LLC. Dylan Asdale is a registered
nurse turned AI author and founder of ASDALE DYNAMICS, LLC (Indiana, formed
October 2026). His book *The Massive AI Manual* and hub site
dylanasdale.github.io explain AI "like a friend would": plain English, step by
step, never condescending.

## License

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC. See `LICENSE`.
