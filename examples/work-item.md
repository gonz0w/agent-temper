# Example: Print a deterministic inventory report

This is a fictional ready issue for the Quay project described in the
[example policy](project-policy.md). No implementation or check has run. All
verification below is planned, and no outcome is claimed.

## Outcome

A workshop operator can turn a local inventory file into a readable terminal
report and compare reports without changes caused by item ordering.

## Scope

Add `quay report inventory.json`. Input is a JSON list of objects with a unique,
nonempty `name` and a nonnegative integer `quantity`. Print one `name: quantity`
line per item, sorted by name using Python's default case-sensitive string order.
Print `No items.` for an empty list. Successful output ends with a newline.

Reject invalid records and duplicate names before printing a report. Exit with
status 2 and a concise diagnostic on standard error; standard output stays empty.
Treat names as text, rejecting control characters so input cannot emit terminal
control sequences.

**Non-goals:** file modification, totals, prices, network access, color, column
layout, alternate sort options, and additional export formats.

## Acceptance and planned verification

| Condition | Planned check and expected result |
| --- | --- |
| Stable readable report | A CLI regression supplies reversed input order and expects sorted `name: quantity` lines, trailing newline, and exit 0. |
| Empty input | A CLI regression expects exactly `No items.\n` and exit 0. |
| Invalid or unsafe input | Table-driven regressions cover malformed JSON, missing fields, duplicate names, negative or noninteger quantities, and control characters; each expects exit 2, a diagnostic, and empty standard output. |
| Existing CLI remains usable | Existing help and invalid-command tests remain green. |
| Operator can use the command | Add a reference contract and one how-to example with synthetic input; run documentation checks. |

Tests for these related behaviors remain in this issue. They are not separate
work items. The implementation uses the established Python standard library and
does not add dependencies.

## Context and readiness

The governing contract is the fictional project's `docs/reference/cli.md`.
The owner approved this scope under the “Readable local inventory” capability
milestone, whose exit condition is a documented, verified local report command.
There are no blocking issues. The issue has `status:ready` and `priority:normal`;
the implementing agent claims ownership before work starts.

## Required evidence and completion

Record the failing new CLI regressions before implementation, their failure
reason, the checked revisions, and passing focused and required checks afterward.
Include the planned synthetic CLI example and documentation validation. Obtain
independent review and merge under the example project policy. Implementation
completion does not authorize publishing a release.
