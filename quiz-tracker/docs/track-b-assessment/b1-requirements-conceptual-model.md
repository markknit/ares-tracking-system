# B1: Requirements and conceptual model

Date: 2026-10-28. Status: B1 documentation complete for review; proposals are not stakeholder approval or an implementation specification.

## Authority, sources, and boundary

The project lead explicitly authorized B1 only on branch `track-b-assessment`: document requirements and the conceptual model, commit, and stop before B2. This supersedes the foundation's pending Track B start gate for B1 only. Track A, shared contracts, and later milestone gates are unchanged.

Sources: [project rules](../../AGENTS.md), [Track B plan](plan.md), [requirements register](../requirements.md), [architecture](../architecture/overview.md), [draft domain concepts](../contracts/domain-concepts.md), [provisional observation contract](../../shared/contracts/observation-v0.1.md), and [foundation decision](../decisions/0001-foundation.md). This document develops Track B requirements consistent with those sources; it does not amend or approve either shared document. Existing R01-R15 remain centrally maintained; the B1 questions below refine their Track B implications without closing them.

B1 describes school workflows, roles, conceptual relationships, integrity/privacy requirements, and questions for review. It selects no platform, database, schema, endpoints, identifier format, authentication mechanism, or deployment configuration. B2 specifies lifecycle transitions; B3 specifies response/attempt rules; B4 specifies reporting formulas and examples; B5/B6 evaluate architecture before any authorized B7 prototype. No backend, UI, report engine, capture integration, or production data collection is authorized here.

## Operating requirements

| ID | Requirement and review expectation |
| --- | --- |
| B1-01 | Registration, school-local authentication, roster preparation, quiz delivery, response entry, and reporting must work without Internet. Later feasibility evidence must exercise these workflows with external connectivity disabled. Preserve school LAN and `ares.local` behavior. |
| B1-02 | Track B must be independently verifiable using synthetic manual/simulated responses. A physical card or working camera is not a prerequisite for a logical response. |
| B1-03 | Each school is an explicit authorization and data-isolation boundary, including reports, imports, exports, audit records, and backups. Access across schools requires a separately reviewed authority and purpose. |
| B1-04 | Student identity survives name, class, academic-period, and card changes within its agreed identity scope. Identity scope across schools remains open; do not merge people by matching names or school numbers. |
| B1-05 | Preserve historical enrollments, assignment context, published quiz versions, session rosters, response provenance, and attributed corrections so later changes do not silently reinterpret earlier results. |
| B1-06 | Reports must expose population, assessment/version, time/period, denominator, coverage, missing-data states, and limits on comparison. Raw scores must not be used to infer teacher effectiveness. |
| B1-07 | School staff must be able to correct mistakes through authorized, attributable review. Original evidence and prior interpretation must remain traceable subject to reviewed retention/deletion requirements. |
| B1-08 | Minimize personal data; protect local access, exports, backups, and diagnostics. Restore and retention policies must be reviewed before real records are collected. |

Internet loss and school Wi-Fi/server loss are different conditions. Offline-first requires the former; device buffering, acknowledgements, and reconciliation during LAN loss remain unresolved in R07/R08. B1 makes no disconnected-device durability claim.

## Proposed actors and authority

These are conceptual responsibilities to review with schools, not approved role names or an access-control implementation. One person may perform several responsibilities only through explicit authorization.

| Responsibility | Necessary work | Proposed access boundary and question |
| --- | --- | --- |
| School administrator/registrar | Register school actors, maintain class/period records, reconcile student registration and enrollment | School scope; distinguish roster administration from permission to alter assessment evidence. Who approves duplicates/transfers? |
| Teacher/session operator | Prepare quizzes and assigned-class rosters, deliver sessions, enter/review responses | Authorized teaching groups and sessions; no implied school-wide student access. Who may substitute for another teacher? |
| Assessment reviewer | Review unresolved responses, approve corrections, inspect provenance | Explicit school/session scope; correction and scoring authority must be defined in B3. |
| School reporting user | Inspect permitted student/class history and export approved results | Purpose-based access; identifiable student reports and aggregates need different permissions. |
| ARES operator | Maintain the local service, recovery, accounts, and backups | Technical maintenance is not automatic authority to browse educational records; define exceptional access and audit. |
| Student | Subject of enrollment and assessment records | No student login, self-service correction, or direct report access is assumed. School review must decide these needs. |

Access revocation must prevent future unauthorized access while retaining historical teacher/session attribution. Administrative changes, exports, corrections, and privileged access need auditability. Offline account recovery and initial administrator provisioning require review rather than a cloud dependency.

## School workflows to validate

1. Establish a school and authorized staff locally; define academic periods, subjects, and teaching groups. Review what identifies a school and who authorizes its creation.
2. Register a student using minimum necessary attributes; search/review potential duplicates rather than assuming a matching name is the same person. Enroll the student in the relevant teaching group and period with a validity interval.
3. Assign a reusable card in the intended roster context when cards are used. Confirm that every token resolves unambiguously before accepting captured evidence. Manual entry identifies the intended enrollment without requiring a token.
4. Prepare a quiz, publish a fixed content version, and open a delivery session against a specific roster and question context. Record teacher responsibility without treating the teacher as owner of student identity.
5. Receive manual/simulated evidence; check school, enrollment, roster, quiz/question version, and provenance before creating a logical response. Hold uncertain or conflicting evidence for authorized review.
6. Review session coverage and unresolved records, then expose results with appropriate missingness and scoring context. Detailed open/close/reopen behavior is a B3 decision.
7. Later inspect the student's or class's history using the original assessment context even after class, teacher, card, or period changes. Authorized corrections must be traceable; reports must identify their revision/as-of context.

Transfers, rollover, withdrawal, re-entry, reassignment, and restore are required use cases for later specifications. This sequence does not prescribe their state transitions or operational procedures (B2/B6).

## Conceptual entities and relationships

The following are semantic relationships, not tables, field lists, or mandatory storage structures. Internal identities must be stable, opaque, and obtainable offline; generation, namespace, import collision, and cross-school rules await review. Names and local registration numbers are attributes, not reliable unique keys.

| Concept | Meaning, relationships, and history required |
| --- | --- |
| School | Administrative scope for teachers, groups, academic periods, student records, sessions, and access. A school has many such records. The scope of the underlying person identity across schools is unresolved. |
| Teacher | Authorized school actor with teaching responsibilities over time. A teacher may serve multiple groups; a group may have multiple or changing teachers. Keep historical responsibility without replacing the teacher recorded for an earlier session. Multi-school affiliation needs review. |
| Academic period | School-defined time interval used by groups, enrollments, and reporting. Period naming, nesting, and overlap rules need school input. A period change does not erase prior memberships. |
| Class/teaching group | School-scoped teaching context associated with subject/course and period information. A group has many enrollments and sessions. Whether a homeroom class and subject course are distinct entities is open under R04; avoid assuming one teacher or one subject per class. |
| Student | Stable internal identity with minimum school-authorized attributes. A student has multiple enrollments over time and potentially concurrently in different teaching groups. Identity is independent of enrollment, card token, name, and scores. |
| Enrollment | Student membership in a specific group and academic-period context over a validity interval. Each enrollment refers to one student and one group; historical responses refer to that enrollment. Interval boundaries and legitimate overlapping memberships are B2 questions. |
| Card assignment | Association of a reusable token with one enrollment in a bounded roster/context and validity interval. An enrollment may have successive assignments; a token may be reused later or in a separate unambiguous context. Token identity includes the applicable marker family/version context; a printed number alone need not be globally unique. |
| Quiz | Continuing assessment identity, separate from each immutable published content version and each delivery session. A quiz can have multiple versions and be delivered in multiple sessions. School ownership and permission to reuse/share quiz content need review. |
| Quiz version and question version | Published content snapshot including prompts, available choices, answer/scoring definitions, and topic metadata as applicable. A quiz version contains version-bound questions. Editing content or scoring must not silently reinterpret old responses; correction/rescoring policy belongs to B3. |
| Quiz session | One delivery instance linking a school, quiz version, responsible staff, intended roster/enrollments, and question context. A version can have many sessions. Preserve roster membership and assignment-resolution context used at delivery; physical snapshot versus historical references is an architecture decision. Multi-class sessions need review. |
| Response | Validated logical answer tied to one enrollment, one session, and its question version, with source/provenance and interpretation history. An enrollment can have many responses across questions/sessions. Multiple candidates for one enrollment/session/question require the B3 attempt/change policy; B1 does not assume one submission or last-write-wins. |
| Observation/input evidence | Source evidence from an adapter or manual/import operation, distinct from a validated response. It may remain unresolved or be duplicate/conflicting evidence. A response must retain traceable source context; precise cardinalities and retention are B3/privacy decisions. |
| Correction/audit event | Attributed record of a change/review, its reason, affected context, and prior/new interpretation. Must support tracing enrollment corrections as well as response changes without silently reassigning historical results. |
| Historical report | Authorized interpretation of responses plus roster, missingness, version/scoring, topic, and period context. It is a derived view, not a new source of student identity. A saved/exported report needs scope, generation/as-of context, and interpretation metadata sufficient to explain it later. |

The central relationship is `student -> enrollment -> session roster participation -> response`. Card resolution follows `session context + token + valid assignment -> exactly one roster enrollment`; it does not follow `card number -> student`. Reporting follows the resolved historical enrollment and version context, rather than joining an old token to today's roster.

## Data-integrity requirements

| ID | Required invariant | Later evidence needed |
| --- | --- | --- |
| I01 | Linked school, group, enrollment, session, and response context must agree. Missing/foreign references cannot produce accepted responses or leak records. | Synthetic cross-school and broken-reference cases; B2/B3 semantics and B7 validation. |
| I02 | A session's roster and assessment context must remain explainable after edits. Roster corrections must not quietly move past responses to another person. | Mid-session roster edit, transfer, and duplicate-student correction review in B2/B3. |
| I03 | Within the applicable scan roster/context, a token must resolve to exactly one eligible enrollment. Unknown, expired, overlapping, or ambiguous assignments remain unresolved. | Reused token across periods/classes and overlapping/expired assignment cases; shared review under R05. |
| I04 | Published version history and original response provenance must remain traceable. Scoring/content changes need explicit version/correction treatment. | Explain a past result before/after a later content or scoring correction (B3/B4). |
| I05 | Exact delivery retries must not create additional logical responses. Same evidence identity with different content is a conflict; repeated frames are not automatically submissions. | Retry/conflict/restart examples in B3; identifier and delivery guarantees await R07/R08/shared review. |
| I06 | Uncertain answers, stale context, and competing evidence must never be guessed into an accepted student/answer pairing. Wall time alone cannot prove ordering or assignment validity. | Stale question, wrong device clock, concurrent input, and manual correction cases in B3. |
| I07 | Distinguish absent, missing capture, unanswered, incorrect, rejected, and unresolved evidence. Absence must not manufacture a response; missing evidence must not automatically become a wrong answer. | B3 state definitions and B4 denominator rules, including partial sessions. |
| I08 | Imports and corrections need source attribution, duplicate/conflict review, and authorization. Names, card numbers, and device timestamps cannot serve as sole identity evidence. | Synthetic import collisions and proposed correction approval workflow in B2/B3. |
| I09 | Durable accepted data and its audit context must be recoverable together. Partial failure or restore must not silently separate responses from their roster/version/provenance. | Failure/recovery boundaries and tested restore objectives in B6/B7; no durability mechanism selected here. |

An operator must be able to see why evidence was held and who may resolve it. Any policy choosing among attempts, late answers, simultaneous edits, or competing corrections remains open; this document deliberately provides no default winner.

## Historical reporting requirements

- Support a student's history through enrollment/period changes and a group's history through changing membership and teachers, within authorized identity scope. Cross-school linkage and cohort equivalence require explicit review.
- Identify assessment and question versions, scoring interpretation, subject/topic context, session dates/periods, population selection, and relevant report revision/as-of context. Retain enough context to explain a prior report after a correction; storage/reproduction methods remain undecided.
- Show denominator and coverage alongside any score or trend. Separate roster eligibility, attendance information, accepted responses, and unresolved/missing states. B4 will define the actual formulas and treatment of each state; B1 approves no aggregate metric.
- Make exclusions and partial sessions visible. Distinguish an observed zero from missing data and show corrections/rescoring when they affect interpretation.
- Do not assume equal difficulty across versions or equivalent populations across periods/classes. Flag limits rather than presenting unsupported learning gains or teacher rankings. Raw quiz scores cannot establish teacher effectiveness.
- Restrict identifiable reports and exports to authorized purposes. Aggregates can still identify children in small groups; threshold/suppression and export policy need privacy review.

## Privacy and operational protection

Use synthetic records only for development and review. The following are requirements awaiting school governance and architecture validation, not implemented protections or claims of legal compliance.

| Area | Requirement / decision needed |
| --- | --- |
| Minimum data | Justify every personal attribute needed for registration, matching, and reporting. No assumption that birth date, national identifier, guardian contacts, or demographic attributes are necessary. Internal opaque IDs are still sensitive when linkable. |
| Markers and devices | Markers contain no names or other student PII; token numbers remain reusable. Do not give a capture adapter a student directory merely to resolve cards. Do not store classroom imagery by default; exceptional diagnostics need purpose, authorization, restricted access, and deletion limits. |
| Access and school isolation | Review least-privilege school/group/session access, local authentication, revocation, offline recovery, and privileged operator access. Protect reports, search results, logs, and exports as well as ordinary records. |
| Audit | Attribute roster/role changes, corrections, imports, exports, and privileged actions; define audit readers and retention. Avoid copying unnecessary PII into diagnostic/audit text. |
| Retention and deletion | School authority must define purposes, consent or other applicable basis, retention periods, correction/access requests, and withdrawal/deletion rules before real data collection. Resolve the tension between historical traceability and permitted deletion, including exports, audit records, and backups. |
| Backup and recovery | Define backup frequency, access, encryption/key custody, offline restore, loss/recovery objectives, and restore verification. Address lost devices, stolen media, and reintroduction of deleted records after restore. |
| Export/sharing | Define who may export which records, recipients, minimal fields, safe transfer, and responsibility for retained copies. Internet-free operation does not imply unrestricted local-network trust. |

## Unresolved requirements and review ownership

Owners are proposed responsibilities, not recorded reviewer assignments. Nothing here resolves a shared requirement or approves a contract.

| B1 question | Existing register | Proposed reviewer | Resolve at/before |
| --- | --- | --- | --- |
| Q01: What are class, subject course, homeroom, academic period, and valid simultaneous enrollments? What student identity is retained on transfer/re-entry, including between schools? | R04 | Track B + school registrars/teachers | B2 |
| Q02: Who may create a school, register staff/students, delegate classes, substitute, and correct roster identity? How is initial/recovery access authorized offline? | R04/R09 | School authority + Track B | B2 role/lifecycle review; before data collection |
| Q03: What bounds an assignment, who supplies the authoritative session roster, and when may a token be reused/replaced? How are boundary times or stale rosters resolved? | R05/R07 | Both tracks + schools | B2/B3 and contract review |
| Q04: Are sessions single-class, multi-class, or individual? How are roster edits, opening/closing, interruptions, and question/version selection governed? | R04/R06 | Track B + teachers | B2/B3 |
| Q05: Which attempts count, and how are answer changes, lateness, absence, partial sessions, corrections, and rescoring approved? | R06 | Track B + teachers | B3 |
| Q06: What is the offline ID/namespace model, retry/conflict behavior, concurrency authority, clock-drift handling, and restart/import reconciliation? | R07/R08/R14 | Both tracks + ARES operations | B3 boundary analysis; shared contract approval before integration |
| Q07: Which data and reporting access are necessary, under whose governance, for how long, and with what deletion/export/diagnostic rules? | R09 | School authority + Track B | Before real data collection; reporting policies in B4 |
| Q08: Which indicators, topic taxonomy, population denominators, small-group controls, and comparability evidence are acceptable? | R11/R09 | Educators + Track B + school authority | B4 |
| Q09: Who owns/publishes quiz content, may share it across schools, and authorizes version or scoring corrections? | R06/R09/R11 | Teachers + school authority | B3/B4 |
| Q10: What recovery objectives, backup/key responsibilities, resource budget, and migration requirements must the selected approach meet? | R10/R12/R13 | ARES operations + Track B + project lead | B5/B6 review |

The current user request authorizes producing and committing B1; it does not record both-track contract approval, general R01 closure, B2 authorization, platform selection, or permission to collect real student data.

## B1 review checklist and handoff

The deliverable covers every requested core entity in the conceptual table, actors and school workflows, integrity invariants I01-I09, privacy requirements, reporting needs, and open questions with proposed reviewers and later gates. These are document-review criteria; no runtime behavior has been tested or implemented.

Future school review should walk through these synthetic cases when refining B2-B4:

- One student changes class and card between periods: earlier results retain the original enrollment and version context.
- Two different students share a name, and a token is reused in a later class: identity and historical reporting do not follow the name or current token owner.
- A token is ambiguous in one session, or evidence names another school's context: hold it without attributing a student response.
- A retry, conflicting retry, manual answer change, and quiz correction arrive: preserve evidence without silently selecting a winner or rewriting the original version.
- A rostered student is absent while another has no capture: later reports distinguish these situations and disclose coverage.
- A revoked teacher requests an export or a restored backup contains older permissions/data: access and recovery policy must handle the case before production use.

Stop after this B1 commit. B2 lifecycle specification, B3 response policy, B4 formulas, B5/B6 platform/architecture work, and B7 implementation remain unstarted. Shared contracts remain provisional and unchanged; Track A is untouched.
