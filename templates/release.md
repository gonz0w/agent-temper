# {{RELEASE_OR_DELIVERY_TITLE}}

Use this record in the authoritative delivery work item or release system. Link
existing procedures and remove inapplicable sections with a reason. Replace all
placeholders before treating the procedure as executable or the record as complete.

## Candidate and authority

| Field | Recorded value |
| --- | --- |
| Work item and accepted delivery boundary | {{ISSUE_AND_INTEGRATION_PUBLICATION_DEPLOYMENT_OR_OPERATIONAL_ACCEPTANCE}} |
| Source revision and artifact identity | {{IMMUTABLE_SOURCE_AND_ARTIFACT_DIGEST_OR_EQUIVALENT}} |
| Build provenance and supported targets | {{BUILD_INPUTS_TOOLCHAIN_DEPENDENCIES_TARGETS_AND_LIMITS}} |
| Release owner and required authority | {{OWNER_POLICY_AND_APPROVAL_RECORD_IF_REQUIRED}} |
| User-facing changes and support limits | {{RELEASE_NOTES_AND_COMPATIBILITY_REFERENCES}} |

## Procedure and acceptance

| Step | Environment, directory, inputs, and command or manual procedure | Expected result and stop condition | Actual evidence |
| --- | --- | --- | --- |
| {{BUILD_INSTALL_PUBLISH_DEPLOY_OR_CHECK}} | {{EXACT_PROCEDURE_OR_CANONICAL_REFERENCE}} | {{OBSERVABLE_EXPECTATION_AND_FAILURE_TRIGGER}} | {{NOT_RUN_OR_ARTIFACT_ENVIRONMENT_RESULT_AND_EVIDENCE_LINK}} |

Include the product's smoke check at the actual delivery boundary. Separate
candidate verification from publication or production checks. Identify the
reviewed artifact; do not treat commands in this template as executed evidence.

## Compatibility and recovery

- Changed interfaces, configuration, or data: {{EFFECTS_AND_MIGRATION_OR_NONE}}
- Recovery trigger and authorized operator: {{STOP_SIGNALS_AND_AUTHORITY}}
- Known-good artifact and recovery inputs: {{IDENTITIES_AVAILABILITY_AND_BACKUPS_OR_REASON_NOT_APPLICABLE}}
- Restoration or safe-stop procedure: {{EXACT_STEPS_OR_CANONICAL_RUNBOOK}}
- Recovery verification and actual rehearsal: {{CHECKS_RESULTS_AND_LIMITATIONS}}
- Irreversible changes and forward-repair limits: {{LIMITS_AND_REQUIRED_DECISION_OR_NONE}}

An older artifact does not establish data compatibility. Record an untested
recovery path as untested and apply the project's required acceptance gates.

## Review, delivery, and follow-up

- Review: {{REVIEWER_TYPE_FINDINGS_RESOLUTION_AND_REVIEWED_IDENTITY}}
- Delivery result: {{ACTUAL_IDENTITY_TARGET_TIME_OPERATOR_AND_OUTCOME_OR_NOT_PERFORMED}}
- Support and incident owner: {{OWNER_AND_APPROVED_CONTACT_OR_RUNBOOK_REFERENCE}}
- Remaining failed, skipped, or unavailable checks: {{LIMITS_AND_AUTHORIZED_DECISIONS_OR_NONE}}
- Later rollout or product learning: {{LINKED_WORK_OWNER_AND_TRIGGER_OR_NONE}}

Reconcile issue completion against the accepted boundary. Preserve unsuccessful
delivery and recovery results; do not rewrite them as a successful release.
