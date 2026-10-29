# Project operating rules

- Offline-first operation is mandatory. Classroom activities must not depend on Internet access; preserve school Wi-Fi and `ares.local` behavior.
- Preserve existing repository files and the MIT license. Keep quiz work under `quiz-tracker/`; do not overwrite unrelated tracking functionality.
- Track A owns `cards/`, `scanner-android/`, and `docs/track-a-scanner/`. Track B owns `assessment-server/`, `admin-web/`, `reporting/`, and `docs/track-b-assessment/`.
- Use separate branches and worktrees. `scanner-windows/` is reserved, not an initial implementation commitment; assign its ownership before work.
- Shared contracts in `shared/contracts/` and domain documentation in `docs/contracts/` are centrally reviewed. Neither track may change an approved contract unilaterally. Record review by representatives of both tracks before approval.
- Use small, testable milestones. Record important architectural decisions in `docs/decisions/` and update `STATUS.md` for handoff.
- Run applicable tests/checks before completing milestones. For documentation, validate links, whitespace, scope, and repository preservation. For implementation, record behavioral test evidence and limitations.
- Make a Git commit after each major completed milestone. Stage explicit paths, review the staged diff, and respect any no-push instruction.
- Never commit credentials, secrets, signing keys, build artifacts, or real student records. Use synthetic records in development and tests.
- Minimize personally identifiable student data (PII). Never encode student names or other PII in response markers. A card number is a reusable token, not `student_id`.
- Give special attention to student privacy and data integrity: access control, auditability, retention, backup, restore, and correct enrollment resolution.
- Do not infer teacher effectiveness from raw student quiz scores.
- A missed card is preferable to an incorrect card/answer assignment. Do not guess uncertain observations.
- Stop before A1 or B1 until foundation review. Stop after A7 feasibility evidence before integration commitments. Stop after B5/B6 for architecture review before major backend implementation or B7. Stop before integration until each track is independently reliable and the shared contract is reviewed.
