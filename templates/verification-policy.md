# {{PROJECT_NAME}} verification policy

Optional module. Complete and approve this document before selecting it from
project policy. A short project command table can supply the same information.

| Decision | Recorded answer |
| --- | --- |
| Module/rule identities | {{MODULE_ID_AND_STABLE_RULE_IDS}} |
| Owner, applicability and source | {{OWNER_SCOPE_AND_SOURCE_RECORD}} |
| Dependencies and conflicts | {{REQUIRED_POLICIES_AND_CONFLICTS_OR_NONE}} |
| Selection and change authority | {{PROJECT_SELECTION_AND_AUTHORIZED_CHANGE_PROCESS}} |

## Change and check map

For each maintained check, record its semantic trigger, input/source identity,
working directory, command or manual procedure, permitted executor, tool/input
requirements, resource bounds, expected result, evidence and stop condition.
Link the canonical command contract; avoid copied scripts or duplicated pins.

{{CHANGE_CLASSES_CHECKS_EXECUTORS_AND_EXPECTED_RESULTS}}

Inspect the actual diff. Distinguish source inspection, executable/configuration,
product/data, authority and delivery changes. Unknown impact uses the declared
conservative path until investigated. Keep meaningful test-first expectations for
behavior changes. A file extension or successful syntax parse is insufficient.

## Integration and delivery

{{LOCAL_HOSTED_MANUAL_AND_RELEASE_GATES_WITH_REVIEW_AND_AUTHORITY}}

Map required checks to the chosen platform/provider. Keep failed, unavailable,
skipped and not-applicable outcomes distinct. A successful aggregate means the
required checks for the declared scope actually satisfied their contracts; it
must not claim that unexecuted product tests passed. A new selector needs positive,
negative and unknown-input controls before reliance. Release/build/package checks
identify immutable artifacts; installation/recovery checks exercise the actual
accepted boundary. State any manual gates or deferred product qualification.

## Exceptions

{{ACTIVE_APPROVED_EXCEPTIONS_OR_NONE_WITH_HISTORICAL_RECORD_LINKS}}
