# Shared domain concepts — draft

This vocabulary is conceptual and unapproved. It is not a database schema or wire API.

| Concept | Meaning and integrity rule |
| --- | --- |
| School | Administrative and data-isolation boundary; scope identifiers and authorization explicitly. |
| Academic period | Named time interval; retain historical enrollment and assignment context. |
| Teacher | Authorized school actor; roles and registration workflow unresolved. |
| Student | Stable internal identity, independent of names, card numbers, and class membership. |
| Class/course | Teaching group with subject context; class versus course distinction needs review. |
| Enrollment | Student membership in a class/course over a validity interval and academic period. |
| Card assignment | Reusable card token assigned to an enrollment for a bounded context/interval. Prevent overlapping ambiguous assignments within a scan roster. |
| Quiz | Continuing assessment identity. |
| Quiz version | Immutable published content snapshot; edits must not reinterpret past results. |
| Question | Versioned prompt, options, scoring/topic metadata; session binds a specific version. |
| Quiz session | Delivery instance binding roster, quiz version, and active question context. |
| Response | Validated answer associated with enrollment, session, question version, and provenance. |
| Correction/audit event | Attributed change with reason and prior/new state; preserve original evidence. |

## Identifier rules

Use opaque stable internal identifiers generated without Internet access; do not derive identifiers from PII. Choose UUID or another collision-resistant scheme only after review. Define school/device namespaces and import collision handling before implementation. A physical card number is not a student ID. Names and imported school numbers are attributes whose uniqueness cannot be assumed.

## Duplicates, uncertainty, and corrections

An observation identifier supports idempotent retries. Same identifier with different content is a conflict requiring quarantine/review. Repeated frames are capture evidence, not automatically separate submissions. Multiple distinct observations for the same enrollment/session/question require an explicit attempt and answer-change policy; never silently apply last-write-wins.

Unknown cards, ambiguous assignments, uncertain answers, and stale session context must remain unresolved with an explanatory status. Missing, absent, unanswered, incorrect, and rejected observations are distinct states. Do not manufacture a response for an absent student.

Corrections must record actor, reason, event identity, and affected version/context, retaining original provenance. Authorization and whether corrections are append-only are review decisions; silent destructive edits are unacceptable.

## Versioning

Separate quiz/question versions from contract versions. Proposed contract changes require both tracks' review, compatibility notes, migration/replay strategy, and synthetic fixtures. A breaking change needs an explicit new version. Neither this document nor `v0.1` implies contract approval.
