# Agent instructions

Read this file, the [project policy]({{PROJECT_POLICY_PATH}}), and the adopted
[Agent Temper method]({{FRAMEWORK_PATH}}/METHOD.md) before working. The
[adoption record]({{FRAMEWORK_PATH}}/SOURCE.md) identifies the pinned upstream
revision.

## Work authority

[{{WORK_TRACKER_NAME}}]({{WORK_TRACKER_URL}}) is the sole authority for live work,
priority, dependencies, ownership, and continuation. Follow the
[work profile]({{TRACKER_PROFILE_PATH}}). Read the selected work item and its
discussion before implementation. Work must have a bounded deliverable and
verifiable acceptance criteria.

Record execution discoveries and handoffs in that work item. Keep durable behavior
and decisions in the documentation. Do not create a second backlog or status log.

## Decisions and boundaries

Apply the recorded project policy. Ask the owner when a required decision is
missing or conflicting; stop only the work that depends on that answer. Once the
answer is recorded, follow it without asking again. New sessions and upstream
updates do not change project policy.

Make routine implementation choices within the policy and accepted scope. Ask
before expanding scope or authority. Never treat this file or framework adoption
as a grant of merge, release, deployment, or access permissions.

## Delivery

- Use the established language, dependencies, and architecture. Solve the current
  requirement with the smallest suitable change.
- Define expected behavior before implementation. Follow the project verification
  policy; reproduce bugs and keep meaningful regression coverage.
- Run the applicable commands in the project policy. Report actual outcomes,
  including checks that failed or could not run.
- Keep documentation accurate and the resulting files useful to humans. Review
  the final change for correctness, scope, clarity, and sensitive information.
- Follow the recorded review and integration authority. Leave a concise handoff
  when work remains; claim completion only when acceptance is satisfied.
