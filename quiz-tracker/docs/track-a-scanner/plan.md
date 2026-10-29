# Track A — Classroom response capture

Goal: reliably capture approximately 30–40 responses in realistic classrooms using reusable cards. Initial technology direction: Android, Kotlin, CameraX, OpenCV, and ArUco and/or AprilTag. Versions, marker family, and any extra runtime dependency remain unselected.

Track A owns `cards/`, `scanner-android/`, and this documentation directory. Windows scanning is reserved for a later decision. Track A must work against synthetic roster/context fixtures without waiting for a backend.

| Milestone | Deliverable and evidence required |
| --- | --- |
| A1 | Printable marker-card candidate with reproducible marker family/IDs, orientation legend, print dimensions, and print/read checks; no PII. |
| A2 | CameraX preview prototype; verify lifecycle, permissions, supported device behavior, and offline launch. |
| A3 | Marker recognition; measure false IDs and misses across distance, lighting, occlusion, and print quality. |
| A4 | Explicit rotation-to-A/B/C/D mapping; test all orientations and reject ambiguous/skewed poses. |
| A5 | Multi-frame confirmation; evaluate stability, answer changes, duplicate suppression, and uncertainty rejection. |
| A6 | Captured/missing-card interface; show roster coverage and uncertain cards without inventing answers; support explicit recapture. |
| A7 | Classroom-scale evidence for 30–40 cards; record ground truth, false card/answer assignments, misses, capture time, device, distances, and conditions. |

A missed card is preferable to an incorrect card/answer assignment. Accuracy thresholds, confirmation intervals, and acceptable latency must be agreed before declaring feasibility. Test against independently recorded ground truth, not the scanner's own output.

Gate: foundation review before A1. At A7 stop for feasibility review; do not integrate a system whose false assignments or usability are not acceptable. Marker dictionary licensing and Android/OpenCV/AprilTag compatibility must be checked when selecting dependencies. No dependency or marker implementation is included now.
