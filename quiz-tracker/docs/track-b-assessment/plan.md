# Track B — Assessment and reporting

Goal: evaluate and design offline school registration, teacher/student management, classes/subjects, academic periods, historical enrollment, quizzes, sessions, responses, longitudinal reporting, privacy, backup, and data integrity.

Track B owns `assessment-server/`, `admin-web/`, `reporting/`, and this documentation directory. It must validate assessment behavior using simulated/manual input independently of camera capture.

| Milestone | Deliverable and review evidence |
| --- | --- |
| B1 | Requirements and conceptual model with school workflows, roles, data relationships, and unresolved decisions. |
| B2 | Lifecycle specification for registration, transfers, class changes, period rollover, enrollment history, and reusable card assignment. |
| B3 | Quiz/version/session/response semantics including attempts, missingness, duplicate handling, correction audit, and imports. |
| B4 | Reporting framework: denominators, coverage, topic/class/student indicators, comparability limits, privacy, and synthetic examples. |
| B5 | Evidence-backed build-versus-integrate evaluation of existing open-source platforms and a hybrid option. |
| B6 | Architecture recommendation with tradeoffs, operating costs, deployment, recovery, and migration plan; stop for review. |
| B7 | Authorized simulated/manual response prototype demonstrating reviewed lifecycle and integrity rules. |

## B1 handoff

[B1 requirements and conceptual model](b1-requirements-conceptual-model.md) is complete as documentation for review on 2026-10-28 under explicit project-lead authorization. See [current status](../../STATUS.md) for the verified worktree and scope. Stop before B2; shared contracts remain provisional and unchanged. No backend has been implemented and no platform selected.

## B5 evaluation method

Identify a current shortlist from official project sources at B5; no platform is selected now. Record source URLs, review date, license/version, maintenance status, and reproducible local feasibility evidence. Compare complete custom build, integration, and hybrid approaches using the same workflows and synthetic data.

Evaluate Internet-free authentication and classroom operation; Ubuntu/nginx fit and resource needs; enrollment history; immutable quiz versions; response import/extension boundaries; idempotency/audit; reporting/export portability; privacy/access control; backup/restore; accessibility; maintenance/security updates; licensing; and migration/lock-in. Treat classroom Internet dependence or an unworkable response boundary as blockers. Record total maintenance effort and unresolved gaps rather than assuming custom development is cheaper.

Reports must distinguish missing/absent/unanswered/incorrect, show denominator and coverage, and avoid unsupported comparisons across different quiz versions or populations. Do not infer teacher effectiveness from raw student quiz scores.

Gate: foundation review before B1. B1–B6 are analysis/design milestones, not authorization for a backend. Do not begin major backend implementation or B7 before B5/B6 review. Integration additionally requires independently reliable Track A and reviewed shared contracts.
