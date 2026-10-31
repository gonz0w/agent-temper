# Agent instructions

Read this file, the [project policy]({{PROJECT_POLICY_PATH}}), and the adopted
[Agent Temper method]({{FRAMEWORK_PATH}}/METHOD.md) before working. The
[adoption record]({{FRAMEWORK_PATH}}/SOURCE.md) identifies the pinned upstream
revision. Apply only the profiles and local extensions selected in project policy;
read their requirements and compatibility conditions before affected work.

## Work authority

[{{WORK_TRACKER_NAME}}]({{WORK_TRACKER_URL}}) is the sole authority for live work,
priority, dependencies, ownership, and continuation. Follow the
[work profile]({{TRACKER_PROFILE_PATH}}). Read the selected work item and its
discussion before implementation. Work must have a bounded deliverable and
verifiable acceptance criteria.

Use the adopted [workflow]({{FRAMEWORK_PATH}}/docs/reference/workflow.md) to select
a bounded delivery batch and recheck it when resuming or changing scope. Follow
the project's work-in-progress limit. Multiple related issues may share one
integration; discovering another issue does not authorize adding it. Record a
disposition for findings and leave unrelated work for milestone prioritization.

Record execution discoveries and handoffs in that work item. Keep durable behavior
and decisions in the documentation. Do not create a second backlog or status log.

## Decisions and boundaries

Apply the recorded project policy. Ask its authorized decision maker when a
required decision is missing or conflicting; stop only dependent work. Once the
answer is recorded, follow it without asking again. New sessions and upstream
updates do not change project policy.

Make routine implementation choices within the policy and accepted scope. Ask
before expanding scope or authority. Never treat this file or framework adoption
as a grant of merge, release, deployment, or access permissions.

When project policy selects a model-routing profile, use its configured roles for
suitable bounded work. Supply the work item, applicable policy, source context,
acceptance, and edit boundaries. Follow its escalation and fallback rules. The
lead verifies returned evidence and owns integration; do not assume a requested
model ran without runtime evidence.

## Delivery

- Use the established language, dependencies, and architecture. Solve the current
  requirement with the smallest suitable change.
- Define expected behavior before implementation. Follow the project verification
  policy; reproduce bugs and keep meaningful regression coverage.
- Run the applicable commands in the project policy. Report actual outcomes,
  including checks that failed or could not run.
- Follow the adopted [attempt and stopping rules]({{FRAMEWORK_PATH}}/docs/reference/verification.md#bound-attempts-and-stop).
  Finish when acceptance, required checks and review are satisfied. At an attempt
  limit or repeated unexplained failure, checkpoint and replan; do not restart
  automatically, expand scope or waive a required gate.
- Keep documentation accurate and the resulting files useful to humans. Review
  the final change for correctness, scope, clarity, and sensitive information.
- Follow the recorded review and integration authority. Leave a concise handoff
  when work remains; claim completion only when acceptance is satisfied.
