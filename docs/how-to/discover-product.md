# Turn an uncertain product request into useful work

Use this guide when the user problem, proposed solution, or expected benefit is
uncertain. The result is a recorded decision and, when authorized, a bounded
implementation issue. A clear defect or small understood change can go directly
through the [work-item template](../../templates/work-item.md).

## Before you start

Read project policy, the request, relevant product contracts, and existing work.
Confirm the investigation's scope and decision owner. Use the authoritative
tracker for live discovery; do not create a second backlog or a required product
document. A durable contract can become a linked product reference when needed.

Access to users, services, data, or spending still follows project authority.
Obtain any required permission before contacting people or running experiments.
Research authorization alone does not authorize implementation or deployment.

## 1. Describe the task and separate evidence from assumptions

Record who needs to do what, in which situation, and what prevents completion.
Describe the current workaround and its consequence. Separate the requested
feature from the underlying task: several solutions may serve the same need.

For each consequential claim, identify its source and limits. An observed failed
task, an owner's report, and an agent's inference provide different evidence.
Mark an assumption explicitly. An agent-generated persona or simulated interview
can help prepare questions; it cannot establish what actual users need.

**Check:** Another reader can identify the intended benefit and explain which
claims have evidence. Missing evidence remains visible in the issue.

## 2. Test the assumption that could change the decision

Compare a small number of plausible approaches, including the existing workaround
or a simpler change. Identify an assumption whose failure would alter the choice.
Choose a bounded way to investigate it before committing to a larger build.

An existing support report, an authorized task observation, a paper interaction,
or a small technical experiment may supply enough evidence. Choose the procedure
for the question; do not require interviews or prototypes for every change.

Record these fields before observing the result:

| Field | What to record |
| --- | --- |
| Question | The uncertain claim and the decision it affects |
| Procedure and limit | Inputs, participants if relevant, maximum effort, and stopping point |
| Decision criterion | What would support proceeding, changing the approach, or stopping |
| Authority | Who may conduct the investigation and settle the next action |

Record what happened, including contrary evidence and limitations. Distinguish a
criterion that was not met from an inconclusive result or an unavailable check.
A small observation can support a narrow decision without proving broad demand.
Do not adjust the original criterion silently to make a result look favorable.

**Check:** The decision follows the recorded evidence. If it remains uncertain,
name the next bounded question or stop; do not treat uncertainty as approval.

## 3. Specify one complete user task

Use the discovery result to propose a useful first increment. Describe the task
from its starting input or situation through an observable result. Include the
necessary interactions, failure response, and recovery. A database, API, or screen
alone is not a useful increment unless its intended consumer can complete a task.

Keep the specification in the implementation issue when that is sufficient.
Record accepted behavior, non-goals, constraints, dependencies, and evidence for
acceptance. Cover relevant invalid inputs, unavailable resources, permissions,
compatibility, and accessibility. Link existing contracts instead of copying them.

Resolve the choices that change the expected result or authority. Leave routine
implementation choices delegated by project policy to the implementer. Before
work starts, confirm that the proposed increment is within authorized scope;
supplying a complete specification does not itself make new scope ready.

**Check:** A reviewer can follow one whole task and explain how its result will
be checked. See the [verification reference](../reference/verification.md) for
checks appropriate to the change, including real interaction when relevant.

## 4. Arrange evidence of user benefit

When usefulness needs later observation, record a follow-up in the tracker with:

- The benefit to assess and the signal that would support or challenge it.
- The procedure, relevant baseline, and limits of the comparison.
- An accountable owner and a date or event that triggers the assessment.
- The decision the evidence will inform and the authority needed to act on it.

A task observation, support report, or owner review may be sufficient. Add
instrumentation only when it serves the question and fits project policy.
Do not equate a passing test, a shipped feature, or a count of visits with benefit.

Define the implementation completion boundary before delivery. If later outcome
evaluation is separate work, link its owner and trigger before closing the
completed implementation issue. If outcome evidence is part of current acceptance,
keep that work open until its gate is satisfied or explicitly changed by authority.

## 5. Use the result to choose subsequent work

At the recorded trigger, assess the signal and preserve its limits. A result may
support the benefit, contradict it, remain inconclusive, or be unavailable.
Record the actual state; absent feedback is not success. Report a missed trigger
and assign the next action rather than leaving an ownerless follow-up.

Use the evidence to propose continuing, changing, or stopping the approach. Keep
new work bounded and obtain authority where the next increment changes scope.
A functioning implementation can remain completed even when later learning
changes product direction; record the new finding without rewriting old evidence.

For a worked example, read the [first-product tutorial](../tutorials/first-product.md).
The [source notes](../explanation/sources.md) describe influences and their limits.
