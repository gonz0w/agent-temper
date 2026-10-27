# Compose project policy

Use this guide to keep project policy readable as requirements grow. The result
is one clear entry point, explicitly selected rules and a usable check/delivery
map. Small projects can keep rules inline. This procedure grants no execution,
integration or release permission and requires no policy runtime.

## 1. Assign each fact one home

Read current policy, adopted sources and the owning work item. Inventory actual
conflicts and duplicates before moving files. Use the
[composition reference](../reference/extensions.md#organize-local-policy-by-responsibility)
and [project-policy template](../../templates/project-policy.md).

Keep portable method requirements upstream, reusable technical rules in a
selected retained profile, and product-specific requirements in local contracts.
A shared policy source is optional and may be any appropriate provider. It does
not impose one organization's platform, forge or AI vendor on unrelated projects.
Keep live work in the selected tracker.

For example, PROJECT can link verification, execution, integration and model-routing
modules when these concerns need separate maintained documents. Do not create
empty modules or repeat their full rules in AGENTS and CONTRIBUTING. Keep settled
small choices in PROJECT; use [an extension record](../../templates/extension.md)
only when it improves the reader's task.

## 2. Select and review the combined rules

For each selected module, identify its path, source identity, owner, applicability,
dependencies, declared conflicts and change authority. Give referenced rules stable
IDs. Bind local documents to the containing project revision; retain immutable
external source and hashes. Files being present does not activate them.

Check requirements, defaults and delegated choices together. Name the exact
approved replacement for a superseded rule. No implicit latest/local/strictest
precedence applies. Missing dependencies or conflicting obligations stop dependent
work for the required decision. Keep active exceptions separate from linked
historical decisions. Check date and event expiry before using an allowance.

Walk one ready work item from selection through acceptance, review and delivery.
A new agent should find the applicable rules and authority from PROJECT without
reconstructing a conversation or searching expired approvals.

## 3. Map checks to effects and permitted execution

Use the [verification-policy template](../../templates/verification-policy.md)
where a command table is insufficient. Record semantic triggers, inputs, commands
or manual steps, allowed executors, limits, expected outcomes and evidence.
Separate check applicability from execution permission and executor availability.
Review the concrete diff; prose/configuration can alter consequential behavior.

An owner-approved [method-maintenance policy](../../templates/method-maintenance.md)
can settle repeated passive-source work once. Fill its exact eligibility, trusted
inputs, allowed tools/hosts, exclusions, review and integration gates. Record any
replacement of an existing requirement explicitly. The template itself cannot
permit a host validator or replace a mandatory native check.

## 4. Connect the delivery implementation

Map the same verification contract to the project's chosen tools and provider:
trigger, identified inputs, permitted executor, applicable checks, actual results,
review, immutable artifacts, release authority and recovery. Check local/hosted
alignment rather than assume it. A local tracker or manual release can implement
the same method without GitHub or a hosted pipeline.

A required integration result must accurately reflect its selected checks and
manual gates. Unknown changes follow the conservative path. Test the selector's
positive, negative and unknown-path cases before relying on it. A missing required
executor or status remains a block; a document edit does not change protections.
In GitHub specifically, skipping an entire required workflow can leave its status
pending; see [required-check behavior](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks#handling-skipped-but-required-checks).
This is an optional provider detail, not a prescribed implementation.

Before release, exercise the actual artifact boundary and recovery according to
the [release guide](release-software.md). Packaging is not publication, a source
merge is not deployment, and a copied pipeline is not evidence of successful use.

## 5. Validate portability and retain the decision

Use contrasting paper cases before a real adoption:

| Fictional project | Local choices | Shared workflow question |
| --- | --- | --- |
| [Windows game](../../examples/windows-game/PROJECT.md) | Windows target, selected engine, asset/save/playtest contracts, local tracker and manual publication. No Codex or GitHub profile. | Can an agent distinguish asset, save-format, engine, policy and release work without importing BSD/provider assumptions? |
| [Quay CLI](../../examples/project-policy.md) | Python, Linux/macOS and selected GitHub work profile. | Does the same method preserve its own command map, issue states and review authority? |
| Harbor service (paper case only) | Containerized service, internal tracker, approved staging executor; production credentials unavailable. | Stage smoke/recovery may pass while production delivery remains blocked; no new access follows from the method. |

The [Windows-game walkthrough](../tutorials/windows-game.md) includes rejection,
unavailable-gate and delivery cases. These examples are fictional source/reader
exercises, not platform or pipeline qualification. Record real consumer findings
in its own work item, then propose a bounded upstream correction through the
[feedback route](../reference/extensions.md#feed-useful-findings-back).
