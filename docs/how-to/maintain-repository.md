# Maintain a repository

Use this guide for a bounded maintenance pass: understand the affected system,
inspect selected work and checks, and leave evidence with a concrete next action.
The result can be a corrected tracker record or an actionable finding; it need
not be a code change.

Before starting, read project policy, the selected work item and discussion,
active ownership, and relevant reviews. Use the project's existing tracker and
selected work profile under the [workflow](../reference/workflow.md). This guide
grants no new authority.

## 1. Bound the pass

Record the trigger, inspected scope, and completion condition in the maintenance
work item. A trigger can be a new report, failed check, support change, or an
authorized maintenance request. Identify the relevant records or time window and
any permitted changes. Do not turn a pass into an unbounded repository cleanup.

For example, a fictional task could inspect reports filed against the last release
and finish when each has evidence, a classification, and a next action. Fixing
every reported defect is outside that task unless its acceptance says otherwise.

## 2. Orient when the system is unfamiliar

Start at the README and agent entry point. Follow existing architecture and
setup documentation. Use a short [repository map](../../templates/repository-map.md)
only when it improves navigation; retain canonical links instead of copying
commands, policy, or live status. Do not inventory every file.

Have an agent without prior implementation context follow one representative
behavior through this exercise:

1. Trace an input from its entry point through the relevant components to its
   visible result. Identify external systems, data boundaries, and an invariant
   that must remain true. Distinguish maintained source from generated output.
2. Locate the tests for that behavior and the contracts they check. Identify
   consumers that a change could affect, including callers outside that component.
3. Follow the documented setup and run an authorized local path with safe sample
   inputs. Run the relevant focused check and compare its outcome with the stated
   expectation. Use the project's existing commands and environment rules.
4. Record the source revision, route followed, actual results, and navigation gaps
   in the work item. If setup, credentials, or a service is unavailable, record the
   blocked step and what source inspection established. Do not call that execution
   a pass or use it to claim end-to-end coverage.

For a small project, a few links and prose can explain the system. Add context,
container, or finer views only when they answer a reader's question. A diagram
is optional. Keep the map current when the relationships it describes change.

## 3. Inspect and choose the next action

Apply the following cases within the recorded scope. Use the existing work item
when a finding belongs to its acceptance; otherwise propose a bounded item under
project policy. A finding does not itself authorize implementation or urgency.

| Trigger | Evidence to inspect | Next action |
| --- | --- | --- |
| Incoming report or possible duplicate | Expected and actual behavior, affected version, reproduction, and related reports | Record missing information or a reproducible result. Compare the actual failure and scope before declaring a duplicate. Link the canonical issue and preserve any distinct evidence; close a duplicate only with the required authority and reason. |
| Failed CI | Source revision, failed assertion or step, environment, and relevant prior results | Distinguish a product regression from setup or infrastructure failure. Reproduce with the smallest useful check when possible. Record unavailable evidence and the next diagnostic; do not waive a gate or treat an unexecuted check as passed. |
| Review with no recent activity | Current owner, review findings, latest diff, and changed inputs since verification | Identify the outstanding review or decision and its responsible actor. Record the next action or use an authorized reminder route. Age alone does not transfer ownership, authorize a merge, or justify closure. |
| Blocked dependency | The named prerequisite, its actual acceptance and integration state, and the dependent contract | Remove a blocker only when its condition is satisfied. Recheck dependent readiness; a merged component may still need system acceptance. Record the remaining blocker otherwise. |
| Dependency or support change | Current versions and usage, upstream notices, affected contracts, support promises, and relevant risk | Propose a bounded update, mitigation, or support decision with compatibility and verification needs. Do not upgrade merely because a newer version exists or change support promises without authority. |
| Milestone appears complete | Every exit condition, linked deliverables, integrated evidence, and any release or operational gate | Reconcile missing evidence and unfinished work. Close only under the project's authority after the actual exit conditions pass; task counts alone do not establish completion. |

Protect sensitive reports and logs under the project's evidence policy. Keep
private data out of public tracker records. Follow the project's security or
incident route when the finding requires it.

## 4. Reconcile and finish

Update only records and artifacts within the authorized scope. Preserve current
owners, accepted priorities, deferred scope, and useful history. An old issue can
still describe a current need; elapsed time is evidence about activity, not proof
that the need disappeared. Do not change permissions or bypass checks to finish.

For each finding, record the evidence, disposition, existing or proposed work
item, and next action with its responsible actor or unresolved decision. State
what was not inspected and which checks were unavailable. Link to durable product
documentation when a fact belongs there instead of maintaining a second backlog.

Complete the maintenance item when its recorded inspection and reconciliation
conditions are met and its required review is complete. Finding a defect can
complete an investigation while leaving the repair open. If the pass is
interrupted, leave the [continuation checkpoint](../reference/workflow.md#leave-a-usable-continuation).
