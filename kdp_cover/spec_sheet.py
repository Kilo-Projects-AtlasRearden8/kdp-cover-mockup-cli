"""Print-ready spec sheet rendering: plain text and SVG."""

from __future__ import annotations

import os

from .dimensions import CoverSpec, BLEED_IN, SAFE_ZONE_IN


def spec_to_text(spec: CoverSpec) -> str:
    lines: list[str] = []
    lines.append("KDP Cover Spec Sheet")
    lines.append("=" * 40)
    lines.append("")
    lines.append("Source: Asdale Dynamics, LLC — local-first KDP tooling")
    lines.append("")
    lines.append("Interior")
    lines.append(f"  Page count: {spec.pages}")
    lines.append(f"  Paper type: {spec.paper.name} ({spec.paper.id})")
    lines.append(f"  PPI: {spec.paper.ppi}")
    lines.append("")
    lines.append("Trim size")
    lines.append(f"  {spec.trim.label}")
    lines.append(f"  {spec.trim.width_in} in x {spec.trim.height_in} in")
    lines.append(f"  {spec.trim.width_cm()} cm x {spec.trim.height_cm()} cm")
    lines.append("")
    lines.append("Spine")
    lines.append(f"  {spec.spine_in} in ({spec.spine_cm} cm)")
    lines.append("")
    lines.append("Full cover wrap (includes 0.125 in bleed on all sides)")
    lines.append(f"  Width:  {spec.cover_width_in} in ({spec.cover_width_cm} cm)")
    lines.append(f"  Height: {spec.cover_height_in} in ({spec.cover_height_cm} cm)")
    lines.append("")
    lines.append("Bleed: 0.125 in per edge (top, bottom, outside, spine-side edge)")
    lines.append(f"Safe zone: keep live text {SAFE_ZONE_IN} in inside the trim edge")
    lines.append("")
    lines.append("Cover layout (left to right): back cover | spine | front cover")
    lines.append("Confirm final dimensions with KDP's cover calculator before upload.")
    return "\n".join(lines) + "\n"


def spec_to_svg(spec: CoverSpec) -> str:
    """Render an SVG cover-wrap diagram with bleed, trim, spine, and safe zone.

    Units are inches; viewBox matches the bleed-to-bleed cover size so the
    drawing prints at true size when width/height are set in inches.
    """
    w = spec.trim.width_in
    h = spec.trim.height_in
    s = spec.spine_in
    b = spec.bleed_in
    sz = SAFE_ZONE_IN

    total_w = w + s + 2 * b
    total_h = h + 2 * b

    # Geometry: cover wrap runs back | spine | front left to right.
    back_x = b
    spine_x = back_x + w
    front_x = spine_x + s

    # Trim rectangle (inset by bleed from outer edges)
    trim_x = b
    trim_y = b

    # Safe zone rectangle (inset by safe zone from trim edges)
    safe_x = trim_x + sz
    safe_y = trim_y + sz
    safe_w = w - 2 * sz
    safe_h = h - 2 * sz

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {total_w:.3f} {total_h:.3f}" '
        f'width="{total_w:.3f}in" height="{total_h:.3f}in">'
    )
    parts.append(
        f'<rect x="0" y="0" width="{total_w:.3f}" height="{total_h:.3f}" '
        f'fill="#ffffff" stroke="#000000" stroke-width="0.5"/>'
    )
    # Bleed area (outer frame)
    parts.append(
        f'<rect x="0" y="0" width="{total_w:.3f}" height="{total_h:.3f}" '
        f'fill="none" stroke="#d9d9d9" stroke-width="0.75" stroke-dasharray="4,2"/>'
    )
    # Bleed label
    parts.append(
        f'<text x="{total_w/2:.3f}" y="{b/2:.3f}" font-size="8" '
        f'text-anchor="middle" fill="#666666">bleed ({b} in)</text>'
    )
    # Trim rectangle
    parts.append(
        f'<rect x="{trim_x:.3f}" y="{trim_y:.3f}" width="{w:.3f}" height="{h:.3f}" '
        f'fill="none" stroke="#000000" stroke-width="1.25"/>'
    )
    # Spine divider lines within trim
    parts.append(
        f'<line x1="{spine_x:.3f}" y1="{trim_y:.3f}" x2="{spine_x:.3f}" '
        f'y2="{trim_y + h:.3f}" stroke="#333333" stroke-width="1" stroke-dasharray="2,2"/>'
    )
    parts.append(
        f'<line x1="{front_x:.3f}" y1="{trim_y:.3f}" x2="{front_x:.3f}" '
        f'y2="{trim_y + h:.3f}" stroke="#333333" stroke-width="1" stroke-dasharray="2,2"/>'
    )
    # Back / spine / front fill (light tints)
    parts.append(
        f'<rect x="{back_x:.3f}" y="{trim_y:.3f}" width="{w:.3f}" height="{h:.3f}" '
        f'fill="#eef2f6" opacity="0.5"/>'
    )
    parts.append(
        f'<rect x="{spine_x:.3f}" y="{trim_y:.3f}" width="{s:.3f}" height="{h:.3f}" '
        f'fill="#d9e2ec" opacity="0.7"/>'
    )
    parts.append(
        f'<rect x="{front_x:.3f}" y="{trim_y:.3f}" width="{w:.3f}" height="{h:.3f}" '
        f'fill="#eef2f6" opacity="0.5"/>'
    )
    # Safe zone
    parts.append(
        f'<rect x="{safe_x:.3f}" y="{safe_y:.3f}" width="{safe_w:.3f}" height="{safe_h:.3f}" '
        f'fill="none" stroke="#2e7d32" stroke-width="0.75" stroke-dasharray="3,2"/>'
    )
    # Dimension labels
    parts.append(
        f'<text x="{back_x + w/2:.3f}" y="{trim_y + h + 0.2:.3f}" font-size="10" '
        f'text-anchor="middle" fill="#000000">trim {w:.2f} in x {h:.2f} in</text>'
    )
    parts.append(
        f'<text x="{spine_x + s/2:.3f}" y="{trim_y + h/2:.3f}" font-size="10" '
        f'text-anchor="middle" fill="#000000">spine {s:.3f} in</text>'
    )
    parts.append(
        f'<text x="{front_x + w/2:.3f}" y="{trim_y + h + 0.2:.3f}" font-size="10" '
        f'text-anchor="middle" fill="#000000">front cover</text>'
    )
    parts.append(
        f'<text x="{back_x + w/2:.3f}" y="{trim_y + h/2:.3f}" font-size="10" '
        f'text-anchor="middle" fill="#000000">back cover</text>'
    )
    # Overall width label below
    parts.append(
        f'<text x="{total_w/2:.3f}" y="{total_h - 0.1:.3f}" font-size="10" '
        f'text-anchor="middle" fill="#000000">total cover width {total_w:.3f} in</text>'
    )
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def write_spec_sheet(spec: CoverSpec, base_path: str) -> dict[str, str]:
    """Write text and SVG spec sheets. Returns the paths written."""
    directory = os.path.dirname(os.path.abspath(base_path))
    if directory and not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)
    text_path = f"{base_path}.txt"
    svg_path = f"{base_path}.svg"
    with open(text_path, "w", encoding="utf-8") as handle:
        handle.write(spec_to_text(spec))
    with open(svg_path, "w", encoding="utf-8") as handle:
        handle.write(spec_to_svg(spec))
    return {"text": text_path, "svg": svg_path}
