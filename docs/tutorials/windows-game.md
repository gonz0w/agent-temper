# Walk a Windows game through Temper

This fictional paper exercise shows the same method used by a project with a
Windows game target, local tracker and owner-controlled release. It supplies no
game engine, executable pipeline, actual approvals or measured results. Read the
[example PROJECT](../../examples/windows-game/PROJECT.md) and its three modules.
For a real project, fill the [onboarding questions](../../templates/onboarding.md),
select actual engine/toolchain/targets and follow [adoption](../how-to/adopt.md).

## 1. Read one coherent selection

PROJECT selects verification, execution and integration modules, each with a
canonical home, owner and rule IDs. No GitHub, Codex, BSD or shared-standards
provider is required. The same roles of work item, evidence, reviewer and delivery
owner apply regardless of which tools implement them.

Check that VERIFY-01's check choices and EXEC-01/02's execution boundaries are
compatible. INT-01 accepts reviewed source; DELIVER-02 separately gates public
release. Do not infer authority from the method's presence or a working tool.

## 2. Select a first useful increment

Imagine an accepted work item: “A player can complete one puzzle and resume its
checkpoint after restarting.” Its non-goals exclude cloud saves, multiplayer and
a store release. The fictional owner supplies an existing Windows fixture and
finite task budget; if either is missing, dependent execution is blocked.

Before implementation define allowed outcomes: solve the puzzle, save once,
restart and resume the same state. Define rejection/recovery: malformed save,
interrupted write and incompatible version preserve the previous valid save or
produce the documented safe refusal. Use synthetic files and derive assertions
from these requirements. Establish actual red then green in a real implementation;
this paper exercise claims no historical run.

## 3. Apply the policy to different changes

| Proposed change | Expected policy route in this paper case |
| --- | --- |
| Change a texture | Asset rights/import/budget plus rendered inspection under VERIFY-01 and EXEC-02. It cannot use passive source checks alone. |
| Change checkpoint serialization | Behavior-first save/migration/interrupt/recovery tests and the Windows puzzle task. Use owned synthetic copies; no player data. |
| Upgrade the engine | Exact toolchain/dependency review plus clean build/package, input/render/save checks and playtest. No new installation or rights by inference. |
| Update the method pin | Inspect semantic differences. If no tool/runtime/authority/gate change, EXEC-01 permits its precise passive source checks plus separate review. Otherwise select the affected broader route. |
| Add a rule that permits store upload while DELIVER-02 still requires approval | Stop that conflicting action. The owner must explicitly replace the named requirement or reject the proposal; file order cannot settle it. |
| Need Windows checks while the approved Windows executor is unavailable | Record unavailable coverage and stop dependent acceptance/integration. Permitted source preparation may continue; metadata success cannot qualify the game. |
| Find a temporary allowance whose expiry event already occurred | Treat the allowance as ended. No retry, check waiver or authority is renewed. |

## 4. Implement the development and delivery contract

In a real adoption, bind each example check to maintained actual tooling before
use. Record trigger, source/input identity, working directory/command or manual
steps, permitted executor, bounds, expected outcome, evidence and stop condition.
A future pipeline must implement that map and be exercised, including unknown
changes and unavailable executors; copying YAML cannot supply this evidence.
The framework's Python checks exercise its own documents/helpers only.

Once required behavior checks and separate review pass, INT-01 permits the
fictional local source integration. DELIVER-01 then needs the identified Windows
package in an owned install, with puzzle/input/save smoke checks. Passing unit
checks alone does not show that the packaged game starts without its source tree.

Suppose the installed candidate fails to resume its checkpoint. Record failure,
stop publication and use DELIVER-03's approved recovery path. The known-good
package and save compatibility must be available before recovery; never destroy
the only save copy or label an untested recovery procedure successful.

Even if all development/package checks pass, DELIVER-02 still requires owner
release approval. A local project, hosted CI and store distribution each retain
their own integration/publication authority and evidence.

## 5. Review what this establishes

A reader can trace asset, save-data, engine, policy and release work through one
consistent method with different applicable checks. The
[composition guide's CLI and service cases](../how-to/compose-policy.md#5-validate-portability-and-retain-the-decision)
use the same questions with different local tools and delivery boundaries.

This is source/example/reader validation of policy portability, not a built game,
Windows qualification, functioning CI/CD pipeline, accessibility certification or
proof of improved productivity. Real projects retain real execution evidence in
their own trackers. A missing requirement or runtime failure remains visible.
