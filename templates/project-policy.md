# Project policy

This file records settled project decisions. Replace every placeholder during
onboarding. An unanswered required decision blocks dependent work. Do not infer
permission from a blank field.

## Adoption and authority

| Decision | Recorded answer |
| --- | --- |
| Project purpose and boundaries | {{PURPOSE_AND_NON_GOALS}} |
| Policy owner and authorized decision makers | {{POLICY_OWNER}} |
| Agent Temper source and immutable revision | {{SOURCE_URL_AND_COMMIT}} |
| Local framework bundle and adoption record | {{FRAMEWORK_PATH}}/SOURCE.md |
| Selected tool and practice profiles | {{PROFILE_PATHS_AND_APPLICABILITY_OR_NONE}} |
| Local extensions and label/default mappings | {{CANONICAL_PATHS_AND_MAPPINGS_OR_NONE}} |
| Product and architecture references | {{CONTRACT_DOCUMENT_PATHS}} |
| Policy change procedure | {{WHO_APPROVES_AND_HOW_DECISIONS_ARE_RECORDED}} |

Apply the pinned method and explicitly selected profiles together with this policy.
A copied profile is not selected merely because its file exists. Record extension
source identities, compatibility, verification, and change authority here or in a
linked local record. Project choices fill decisions delegated by the method.
Resolve contradictions with the owner before dependent work. Record a deliberate scoped exception when
departing from an adopted requirement; never invent an undocumented override.

## Technical constraints

| Decision | Recorded answer |
| --- | --- |
| Implementation languages and toolchains | {{LANGUAGES_VERSIONS_AND_VERSION_SOURCE}} |
| Supported platforms and compatibility | {{PLATFORMS_AND_SUPPORT_BOUNDARIES}} |
| Dependency and new-language approval | {{DEPENDENCY_AND_STACK_POLICY}} |
| Architecture, security, privacy, and resource limits | {{LIMITS_AND_CANONICAL_REFERENCES}} |
| Public contribution and licensing rules | {{LICENSE_AND_CONTRIBUTION_RULES}} |

## Work and verification

| Decision | Recorded answer |
| --- | --- |
| Sole live work tracker | {{TRACKER_AND_LOCATION}} |
| Priority, readiness, ownership, and dependency rules | {{RULES_OR_PROFILE_REFERENCE}} |
| Milestone completion conditions | {{CAPABILITY_GATES_OR_WHEN_MILESTONES_APPLY}} |
| Behavior specification and test-first requirements | {{VERIFICATION_POLICY_AND_EXCEPTION_PROCESS}} |
| Required checks by change type | {{CHECK_COMMAND_MAP_OR_PATH}} |
| Real-system or manual validation triggers | {{TRIGGERS_AND_REQUIRED_EVIDENCE}} |
| Documentation structure and writing style | {{DOCUMENTATION_POLICY}} |
| Definition of completion | {{ACCEPTANCE_REVIEW_AND_DELIVERY_CONDITIONS}} |

Document executable local commands for setup, focused verification, formatting,
linting, static analysis, tests, build, and documentation validation where they
apply. State why a category does not apply. Record required environment and
external dependencies. Identify which commands CI runs and what cannot run
locally; do not promise local and CI equivalence without checking it.

Where relevant, link a short repository map from the architecture references.
Record maintenance triggers and delegated actions, and link release, recovery,
support, and incident procedures for shipped software. Keep each current pass or
release's scope and evidence in its work item. Product investigations and later
outcome evaluations identify their owner, decision criteria, and trigger there;
this policy records the durable research and data-access authority.

When selecting model routing, record the role configuration paths, model/effort
mapping, unavailable-model fallbacks, resource limits, and change authority here
or in a linked local rule. Keep model configuration outside the pinned framework
bundle. Record runtime verification and evaluation evidence in the adoption work
item; a model choice never changes the authority table below. Omit this guidance
when the project does not use model routing.

## Agent authority

Specify **allowed**, **ask first**, or **prohibited**, with conditions. A tool's
technical access does not itself authorize an action.

| Action | Decision and conditions |
| --- | --- |
| Routine design, code, tests, and documentation within accepted scope | {{IMPLEMENTATION_AUTHORITY}} |
| Create or change work items and milestones | {{TRACKER_AUTHORITY}} |
| Commit, push, and open reviews | {{SOURCE_AND_REVIEW_AUTHORITY}} |
| Required reviewers and independent review triggers | {{REVIEW_REQUIREMENTS}} |
| Integrate or merge accepted changes | {{INTEGRATION_AUTHORITY}} |
| Publish releases and packages | {{RELEASE_AUTHORITY}} |
| Deploy or operate production and external services | {{OPERATIONS_AUTHORITY}} |
| Destructive actions, secrets, spending, and external communication | {{SENSITIVE_ACTION_AUTHORITY}} |

## Exceptions and changes

{{ACTIVE_EXCEPTIONS_OR_NONE}}

Each exception identifies the requirement, narrow scope, reason, approver,
alternative safeguard, and review or expiry condition. Record policy changes in
version control with their rationale and authorizing decision. Keep live work
status in the tracker; this policy is not an execution log.
