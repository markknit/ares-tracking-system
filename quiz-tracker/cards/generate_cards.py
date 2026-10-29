"""A1 printable candidate. No capture, answer inference, roster, or transport code."""

import argparse
import hashlib
import io
import json
from pathlib import Path

import cv2
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

FAMILY = "DICT_4X4_50"
LAYOUT = "ares-a1-v1"
CARD_COUNT = 40
PAGE_MM = (210, 297)
CARD_MM = 180
MARKER_MM = 96
QUIET_MM = 16  # One complete cell around a 6 x 6 marker including its border.
EDGE_ANSWERS = ("A", "B", "C", "D")  # Top, right, bottom, left on canonical front.


def validate_cards(cards):
    cards = tuple(cards)
    if not cards or any(type(n) is not int or not 1 <= n <= CARD_COUNT for n in cards):
        raise ValueError("Card numbers must be integers from 1 through 40")
    if len(set(cards)) != len(cards):
        raise ValueError("Duplicate card numbers are not allowed")
    return cards


def marker_grid(card_number):
    validate_cards([card_number])
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    return cv2.aruco.generateImageMarker(dictionary, card_number - 1, 6, borderBits=1)


def label(canvas, x, y, text, size=10, rotation=0):
    canvas.saveState()
    canvas.translate(x * mm, y * mm)
    canvas.rotate(rotation)
    canvas.setFont("Helvetica-Bold", size)
    canvas.drawCentredString(0, 0, text)
    canvas.restoreState()


def draw_card(canvas, card_number):
    # Coordinates are in physical millimetres. Front view, no reflection.
    label(canvas, 105, 279, "ARES RESPONSE CARD - A1 TEST CANDIDATE", 13)
    label(canvas, 105, 269, f"CARD {card_number:02d}  |  {FAMILY} ID {card_number - 1}", 11)
    canvas.saveState()
    canvas.translate(15 * mm, 60 * mm)
    canvas.setLineWidth(0.2 * mm)
    canvas.setDash(2 * mm, 2 * mm)
    canvas.rect(0, 0, CARD_MM * mm, CARD_MM * mm)
    canvas.setDash()
    for answer, (x, y, rotation) in zip(
        EDGE_ANSWERS, ((90, 166, 0), (166, 90, -90), (90, 14, 180), (14, 90, 90))
    ):
        label(canvas, x, y, answer, 32, rotation)
    # Outer black marker bounds: x/y 42..138. Quiet bounds: 26..154.
    # Black horizontal runs share boundaries exactly; no image interpolation.
    grid = marker_grid(card_number)
    for row in range(6):
        col = 0
        while col < 6:
            if grid[row, col] != 0:
                col += 1
                continue
            start = col
            while col < 6 and grid[row, col] == 0:
                col += 1
            canvas.rect((42 + start * 16) * mm, (42 + (5 - row) * 16) * mm,
                        (col - start) * 16 * mm, 16 * mm, stroke=0, fill=1)
    # Number is repeated on the retained card, outside the quiet zone.
    label(canvas, 18, 169, f"{card_number:02d}", 11)
    label(canvas, 162, 7, f"{card_number:02d}", 11, 180)
    label(canvas, 90, 158, f"{FAMILY} | {LAYOUT}", 6)
    canvas.restoreState()
    label(canvas, 105, 48, "Hold the chosen answer at the TOP, facing the camera.", 10)
    label(canvas, 105, 41, "Print A4 at 100% / Actual size. Single-sided. Cut dashed square.", 9)
    label(canvas, 105, 34, "Keep fingers and writing outside the marker and white margin.", 9)
    # Scale bar outside the card. Check before cutting.
    canvas.setLineWidth(0.3 * mm)
    canvas.line(80 * mm, 23 * mm, 130 * mm, 23 * mm)
    for x in (80, 130):
        canvas.line(x * mm, 21 * mm, x * mm, 25 * mm)
    label(canvas, 105, 16, "50 mm scale check | Marker 96 mm | Card 180 mm", 9)
    label(canvas, 105, 8, f"{LAYOUT} | Reusable card token; no student identity", 8)


def pdf_bytes(cards):
    cards = validate_cards(cards)
    stream = io.BytesIO()
    canvas = Canvas(stream, pagesize=tuple(n * mm for n in PAGE_MM),
                    invariant=1, pageCompression=1, pdfVersion=(1, 4))
    canvas.setTitle("ARES A1 response-card candidates")
    canvas.setAuthor("ARES Track A")
    canvas.setSubject(f"{LAYOUT}; {FAMILY}; synthetic reusable card tokens")
    for card_number in cards:
        draw_card(canvas, card_number)
        canvas.showPage()
    canvas.save()
    return stream.getvalue()


def manifest(cards, pdf):
    return {
        "layout_version": LAYOUT,
        "marker_family": FAMILY,
        "opencv_version": cv2.__version__,
        "page_mm": list(PAGE_MM),
        "card_mm": CARD_MM,
        "marker_mm": MARKER_MM,
        "quiet_zone_mm": QUIET_MM,
        "border_bits": 1,
        "canonical_front_edges": dict(zip(("top", "right", "bottom", "left"), EDGE_ANSWERS)),
        "pdf_sha256": hashlib.sha256(pdf).hexdigest(),
        "cards": [{"card_number": n, "marker_id": n - 1,
                   "grid_sha256": hashlib.sha256(marker_grid(n).tobytes()).hexdigest()}
                  for n in cards],
    }


def parse_cards(value):
    try:
        return validate_cards([int(part) for part in value.split(",")])
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cards", type=parse_cards, default=tuple(range(1, 41)),
                        help="Unique comma-separated card numbers 1..40; default all 40")
    parser.add_argument("--output", type=Path, required=True, help="Destination .pdf (must not exist)")
    args = parser.parse_args(argv)
    if args.output.suffix.lower() != ".pdf":
        parser.error("--output must end in .pdf")
    sidecar = args.output.with_suffix(".json")
    if args.output.exists() or sidecar.exists():
        parser.error("Output PDF or JSON already exists; choose a new path")
    pdf = pdf_bytes(args.cards)
    metadata = manifest(args.cards, pdf)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pdf)
    sidecar.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(args.cards)} cards to {args.output} and {sidecar}")


if __name__ == "__main__":
    main()
