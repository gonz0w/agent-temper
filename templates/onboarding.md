# Project onboarding questions

Use this guide to fill `project-policy.md`. Read existing project documentation
first. Present known answers with their sources and ask about gaps or conflicts.
Do not maintain a second copy of the settled answers here.

Ask short batches of related questions. Distinguish required policy decisions
from routine choices the owner wants agents to make. Proceed with independent
work while a required answer is pending; do not proceed with dependent work.

## Purpose and adoption

- What should this project deliver, for whom, and what is outside its scope?
- For an uncertain product direction, what evidence supports the need, which
  assumption needs testing, and who decides whether to proceed? Keep the current
  investigation in its work item; a well-understood fix needs no discovery exercise.
- When user benefit needs later evaluation, who owns that evaluation, what signal
  matters, and what event triggers it? What research or data collection is authorized?
- Who can settle policy? How must changes be approved and recorded?
- Which immutable Agent Temper revision and tool or practice profiles will it adopt?
- Which local rules and label/default mappings must remain? Are the selected rules
  compatible, and who may approve updates, exceptions, or removal?
- Which existing product, architecture, security, and privacy contracts apply?
- Does an adopted requirement need a scoped, approved exception?
- Which observed adoption problems belong upstream, and which are local or obsolete?

## Technology and verification

- Which languages, toolchains, platforms, and compatibility promises are required?
- What may agents decide about dependencies or architecture? What needs approval?
- What are the local setup and check commands? Which checks does CI run?
- Where can a new agent trace a user task through the code and its tests? Would a
  short repository map improve the existing architecture references?
- When are TDD, a failing reproduction, integration tests, or manual checks required?
- Which checks need a real system or external service, and what evidence is enough?
- What documentation, naming, licensing, and writing conventions apply?

## Work and authority

- Where is the sole live work tracker? How are priority, readiness, blockers,
  milestones, and ownership represented?
- May agents create work items and propose scope? Which work is authorized to start?
- Which routine implementation choices are delegated?
- If model routing would help, which roles, available models, effort settings,
  resource limits, and fallbacks apply? Who may change them, and how will actual
  routing and completed-work quality be checked? Otherwise leave the profile unselected.
- May agents commit, push, and open reviews? What independent review is required?
- May agents integrate after checks and review, or must they stop for approval?
- Who may publish releases, deploy, access secrets, spend money, or contact others?
- Which actions are prohibited? What are the acceptance and completion gates?
- Which events trigger repository maintenance, and what may an agent resolve?
  For shipped software, where are release, recovery, support, and incident procedures?

## Confirm and preserve

Review the completed policy with the owner through the project's authorized
decision process. Record answers and adoption evidence in version control. Remove
unresolved template placeholders. Record explicit “not applicable” answers with
reasons where appropriate.

Settled decisions remain effective across agents and sessions. Revisit them only
through the recorded change process. An upstream framework release is a proposed
update, not an automatic policy change.
