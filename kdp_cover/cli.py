"""Command-line interface for the KDP cover mockup tool."""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional, Sequence

from .dimensions import (
    load_paper_types,
    load_trim_sizes,
    find_paper,
    find_trim,
    compute_cover_spec,
)
from .storage import save_record, load_records, clear_records, DEFAULT_STORAGE_PATH
from .csv_export import export_csv
from .spec_sheet import spec_to_text, write_spec_sheet


def _data_dir(args) -> str:
    if getattr(args, "data_dir", None):
        return args.data_dir
    return os.path.join(os.path.dirname(__file__), "data")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kdp-cover",
        description="Compute KDP cover dimensions and spine width from page count, "
        "paper type, and trim size. Local-first, no keys.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_compute = sub.add_parser("compute", help="Compute a cover spec.")
    p_compute.add_argument("pages", type=int, help="Page count of the interior.")
    p_compute.add_argument("--paper", default="white", help="Paper type id (default: white).")
    p_compute.add_argument("--trim", default="6x9", help="Trim size key (default: 6x9).")
    p_compute.add_argument(
        "--data-dir", default=None, help="Directory containing data JSON files."
    )
    p_compute.add_argument(
        "--save", action="store_true", help="Save the computed spec to local JSON storage."
    )
    p_compute.add_argument(
        "--spec-sheet", metavar="BASE", help="Write text+SVG spec sheets to BASE.txt / BASE.svg."
    )
    p_compute.add_argument(
        "--export-csv", metavar="PATH", help="Append this spec to a CSV file at PATH."
    )
    p_compute.add_argument(
        "--storage", default=DEFAULT_STORAGE_PATH, help="JSON storage file path."
    )

    sub.add_parser("list-papers", help="List available paper types.")
    sub.add_parser("list-trims", help="List available trim sizes.")

    p_saved = sub.add_parser("list-saved", help="List saved specs from local storage.")
    p_saved.add_argument("--storage", default=DEFAULT_STORAGE_PATH)

    p_clear = sub.add_parser("clear-saved", help="Clear all saved specs from local storage.")
    p_clear.add_argument("--storage", default=DEFAULT_STORAGE_PATH)

    p_export = sub.add_parser("export-csv", help="Export saved specs to CSV.")
    p_export.add_argument("path", help="Output CSV path.")
    p_export.add_argument("--storage", default=DEFAULT_STORAGE_PATH)

    return parser


def spec_to_record(spec) -> dict:
    return {
        "pages": spec.pages,
        "paper": {"id": spec.paper.id, "name": spec.paper.name, "ppi": spec.paper.ppi},
        "trim": {
            "key": spec.trim.key,
            "label": spec.trim.label,
            "width_in": spec.trim.width_in,
            "height_in": spec.trim.height_in,
        },
        "spine_in": spec.spine_in,
        "spine_cm": spec.spine_cm,
        "cover_width_in": spec.cover_width_in,
        "cover_height_in": spec.cover_height_in,
        "cover_width_cm": spec.cover_width_cm,
        "cover_height_cm": spec.cover_height_cm,
        "bleed_in": spec.bleed_in,
        "safe_zone_in": spec.safe_zone_in,
    }


def cmd_compute(args: argparse.Namespace) -> int:
    data_dir = _data_dir(args)
    papers = load_paper_types(os.path.join(data_dir, "paper_types.json"))
    trims = load_trim_sizes(os.path.join(data_dir, "trim_sizes.json"))
    paper = find_paper(papers, args.paper)
    trim = find_trim(trims, args.trim)
    spec = compute_cover_spec(args.pages, paper, trim)

    print(spec_to_text(spec))
    if args.save:
        save_record(spec_to_record(spec), args.storage)
        print(f"\nSaved to {args.storage}")
    if args.spec_sheet:
        paths = write_spec_sheet(spec, args.spec_sheet)
        print(f"Spec sheet: {paths['text']}")
        print(f"Spec sheet: {paths['svg']}")
    if args.export_csv:
        export_csv([spec_to_record(spec)], args.export_csv)
        print(f"CSV: {args.export_csv}")
    return 0


def cmd_list_papers(args: argparse.Namespace) -> int:
    data_dir = _data_dir(args)
    papers = load_paper_types(os.path.join(data_dir, "paper_types.json"))
    for p in papers:
        print(f"{p.id:10} {p.name:12} ppi={p.ppi}")
    return 0


def cmd_list_trims(args: argparse.Namespace) -> int:
    data_dir = _data_dir(args)
    trims = load_trim_sizes(os.path.join(data_dir, "trim_sizes.json"))
    for t in trims:
        print(f"{t.key:14} {t.label:24} {t.width_in} in x {t.height_in} in")
    return 0


def cmd_list_saved(args: argparse.Namespace) -> int:
    records = load_records(args.storage)
    if not records:
        print("No saved specs.")
        return 0
    for i, r in enumerate(records, 1):
        paper = r.get("paper", {})
        trim = r.get("trim", {})
        print(
            f"{i}. {r.get('created_at','')} pages={r.get('pages')} "
            f"paper={paper.get('id','?')} trim={trim.get('key','?')} "
            f"spine={r.get('spine_in','?')} in cover={r.get('cover_width_in','?')}x{r.get('cover_height_in','?')} in"
        )
    return 0


def cmd_clear_saved(args: argparse.Namespace) -> int:
    count = clear_records(args.storage)
    print(f"Cleared {count} saved specs from {args.storage}")
    return 0


def cmd_export_csv(args: argparse.Namespace) -> int:
    records = load_records(args.storage)
    export_csv(records, args.path)
    print(f"Exported {len(records)} records to {args.path}")
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "compute":
        return cmd_compute(args)
    if args.command == "list-papers":
        return cmd_list_papers(args)
    if args.command == "list-trims":
        return cmd_list_trims(args)
    if args.command == "list-saved":
        return cmd_list_saved(args)
    if args.command == "clear-saved":
        return cmd_clear_saved(args)
    if args.command == "export-csv":
        return cmd_export_csv(args)
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
