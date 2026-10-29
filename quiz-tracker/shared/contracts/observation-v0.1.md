# Capture observation concept v0.1 — PROVISIONAL

Review status: unapproved. No transport, REST endpoint, serialization, or exact field types are frozen. This is the sole provisional observation definition; domain rationale lives in [domain concepts](../../docs/contracts/domain-concepts.md).

| Information | Intended purpose |
| --- | --- |
| Observation identity | Offline-generated stable retry/deduplication key. |
| Capture method | Provisional adapter name; initially `card_scan`. |
| Card token and marker family/version | Identify reusable physical marker without student PII. |
| Candidate answer | A/B/C/D when sufficiently supported; unresolved otherwise. |
| Session/question context | Intended capture context; validation and stale-context handling required. |
| Device and capture-run identity | Separate simultaneous devices and scan runs without exposing student identity. |
| Capture time and local sequence | Diagnostic ordering; wall clocks may be wrong. |
| Recognition metadata | Confirmation state, frame support, algorithm/version, uncertainty reason; confidence scores require calibration. |

Student identity must not be inferred by the scanner from card number alone. Assessment resolution uses the session roster and valid card assignment to produce a logical response. Do not store classroom images by default; any diagnostic image retention needs a privacy decision.

Future synthetic acceptance cases: exact retry, conflicting retry, repeated frames, answer change, reused card across classes/periods, unknown card, overlapping assignment, stale question, device restart, and disconnected delivery. Define acknowledgements and durable delivery before connecting either track.
