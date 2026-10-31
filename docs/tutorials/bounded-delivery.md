# Finish a bounded delivery batch

This fictional reader exercise shows how small issues can share one integration
without absorbing every discovery. No implementation, test or platform campaign
described here has run. You need only a text viewer; do not open live issues from
the sample identities.

## 1. Select a capability and a batch

Imagine **Lantern**, a report tool. Its milestone is "Operators can export a
report and understand failures." The milestone also requires a later native
installation demonstration. Project policy permits source integration after
source checks and separate review; native qualification and release remain
separate gates. The owner selects milestone priorities and delegates selection
of ready member issues and ordinary verification repairs to the integration lead.

The lead selects these fictional issues:

| Issue | Bounded acceptance |
| --- | --- |
| L-11: Write a report file | A valid input produces the specified report; an invalid input produces no output file. |
| L-12: Explain write failures | An unwritable destination produces the documented error and preserves existing data. |
| L-13: Document export use | Instructions explain the implemented command and its failure behavior. |

The owning work item records the batch: "Export a report with useful errors,"
L-11 through L-13, one integration lead, source checks and separate review.
Exclusions are caching, alternate formats, native qualification and release.
Member issues link to that record. The lead has one active batch, including
review; this limit does not prohibit other leads working on disjoint outcomes.

**Check:** Each issue has assessable acceptance. The batch is a coherent source
outcome rather than the whole milestone. Tests for each issue stay with that issue.

## 2. Decide what discoveries mean

During implementation, the lead records these fictional findings:

| Finding | Disposition |
| --- | --- |
| The new writer truncates an existing file on failure | Repair L-12: preservation is current acceptance. |
| The required serializer cannot represent the specified output value | Link prerequisite L-14 and mark dependent work blocked. The priority owner must select a separate prerequisite or authorize a bounded batch change. |
| Caching could make repeated exports faster | Search existing findings, then record L-15 in backlog for later milestone prioritization. Do not implement or benchmark it now. |

The priority owner selects L-14 into the batch, records why it is necessary and
updates membership, effort and affected checks before work proceeds. L-15 remains
unselected. If L-14 were a large independent capability, the owner could instead
sequence it separately while preserving the blocked batch and its current work.
Because blocked work still counts against WIP, that separate batch needs another
integration lead or an authorized, recorded adjustment to the original lead's
WIP limit. A dependency decision alone does not create extra capacity.

**Check:** Creating L-15 did not authorize it. A real blocker received a visible
decision rather than becoming an unrecorded expansion. Ordinary acceptance repairs
did not need a new issue or repeated owner permission.

## 3. Bound verification and handle failure

The work item references the project's check map. The planned attempt uses the
focused export/preservation regressions, documentation checks, required assembled
source checks and a separate reviewer. A routine check runs once, then the lead
inspects any failure. A costly native campaign is outside this source batch.

Suppose a focused test exposes the truncation defect. The lead repairs it and
reruns affected checks within delegated authority. Suppose instead the required
executor is unavailable. The lead records that block and continues only independent
authorized work. Repeated unexplained failure ends the attempt with a checkpoint;
it does not authorize endless retries, a new harness or weaker assertions.

A newly identified data-loss path can require broader relevant checks. The lead
records the coverage gap and revised effort under project authority before relying
on those checks. A limit is a reason to replan, never permission to skip a gate.

**Check:** Check selection can respond to evidence. Neither the initial plan nor
an exhausted budget allows the agent to ignore a relevant unmet requirement.

## 4. Review and finish

One fictional PR contains L-11 through L-14. Its description names the batch,
maps each issue's acceptance to actual evidence in a real implementation, links
L-15 as unselected later work, and states the native/release limits. The reviewer
checks the combined behavior, required evidence and boundary. Passing a focused
test alone is insufficient; satisfied integration acceptance is the stopping point.

After required source checks and review pass, the lead integrates under policy
and closes only fully completed member issues. The milestone remains open for
its native demonstration. The lead does not add caching while waiting for review
or claim a healthy installed release from source evidence.

**Check:** Completion follows the previously recorded boundary. If native execution
were an integration requirement, the same source-only result would remain blocked.

## 5. Apply the same method with another work system

A native factory can use objective and change IDs, immutable candidate compositions,
durable checkpoints and policy-authorized promotion instead of GitHub issues and
PRs. A local tracker can use its own work and review records. Each maps the same
batch, disposition, evidence and authority rules; no agent vendor or forge is required.

During adoption, inspect existing ownership, branches, batches and mandatory gates.
Record how unfinished work transitions without discarding it or silently renewing
attempts. Follow [Update an adopted method](../how-to/update.md). The
[workflow](../reference/workflow.md) and [verification reference](../reference/verification.md)
own the rules; this exercise adds no permissions or runtime qualification.
