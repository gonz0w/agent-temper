# Take an uncertain request to a first useful product

This fictional exercise follows **Kit Desk**, a local tool for finding workshop
equipment. Every person, input, observation, and outcome below is invented for
teaching. No product, research session, test run, or delivery is reported as real.

You need only a text viewer. Read each step and answer its check. If you practice
with templates, use disposable files and a sandbox tracker. Do not create live
issues, contact people, or deploy anything from this exercise.

## 1. Clarify the request

The owner asks, “Build an app to manage workshop kits.” That could mean bookings,
stock control, repairs, or finding equipment. The agent first reads the project's
policy and opens an authorized discovery issue with this question:

> Which task should the first increment help a coordinator complete?

For this exercise, suppose the owner supplies these fictional observation notes:

- A coordinator consults one inventory file when someone requests a kit.
- The coordinator manually ignores rows marked `repair` or `allocated`.
- A previous request selected a kit whose row was marked `repair`.

The agent records the source and limitations of the notes. The immediate problem
is selecting an available kit for an activity. The notes do not establish demand
for online bookings or prove how often selection mistakes occur.

**Check:** Which claim is an assumption? “A filtered result would reduce selection
mistakes” is a hypothesis. The supplied notes describe the fictional current task.

## 2. Bound the investigation

The alternatives are a clearer inventory layout, a filtered list, and a booking
service. The first uncertainty is whether the existing inventory fields are enough
to select a usable kit. Building a booking service would not resolve that question.

The owner authorizes one task walkthrough using synthetic inventory rows. Before
the walkthrough, the agent records the proposed criterion:

> Given an activity, the coordinator can select a matching available kit or
> identify that none is available, without extra information about the equipment.
> Any missing selection information requires clarification before implementation.

The procedure is limited to two scenarios: a matching kit and no available match.
A static filtered list is enough to examine the selection question. This exercise
does not require a running application or a new dependency.

Suppose the fictional walkthrough meets that criterion. The conclusion is narrow:
the fields support these two scenarios. It does not prove that the product will
reduce mistakes in daily use. If a necessary field were missing, the next action
would be to clarify it. If the walkthrough could not occur, its result would be
unavailable, not passed.

**Check:** The criterion was recorded before the imagined result. Favorable
evidence still requires the owner to authorize the proposed implementation scope.

## 3. Specify a complete first task

The owner accepts a local command-line increment. The implementation issue says:

> **Outcome:** A coordinator supplies an inventory file and activity, then gets
> an available kit selection or a clear no-match result.
>
> **Scope:** The command is `kit-desk find FILE ACTIVITY`. Read CSV fields `kit`,
> `activity`, and `state`. Valid states are `available`, `allocated`, and `repair`.
> Match activity exactly. List all matching available kits in file order, one kit
> name per line on standard output. The coordinator selects from that result.
>
> **Non-goals:** Bookings, accounts, shared storage, repair tracking, network
> access, and changes to the input file.
>
> **Constraints:** Use the project's accepted stack and local check commands.
> Keep inventory local. Document the file format and supported command syntax.

The issue maps behavior to evidence:

| Acceptance | Check to perform in the actual project |
| --- | --- |
| Matching available kit names appear with exit `0`; allocated and repair kits do not | Command test with synthetic rows covering all three states |
| No available match prints `No available kit for ACTIVITY.` with the supplied activity on standard output and exits `1` | Command test with no match and an empty valid inventory |
| Missing files, missing fields, or unknown states exit `2`, leave standard output empty, and identify the file and cause on standard error; row errors also identify the row and field | Negative command tests with a malformed row after a valid match to check that no partial selection appears |
| The input file remains unchanged | Compare its contents before and after command execution |
| A coordinator can complete the task using the instructions | Follow setup and the documented example in an appropriate fixture |

The issue also names dependencies, owner, verification, and integration authority.
Its specification now establishes expected behavior before implementation; real
project decisions and check commands still come from that project's policy.

**Check:** Reading input through a usable selection is one complete task. Creating
only a CSV parser would not satisfy this issue. The scope does not promise booking.

## 4. Verify and deliver the increment

In a real project, the agent defines substantive success and failure checks,
records actual test-first evidence under project policy, implements the accepted
behavior, and follows the documented task. The reviewer inspects the final
change, evidence, instructions, and limits. No command result is supplied here.

The implementation issue's completion boundary is accepted integration. Any
separate distribution or operational step follows the project's authority. A
merge alone does not prove that coordinators used the tool or benefited from it.

**Check:** The review can establish that the tool obeys its contract. The later
question about selection mistakes needs different evidence.

## 5. Follow up on the intended benefit

Before closing implementation, the agent links a bounded evaluation issue:

> **Owner:** The product owner.
> **Trigger:** The first three authorized uses, or the agreed review date if
> fewer uses occur.
> **Signal:** Whether a coordinator selects an unavailable kit, with the input
> state and reason recorded without personal data.
> **Procedure:** Compare those observations with the earlier reported mistake;
> report the small sample and lack of a measured historical rate.
> **Decision:** Retain the selection approach, investigate a failure, or defer
> further investment. Expansion needs the owner's accepted next scope.

Suppose later fictional feedback says that a selected kit was already allocated,
because the inventory was stale. The implementation may have met its contract,
while the intended benefit remains unsupported. The owner can authorize a bounded
investigation of inventory freshness; a booking service is still only one option.

If no authorized uses occur, record unavailable evidence and the next review
decision. If the observations cannot distinguish causes, record an inconclusive
result. Do not mark either case as success or rewrite the completed test evidence.

**Check:** Implementation closure and product learning have separate evidence and
owners. Continue with [the discovery guide](../how-to/discover-product.md) when
your own request needs this route; use [the small-issue tutorial](first-issue.md)
for an already understood change.
