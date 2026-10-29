# ARES Quiz Tracking System

Offline classroom quizzes and longitudinal assessment for rural Kenyan schools. The school Ubuntu/nginx ARES server is normally available at `http://ares.local`; classroom activities must work without Internet access.

This application lives entirely under `quiz-tracker/` within `markknit/ares-tracking-system`. Preserve root files, the existing MIT license, and any unrelated usage-tracking components.

## Start here

- [Contributor rules](AGENTS.md)
- [Status and handoff](STATUS.md)
- [Architecture](docs/architecture/overview.md)
- [Domain concepts](docs/contracts/domain-concepts.md)
- [Provisional observation contract](shared/contracts/observation-v0.1.md)
- [Track A plan](docs/track-a-scanner/plan.md)
- [Track B plan](docs/track-b-assessment/plan.md)
- [Unresolved requirements](docs/requirements.md)
- [Windows workflow](docs/windows-setup.md)
- [Decision record](docs/decisions/0001-foundation.md)

## Current boundary

Track A A1 is authorized: see the [card generator and printing guide](cards/README.md). Stop before A2. Android, server, database, web UI, and reporting implementation remain unstarted. B1 remains gated. No REST/OpenAPI or persistence schema is approved.

Future paths are reserved, not created empty: `scanner-android/`, `scanner-windows/`, `assessment-server/`, `admin-web/`, `reporting/`, and `tests/`. A1 tests live within `cards/`. Add other paths only when their milestone is authorized.
