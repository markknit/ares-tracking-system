"""A1 print/read checks. These are synthetic checks, not classroom feasibility."""

import hashlib
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import cv2
import numpy as np
from PIL import Image
from pypdf import PdfReader

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import generate_cards as cards


class CardTests(unittest.TestCase):
    def test_card_ids_and_dictionary(self):
        # First codeword from OpenCV 4.10.0 predefined_dictionaries.hpp,
        # DICT_4X4_1000_BYTES first rotation = {181, 50}; DICT_4X4_50
        # uses the first 50 entries (row-major white bits).
        expected = np.array([[1, 0, 1, 1], [0, 1, 0, 1],
                             [0, 0, 1, 1], [0, 0, 1, 0]], dtype=np.uint8) * 255
        np.testing.assert_array_equal(cards.marker_grid(1)[1:-1, 1:-1], expected)
        self.assertEqual(cards.FAMILY, "DICT_4X4_50")
        seen = set()
        for n in range(1, 41):
            grid = cards.marker_grid(n)
            self.assertEqual(grid.shape, (6, 6))
            self.assertEqual(set(np.unique(grid)), {0, 255})
            self.assertFalse(grid[0].any() or grid[-1].any())
            self.assertFalse(grid[:, 0].any() or grid[:, -1].any())
            for turn in range(4):
                key = np.rot90(grid, turn).tobytes()
                self.assertNotIn(key, seen, "Duplicate or rotationally ambiguous marker")
                seen.add(key)

    def test_invalid_and_duplicate_cards(self):
        for value in ([], [0], [41], [-1], [1, 1], [1.0], [True], ["1"]):
            with self.subTest(value=value), self.assertRaises(ValueError):
                cards.pdf_bytes(value)

    def test_reproducible_pdf_and_manifest(self):
        numbers = [1, 2, 20, 40]
        first = cards.pdf_bytes(numbers)
        self.assertEqual(first, cards.pdf_bytes(numbers))
        manifest = cards.manifest(numbers, first)
        self.assertEqual(manifest["pdf_sha256"], hashlib.sha256(first).hexdigest())
        self.assertEqual([c["marker_id"] for c in manifest["cards"]], [0, 1, 19, 39])
        self.assertEqual(manifest["canonical_front_edges"],
                         {"top": "A", "right": "B", "bottom": "C", "left": "D"})

    def test_pdf_dimensions_and_retained_labels(self):
        reader = PdfReader(io.BytesIO(cards.pdf_bytes(range(1, 41))))
        self.assertEqual(len(reader.pages), 40)
        for n, page in enumerate(reader.pages, 1):
            self.assertAlmostEqual(float(page.mediabox.width) * 25.4 / 72, 210, places=3)
            self.assertAlmostEqual(float(page.mediabox.height) * 25.4 / 72, 297, places=3)
            text = page.extract_text()
            self.assertIn(f"CARD {n:02d}", text)
            self.assertIn(f"DICT_4X4_50 ID {n - 1}", text)
            for answer in "ABCD":
                self.assertIn(answer, text.splitlines())
            self.assertIn("50 mm scale check", text)

    def test_cli_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp, redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
            output = Path(tmp) / "nested" / "cards.pdf"
            cards.main(["--cards", "40,1", "--output", str(output)])
            self.assertEqual(output.read_bytes(), cards.pdf_bytes([40, 1]))
            self.assertEqual(len(json.loads(output.with_suffix(".json").read_text())["cards"]), 2)
            before = output.read_bytes()
            with self.assertRaises(SystemExit):
                cards.main(["--output", str(output)])
            self.assertEqual(output.read_bytes(), before)
            for bad in ("0", "41", "1,1", "", "A", "1,"):
                with self.subTest(bad=bad), self.assertRaises(SystemExit):
                    cards.main(["--cards", bad, "--output", str(Path(tmp) / "new.pdf")])
            # Also refuse an existing JSON sidecar even when no PDF exists.
            output.unlink()
            with self.assertRaises(SystemExit):
                cards.main(["--output", str(output)])
            with self.assertRaises(SystemExit):
                cards.main(["--output", str(Path(tmp) / "bad.txt")])

    def test_committed_sample_matches_generator(self):
        sample = Path(cards.__file__).parent / "output" / "pdf" / "a1-test-cards.pdf"
        pdf = cards.pdf_bytes([1, 2, 20, 40])
        self.assertEqual(sample.read_bytes(), pdf)
        self.assertEqual(json.loads(sample.with_suffix(".json").read_text()),
                         cards.manifest([1, 2, 20, 40], pdf))


class RenderedPdfTests(unittest.TestCase):
    def test_all_40_printed_markers_four_rotations_and_quiet_zones(self):
        # Require an independent PDF renderer. Missing tools must fail this
        # evidence check rather than silently turn it into a passing skip.
        renderer = os.environ.get("PDFTOPPM") or shutil.which("pdftoppm")
        self.assertTrue(renderer, "Install Poppler or set PDFTOPPM to pdftoppm")
        detector = cv2.aruco.ArucoDetector(
            cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50),
            cv2.aruco.DetectorParameters(),
        )
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / "all.pdf"
            pdf.write_bytes(cards.pdf_bytes(range(1, 41)))
            subprocess.run([renderer, "-r", "100", "-gray", "-png", str(pdf),
                            str(Path(tmp) / "page")], check=True, capture_output=True)
            pages = sorted(Path(tmp).glob("page-*.png"))
            self.assertEqual(len(pages), 40)
            for n, path in enumerate(pages, 1):
                image = np.array(Image.open(path).convert("L"))
                # Whole-page detection catches surrounding text/labels as well.
                for turn in range(4):
                    rotated = np.ascontiguousarray(np.rot90(image, turn))
                    corners, ids, _ = detector.detectMarkers(rotated)
                    with self.subTest(card=n, quarter_turn_ccw=turn):
                        self.assertIsNotNone(ids)
                        self.assertEqual(ids.flatten().tolist(), [n - 1])
                        # Original top-left corner should follow this rotation;
                        # confirms the PDF did not reflect or rotate the codeword.
                        x = 57 / 25.4 * 100
                        y = (297 - 198) / 25.4 * 100
                        h, w = image.shape
                        expected = ((x, y), (y, w - 1 - x),
                                    (w - 1 - x, h - 1 - y), (h - 1 - y, x))[turn]
                        np.testing.assert_allclose(corners[0][0][0], expected, atol=2)
                        # Measure detected black-square edges, not an expected crop.
                        points = corners[0][0]
                        lengths_mm = np.linalg.norm(points - np.roll(points, -1, axis=0), axis=1) * 25.4 / 100
                        np.testing.assert_allclose(lengths_mm, [96] * 4, atol=0.51)
                # Four white bands: marker at (57,102)..(153,198) in PDF mm.
                # Inset 0.5 mm excludes antialiasing at band boundaries.
                for x0, y0, x1, y1 in ((41.5, 86.5, 56.5, 213.5),
                                          (153.5, 86.5, 168.5, 213.5),
                                          (57.5, 86.5, 152.5, 101.5),
                                          (57.5, 198.5, 152.5, 213.5)):
                    left, right = round(x0 * 100 / 25.4), round(x1 * 100 / 25.4)
                    top = round((297 - y1) * 100 / 25.4)
                    bottom = round((297 - y0) * 100 / 25.4)
                    self.assertEqual(int(image[top:bottom, left:right].min()), 255)


if __name__ == "__main__":
    unittest.main(verbosity=2)
