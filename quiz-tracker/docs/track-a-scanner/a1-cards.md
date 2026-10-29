# A1 - Printable response-card candidate

Date: 2026-10-28. Status: A1 implementation complete; candidate for physical tests.
Authorization: the project lead explicitly requested A1 only on branch
`track-a-scanner`, with tests, documentation, sample PDF, and a local commit.
Stop before A2. This does not authorize B1 or approve a shared contract.

## Decision and alternatives

Select standard OpenCV `DICT_4X4_50` for this candidate, using marker IDs 0..39
for reusable printed card numbers 01..40. Do not invent a new dictionary or
encode a student's identity. Its small payload supports large modules on a
96 mm marker. This is an engineering candidate, not a proven classroom choice.
The remaining ten dictionary IDs are unused; a future scanner must reject IDs
outside its configured card set.

OpenCV's [4.10 marker tutorial](https://docs.opencv.org/4.10.0/d5/dae/tutorial_aruco_detection.html)
defines marker IDs as dictionary indexes and describes generation and detection.
Use its `generateImageMarker` and `ArucoDetector` APIs through pinned
`opencv-python-headless==4.10.0.84`. The first golden codeword in the test is
independently specified from the [upstream dictionary table](https://github.com/opencv/opencv/blob/4.10.0/modules/objdetect/src/aruco/predefined_dictionaries.hpp),
not calculated by the generator under test.

Alternatives considered: AprilTag 36h11 and larger ArUco payloads offer different
coding/detection tradeoffs, but require more modules at the same physical size.
No distance or error-rate advantage is claimed for this choice. Compare families
later if A3-A7 evidence warrants it; changing the family requires a new candidate
version and reprinting, not silent reassignment of these cards.

The [OpenCV license page](https://opencv.org/license/) identifies versions 4.5+
as Apache-2.0; the dictionary source references the project license. No library
binaries or dictionary source tables are redistributed here; dependencies are
installed separately with their license notices. Repository LICENSE is unchanged.
Before packaging Android native libraries, review the exact distribution's
third-party notices as well. OpenCV 4.10 provides the ArUco C++ API, compatible
with the initial OpenCV direction; Android ABI packaging, CameraX bridging,
device support, and offline app launch have not been built or verified in A1.
No Android runtime version is frozen by this desktop generator.

## Layout and use

The [printing guide](../../cards/README.md) is authoritative for commands,
dimensions, and the physical orientation legend. Layout version `ares-a1-v1`
uses A4 pages, 180 mm cut cards, 96 mm markers, 16 mm modules, and at least a
16 mm white margin. The code and black border are vector rectangles. A, B, C,
and D appear on the top, right, bottom, and left edges of the canonical front.
Each letter becomes upright when that edge is held at the top. Retained corners
repeat the card number; no card contains PII. The sample is four pages for
numbers 01, 02, 20, 40; the default generator produces all 40 pages.

## Automated and visual evidence

Validated on Windows with Python 3.12.14, the pinned requirements, OpenCV 4.10.0,
ReportLab 4.2.5, and Poppler 26.07.0. `unittest` suite: 7 tests passed. Independent
100 dpi PDF rasterization: 40 cards x 4 rotations = 160 correct single-ID reads,
zero wrong/additional IDs in those synthetic cases, canonical corner order
preserved. White margins, marker size, page dimensions, labels, determinism,
sample inventory/hash, invalid inputs, and overwrite protection passed.

All four sample pages were rendered and visually inspected for clear labels,
marker orientation, whitespace, cutting boundaries, and readable instructions.
Poppler emitted missing Symbol/ArialUnicode fallback-font warnings; the sample
uses ASCII Helvetica labels and rendered correctly. Physical print measurements
and camera reads have not been performed. The synthetic result is not evidence
of classroom error rates, blur/occlusion performance, or 30-40 simultaneous reads.

## Physical print/read checklist - pending hardware

Record a batch identifier, printer/driver, paper, scale settings, print date,
measured scale bar/marker/card sizes, and a pass/fail for each item below. Use
only synthetic card tokens and independently recorded expected IDs/answers.

1. Print the four-page sample at Actual size. Measure against the guide's
   tolerances; inspect sharp black edges, full white margins, and no bleed-through.
2. Cut and hold each card with A, B, C, and D at the top. A second person records
   the visible answer and card number as ground truth. Check that each letter
   is upright and fingers do not enter the clear white margin.
3. With an independent OpenCV/ArUco test reader configured for `DICT_4X4_50`,
   check expected marker IDs 0, 1, 19, and 39 through all four orientations.
   Record reader/version, device, lighting, distance, misses, wrong IDs, and
   extra IDs. No reader app is supplied in A1; do not claim this step completed.
4. Repeat representative prints if using a different printer, photocopying,
   ink-saving mode, paper, or lamination. Quarantine damaged or incorrectly
   scaled batches rather than correcting their identities by guesswork.

No physical results are currently recorded. A2-A7 remain separate milestones;
do not start camera preview, answer inference, temporal confirmation, roster
coverage, or backend integration as part of this delivery. R02 has a documented
A1 candidate only; R03 acceptance thresholds and shared contract review remain
open. No Track B or shared-contract files were changed.
