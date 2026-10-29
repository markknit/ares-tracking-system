# A1 response-card candidate

Reproducible, offline ArUco card generation and synthetic print/read tests.
This is A1 only: no Android app, camera capture, answer classifier, roster,
backend, or integration. The [A1 decision and evidence](../docs/track-a-scanner/a1-cards.md)
record the candidate choice and remaining physical checks.

## Setup

Use Python 3.12 (validated on 3.12.14), with a normal virtual environment.
From the repository root in PowerShell:

```powershell
py -3.12 -m venv quiz-tracker/cards/.venv
$python = (Resolve-Path quiz-tracker/cards/.venv/Scripts/python.exe).Path
& $python -m pip install -r quiz-tracker/cards/requirements.txt
```

On Linux/macOS use `python3.12 -m venv quiz-tracker/cards/.venv` and
`quiz-tracker/cards/.venv/bin/python` instead. The `py` launcher is optional;
substitute your Python executable. Dependencies and virtual environments are
not committed. The requirements pin direct and transitive dependencies.
Poppler's `pdftoppm` is also required for the complete test suite.

For an offline build machine, first download wheels on a connected machine
with the same Python version/OS/architecture, transfer that directory, then
install locally:

```powershell
& $python -m pip download -r quiz-tracker/cards/requirements.txt -d quiz-tracker/cards/tmp/wheels
& $python -m pip install --no-index --find-links quiz-tracker/cards/tmp/wheels -r quiz-tracker/cards/requirements.txt
```

After setup, generation, tests, and printing require no Internet. Poppler must
also be provisioned before disconnected testing. The card PDFs have no links,
forms, scripts, or online assets.

## Generate

```powershell
# All 40 cards, one page per card, in ascending order.
& $python quiz-tracker/cards/generate_cards.py --output quiz-tracker/cards/tmp/class-set.pdf
# Reproduce the committed four-page sample at a NEW path.
& $python quiz-tracker/cards/generate_cards.py --cards 1,2,20,40 --output quiz-tracker/cards/tmp/sample.pdf
```

The generator refuses existing PDF/JSON destinations and duplicate/out-of-range
card numbers. Requested order is preserved. It writes a vector PDF and JSON
sidecar containing layout, dimensions, family, IDs, module-grid hashes, and the
PDF SHA-256. The sidecar is a local artifact inventory, not an observation or
shared wire contract. Identical inputs with the pinned environment reproduce
identical bytes; no random IDs, current timestamps, paths, or student records
enter the PDF. Other dependency/runtime versions are not byte-identity promises.
The local `.gitattributes` marks PDFs as binary to prevent Git newline conversion.

The committed [sample PDF](output/pdf/a1-test-cards.pdf) and
[inventory](output/pdf/a1-test-cards.json) cover card numbers 01, 02, 20, and 40.

## Print and hold

| Property | A1 candidate |
| --- | --- |
| Family | OpenCV `DICT_4X4_50`; standard predefined dictionary |
| Card number | 01 through 40; reusable token, never student identity |
| Marker ID | card number minus 1; IDs 0 through 39 |
| Reserved | IDs 40 through 49 are unused; not extra assigned cards |
| Page / cut card | A4 portrait 210 x 297 mm / 180 x 180 mm square |
| Outer black marker | 96 x 96 mm; 4 x 4 payload plus one black cell border |
| Module / white margin | 16 mm / at least 16 mm on all four sides |
| Front edge labels | Top A, right B, bottom C, left D |

Print **single-sided, A4, Actual size / 100%**, one PDF page per sheet. Disable
fit/shrink, multiple pages per sheet, booklet, mirroring, and duplex. Use opaque
matte white paper or card with dense black ink. Keep the front flat; avoid glossy
lamination, ink-saving modes, smears, folds, and added marks near the code.

Before cutting, measure the 50 mm scale bar (target 50 +/- 0.5 mm), black marker
(96 +/- 1 mm each side), and dashed square (180 +/- 1 mm each side). Reprint at
correct scale if any dimension fails. Cut the dashed square; keep its white
margin and printed card numbers intact. The family/layout identifier remains
inside the cut card. Keep fingers outside the code and its white margin.

Hold the chosen answer edge at the top, printed front facing the camera.
Relative to the canonical front shown in the PDF:

| Answer at top | Physical turn from the printed front |
| --- | --- |
| A | No turn |
| B | 90 degrees counterclockwise |
| C | 180 degrees |
| D | 90 degrees clockwise |

This is the physical legend only. A4 will implement and test camera rotation,
pose rejection, and preview/mirror behavior. Never infer answers from a mirrored
preview or assume its display rotation equals the sensor rotation.

## Verify

```powershell
# Omit this assignment if pdftoppm is already on PATH.
$env:PDFTOPPM = 'C:\path\to\poppler\bin\pdftoppm.exe'
& $python -m unittest discover -s quiz-tracker/cards/tests -v
```

The seven tests check a known upstream codeword, 40 unique markers with no
rotational collisions, invalid inputs, CLI overwrite protection, deterministic
bytes and inventory, A4 page dimensions/labels, and the committed sample. The
render test generates all 40 PDF pages, rasterizes them independently at 100 dpi
using Poppler, and checks each entire page at four rotations: exactly one
expected ID and the correct canonical first corner, with no unexpected IDs.
It also checks clean white bands and rendered marker size. A missing Poppler
tool is a failure, not a skipped success. All raster/temp files are temporary.

These checks validate synthetic artwork. They do not establish physical print
accuracy, camera range, false-assignment rate, or classroom feasibility. Follow
the manual checklist in the evidence document before using a printed batch.
