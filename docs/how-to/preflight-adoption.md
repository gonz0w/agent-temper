# Preflight an adoption change

Use this guide before editing a project's adopted method, local policy, or model
routing. The result is a bounded approach in the existing adoption/update issue,
with applicable gates and authority identified. This guide adds no execution or
integration permission. Follow the project's current policy even when the proposed
change is small.

## Establish scope before edits

Read the issue and discussion, current agent entry point, project policy, source
record, selected profiles, and candidate diff. Use
[Adopt Agent Temper](adopt.md), [Update Agent Temper](update.md), or
[Configure Codex](configure-codex.md) for the actual procedure. Keep one compact
record in that issue; link settled decisions instead of copying them. Omit rows
that truly do not apply, with a reason. Do not create another status journal.

| Question | Record in the owning issue |
| --- | --- |
| What changes? | Current consumer/source identity, candidate immutable source, exact files and changed obligations or behavior, acceptance, and non-goals. |
| Which rules apply? | Current local policy, selected profiles/extensions, transition rules, and any conflict or missing decision. Proposed policy is not yet effective authority. |
| What evidence is needed? | Checks tied to each affected contract, mandatory hooks/CI, suitable executors, and whether those executors are available and authorized. Link relevant reusable evidence with its limits. |
| Who can integrate? | Required signatures/DCO, separate review, integration authority, and any additional decision needed. Check current protections rather than assume an earlier exception persists. |
| What bounds and stops apply? | Authorized resources, time/attempt limits, isolation and cleanup where applicable; stop on drift, unavailable mandatory gates, failed acceptance, or exhausted authority. |
| What will remain unverified? | Distinguish bundle identity, configuration observations, actual client routing, and product qualification. Name the next owner/action for an unresolved boundary. |

Use the [verification reference](../reference/verification.md) to choose evidence
and assess reuse. File extensions alone do not determine applicability: a TOML
change can alter execution, and a prose change can alter required behavior.
Mandatory local gates remain mandatory until their authorized decision maker
explicitly changes them. A successful source check does not establish runtime
routing or product behavior.

The optional [read-only auditor](audit-adoption.md) can supply bounded bundle and
role observations when local execution policy permits it. Its report does not
choose applicable gates, authenticate the source, or establish integration authority.

## Walk the proposed boundary

These cases are fictional. They describe decisions to record, not permission to
run commands, launch guests, change policy, or merge.

| Case | Bounded scope and evidence | Decision and limit |
| --- | --- | --- |
| Model/pin-only update | Harbor moves from reviewed pin A to reviewed pin B and merges one selected role's model/effort mapping. Its issue lists the actual upstream diff and confirms no product or CI files change. Check complete bundle inventory/hashes against the candidate, provenance, links, role TOML and policy consistency; run all gates required by Harbor policy, obtain separate review and required signed commits. | Harbor permits integration of source/configuration changes with these checks. The issue records client routing as unverified and not part of this increment's acceptance; a separately authorized client exercise is required before relying on the new route. No product performance claim follows. If existing policy requires that exercise now, this boundary cannot exclude it. |
| Genuine behavior change | Orchard changes a role's tool access and fallback behavior, beyond a pin or model identifier. Its issue identifies the changed permissions and affected tasks. Obtain required authority first; establish positive, rejection and fallback expectations, then test in the intended client with observable settings and required product checks. | A TOML parse alone is insufficient. Keep implementation and integration blocked until the required authority and behavior evidence exist. Treat any new CI infrastructure as separate work, not an automatic dependency to implement. |
| Mandatory executor unavailable | Beacon's current policy requires a native gate for every adoption change. No authorized executor is available. The issue records the unavailable gate, exact candidate, permitted independent source preparation, and integration stop. | Stop dependent execution/integration. Present one concrete bounded proposal to the authorized owner, or leave the item blocked. Source review does not replace the native gate. |

A useful Beacon proposal names the exact candidate, current mandatory gate, reason
it is unavailable, requested alternative evidence, resulting assurance gap, and
whether it changes verification applicability or grants a specific execution.
For execution, include finite resources/attempts, stop and cleanup conditions.
For an exception, record its scope and expiry under the
[extension rules](../reference/extensions.md#select-and-compose-explicitly).
An example request is: “For this identified adoption candidate only, accept the
listed source/configuration checks and separate review instead of the unavailable
native gate. Native behavior remains unverified. The exception ends at integration
or rejection and grants no executor, CI, protection, or retry changes.” This is a
proposal, not an accepted waiver; stricter non-waivable policy still governs.

Continue only independent preparation already permitted by policy. Do not start
another attempt, expand a resource ceiling, repair unrelated infrastructure, or
reuse an expired exception because a prior attempt failed. Record an accepted
decision once at its required policy home and link it from the issue. Recheck the
scope if the candidate, applicable rules, or relevant environment changes.

## Review the prepared result

Map each acceptance condition to actual evidence, keeping failed, unavailable,
and not-applicable results distinct. Have the separate reviewer examine the
candidate, preflight boundary, combined policy, checks, and remaining limits.
Integrate only when the project's applicable gates and authority are satisfied.
Keep later runtime qualification or infrastructure work in its own authorized item
when it is outside this adoption's agreed acceptance.
