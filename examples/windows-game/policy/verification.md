# Example: Lantern Trail verification

This is fictional policy for the [example project](../PROJECT.md). Commands and
expectations are paper examples, not an engine interface or executed evidence.
The game owner owns this module and changes to its requirements. It depends on
the selected execution module; no declared conflicts apply.

## VERIFY-01

Requirement: select checks from the semantic effect of the actual diff. All
changes need source/provenance review, affected documentation and separate review.
Unknown impact selects all potentially affected checks until bounded. No blanket
Markdown, asset or configuration exemption exists.

| Trigger | Illustrative checks and acceptance | Permitted executor |
| --- | --- | --- |
| Method/provenance maintenance with no runtime, authority or gate change | Exact retained source/inventory/hash/license/link comparison and combined-policy walkthrough; no unexplained drift. | Passive host boundary under EXEC-01. |
| Texture/audio edit | Asset provenance, import validation, size budget and in-game visual/audio inspection; no missing/invalid asset or rights gap. | Windows development fixture under EXEC-02. |
| Gameplay or save code | Test-first affected behavior, existing regression suite, engine-supported automation, Windows build and representative playtest. | Windows development fixture under EXEC-02. |
| Save schema or migration | Above plus old-save fixtures, interrupted-write/recovery and failed-migration preservation; do not destroy the only save copy. | Owned synthetic save directory under EXEC-02. |
| Engine/toolchain upgrade | Dependency/license review, compatibility matrix, clean Windows build/package and input/render/save/playtest checks. | Approved exact toolchain under EXEC-02; new tools need approval. |
| Policy, check selector or permissions | Owner decision where required; positive/rejection/unknown-impact cases for any executable selector; required checks remain until explicitly replaced. | Existing approved executor; no new permission inferred. |

## VERIFY-02

Requirement: distinguish expected and actual results. Fictional `game-check`
commands would have their exact working directory, inputs, exit/output contract,
resource limits and retained logs defined by this project's maintained tooling.
An engine supporting no headless mode needs another approved oracle; Temper
cannot infer that headless tests exist. Manual playtest, usability/accessibility
and performance observations remain separate from automated assertions.

## VERIFY-03

Requirement: every required gate must pass or have an authorized scoped
disposition. An unavailable Windows executor is not a pass, and host metadata
checks do not establish rendering, frame time, controller behavior or save safety.
This policy grants no exemption from enforced required statuses. Results identify
source/artifact, toolchain, executor, checks, failures and limitations.
