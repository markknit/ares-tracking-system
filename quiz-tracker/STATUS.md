# Project status and handoff

Updated: 2026-10-28. Track A A1 implementation complete under explicit project-lead authorization. Worktree: `C:\Users\MRKni\Dev\ares-tracking-system-scanner`, branch `track-a-scanner`. Foundation commit `cf5590fcce8afb7dcb5526c9df7ad2fba13a3e5a` matched fetched `origin/main` at session start. STOP before A2. B1 remains gated; shared contracts remain unapproved.

## Active threads

| Thread | State | Next action |
| --- | --- | --- |
| Repository inspection | Live clean Track A worktree verified; foundation matches origin/main | Preserve original history and LICENSE |
| Foundation documents | Published at cf5590f; earlier pre-commit narrative below is historical | Retain Track B and integration gates |
| Git checkout and foundation commit | Separate scanner worktree on track-a-scanner | Local A1 milestone commit; Git log is authoritative for SHA; no push requested |
| Track A | A1 generator, tests, documentation, and sample complete | Physical print/read checks pending hardware; stop before A2 |
| Track B | Not started | Foundation review before B1; B5/B6 review before backend/B7 |
| Shared contract | Provisional v0.1, unapproved | Both-track review before integration |

## Inspection baseline

The specified Windows folder was empty, with no `.git`, source files, uncommitted files, control documents, or active handoffs. Git status/remote/branch/log checks therefore failed as not a repository; local ahead/behind status is unavailable.

Connected GitHub inspection verified `markknit/ares-tracking-system`, default branch `main`, containing only `LICENSE` (MIT). Remote HEAD observed: `ac85e73f5ae6a86f5c17d99693d591ba00bffacb` (`Initial commit`). License blob: `80eec6c489f32cd7cba2ff861734d29a8700689e`. No existing applications or quiz structure were present remotely. No remote files or settings were changed.

Both `git ls-remote` and `git clone --branch main https://github.com/markknit/ares-tracking-system.git .` failed to connect to github.com:443. No `git init`, reset, forced checkout, remote commit, or push was performed. The original license remains untouched remotely; a checkout must obtain it from the existing repository.

## Handoff

Current handoff: the user's 2026-10-28 instruction authorizes Track A A1 and its commit only. The clean scanner worktree and fetched foundation supersede the historical checkout/publication instructions below. No CLAUDE.md, WORKFLOW.md, separate HANDOFF file, or project Step 0 block exists. Baseline branch/log/status/fetch checks were run; local main has zero commits missing from this branch. Use this worktree's actual path and branch, not the historical Windows workflow examples. No Track B or shared-contract changes are authorized.

A1 result: [generator/printing guide](cards/README.md), [decision and evidence](docs/track-a-scanner/a1-cards.md), and [four-page sample PDF](cards/output/pdf/a1-test-cards.pdf). Seven automated tests pass, including independent Poppler rasterization and 160 correct single-ID reads (40 cards x four rotations), with canonical corner and white-margin checks. All four sample pages were visually inspected. Physical printer measurements and camera reads are pending, not claimed. Dependencies are desktop-only and pinned; no Android prototype or answer inference exists. To resume, review this evidence and obtain authorization before A2. The provisional observation contract and all Track B files remain unchanged.

### Historical foundation handoff (completed; do not repeat)

Read this file, project rules, architecture, and unresolved requirements. The checkout is now established at `C:\Users\MRKni\OneDrive\ares-tracking-system`, on `main`, with origin `https://github.com/markknit/ares-tracking-system.git`. A separate staging clone verified the original remote history before its Git metadata and LICENSE were moved into this folder. All 11 prepared foundation files were hash-checked and preserved byte-for-byte during that transfer. LICENSE remains blob `80eec6c489f32cd7cba2ff861734d29a8700689e`.

The project lead authorized foundation review, commit, and push on 2026-10-28. Commit exactly `docs(quiz): initialize two-track quiz system` after validation and staged-diff review; review the resulting commit, fetch and check divergence, then push without force. At this pre-commit snapshot publication verification is pending. The final completion report must record the real commit SHA and matching local/remote state; Git history is authoritative for the resulting SHA. Publication does not authorize A1/B1 or approve the provisional shared contract.

After explicit track-start approval, tracks may proceed independently within their documented milestones. No platform, database, API, marker dictionary, or deployment configuration has been selected.

## Session log

- 2026-10-28 (Track A A1): Verified the requested clean branch/worktree, fetched origin, and confirmed foundation cf5590f matches origin/main. Reconciled stale pre-publication status with live Git and explicit A1 authorization. Implemented the offline DICT_4X4_50 vector-PDF candidate, IDs 0..39/card numbers 01..40, versioned layout/inventory, pinned dependencies, seven behavioral tests, print/read checklist, and sample cards 01/02/20/40. Automated checks and visual sample review passed. Physical checks remain pending hardware. Commit this A1 milestone locally; stop before A2. No push, Track B implementation, or shared-contract edit.

- 2026-10-28: Inspected empty Windows folder and verified existing GitHub repository via connector. Prepared documentation only after clone failed. Implementation remains stopped. Documentation validation results are reported in the completion response; no runtime tests apply.

- 2026-10-28 (resume): Live Git HTTPS succeeded outside the sandbox; remote main remained at `ac85e73f5ae6a86f5c17d99693d591ba00bffacb`. Recovered the existing checkout without replacing foundation files or LICENSE. Reviewed documentation and retained every implementation gate. An empty `.foundation-checkout-20261028/` staging directory remains because Windows denied its removal; it contains no files and is outside the staged scope.

## Known issues / lessons

- A card artifact's successful synthetic decode does not establish physical print or classroom performance. Keep pending hardware checks explicit. Desktop generation dependencies do not select an Android package/ABI.
- Worktree Git metadata is outside the scanner writable root; fetch/staging/commit may require approved access to the shared repository metadata. Verify scope before each Git mutation.

- Connected GitHub reads can work while shell Git networking fails. A remote read is not a local checkout or a successful fetch.
- Do not use a separately remembered `ares-quiz-tracker` checkout as this repository's state; the current requested repository and subdirectory are authoritative.
