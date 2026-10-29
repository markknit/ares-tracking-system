# Architecture overview

## Context and boundaries

The school LAN is the classroom operating environment. The existing Ubuntu/nginx ARES server normally answers at `http://ares.local`. Route placement, authentication, packaging, storage, and deployment remain decisions for review; do not change the existing ARES image or unrelated services during foundation work.

Track A captures marker observations on Android. Track B manages assessment identity, enrollment, sessions, responses, and reporting, potentially by integrating an existing open-source platform. Either track must be testable independently using synthetic fixtures or manual input.

## Logical flow

1. A capture adapter produces an observation: reusable card token, candidate answer, and capture context.
2. The assessment boundary validates session, question version, assignment validity, and observation identity.
3. Resolution associates the card with exactly one active enrollment in that session context. Missing or ambiguous assignments are held for review, never guessed.
4. A validated logical response records enrollment, session, question/version, answer, provenance, and audit history.
5. Reporting reads validated responses with coverage and missing-data context.

Provisional adapters are `card_scan`, `manual`, `browser`, `ble_clicker`, and `import`. These are concepts, not a frozen enum or an API promise. Manual and browser entry must preserve the same response semantics without requiring a physical card.

## Integrity boundaries

Keep device observations distinct from authoritative assessment responses. Local durable buffering, retry acknowledgements, transaction boundaries, and recovery behavior must be designed before production capture. Retries must not silently create extra responses. Device time cannot be the sole basis for ordering or identity.

Offline-first does not yet specify whether a scanner must survive loss of school Wi-Fi; resolve this explicitly in requirements. No classroom dependency on cloud authentication, Internet licensing, or online scoring is acceptable.

Privacy review must define roles and minimum data, school isolation, access to exports, retention, deletion, and audit access. Backup design must include restore testing, encryption/key custody, and failure recovery. These are acceptance requirements, not claims of implemented security.

## Review gates

Foundation review precedes A1/B1. Track A classroom feasibility evidence precedes integration commitments. Track B must compare build, integrate, and hybrid options at B5 and present B6 for review before major backend work/B7. Integration requires independently reliable tracks and reviewed, versioned shared contracts.
