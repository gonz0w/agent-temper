# {{PROJECT_NAME}} repository map

Use this optional map when existing documentation does not provide a clear route
through the system. Keep only the views a reader needs. Replace placeholders and
remove these prompts before accepting the document. Link existing facts; do not
duplicate setup commands, policy, live work, or an exhaustive file listing.

## System and boundaries

{{PRIMARY_USER_OR_CALLER_AND_VISIBLE_OUTCOME}}

{{MAIN_COMPONENTS_THEIR_RESPONSIBILITIES_AND_EXTERNAL_SYSTEMS}}

{{IMPORTANT_DATA_OR_TRUST_BOUNDARIES_AND_CANONICAL_CONTRACT_LINKS}}

Start with the system's context and main components. Add a diagram or finer view
only when it makes a relevant relationship easier to understand.

## Find the maintained source

| Reader needs | Canonical location and purpose |
| --- | --- |
| Start the main behavior | [{{ENTRY_POINT_NAME}}]({{ENTRY_POINT_PATH}}): {{RESPONSIBILITY}} |
| Find the core implementation | [{{COMPONENT_NAME}}]({{COMPONENT_PATH}}): {{RESPONSIBILITY}} |
| Verify the behavior | [{{TEST_NAME}}]({{TEST_PATH}}): {{CONTRACT_CHECKED}} |
| Find affected consumers | [{{CONSUMER_NAME}}]({{CONSUMER_PATH}}): {{CONTRACT_USED}} |
| Set up and run local checks | [Setup and verification]({{CANONICAL_SETUP_AND_CHECKS_PATH}}) |
| Find governing decisions | [Architecture and contracts]({{CANONICAL_ARCHITECTURE_PATH}}) |

Add or remove rows for the actual navigation needs. Link to the canonical owner
record when ownership matters; keep assignments and progress in the tracker.

## Trace one behavior

{{REPRESENTATIVE_INPUT_TO_ENTRY_POINT_TO_COMPONENTS_TO_VISIBLE_RESULT}}

{{IMPORTANT_INVARIANT_AND_LINK_TO_ITS_CONTRACT_AND_CHECK}}

{{AFFECTED_CALLERS_OR_CONSUMERS_AND_FAILURE_OR_RECOVERY_BOUNDARY}}

Identify where external systems participate and which parts the local checks
exercise. Link to setup or operational documentation for commands and procedures.

## Maintained and generated files

{{MAINTAINED_SOURCE_LOCATIONS_AND_GENERATED_OUTPUT_BOUNDARIES}}

{{CANONICAL_GENERATION_INSTRUCTIONS_OR_REASON_NO_GENERATED_OUTPUT_APPLIES}}

Name the source of generated output and how it is reproduced. Update this map
with changes to the relationships it describes. Record orientation checks and
navigation findings in the work item, not as a status log here.
