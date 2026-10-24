# Take a small issue from intent to delivery

This fictional exercise shows how policy, a ready issue, verification, and
continuation fit together. It does not assign live work or report tests run in
this repository. Every result below is illustrative.

You need only a text viewer. Read each step and check the expected result. If
you practice by editing templates, use a disposable directory and a sandbox
tracker; do not create real backlog entries from this example.

## 1. Establish the project's decisions

Imagine **Parcel**, a small command-line tool that inspects local data files.
Its owner has accepted these decisions in project policy:

| Decision | Accepted answer |
| --- | --- |
| Work authority | GitHub Issues; milestones describe useful capability outcomes |
| Implementation | Continue with the project's existing language and test tools |
| Verification | Reproduce bugs; prefer test-first behavior changes; run the documented local checks |
| Agent authority | Implement ready issues and integrate after required checks and review |
| Release authority | Ask the owner before publishing a release |
| Policy changes | Owner-approved change recorded in project policy |

The actual project policy would name the language and exact commands. They are
not invented here because this exercise does not execute a software project.
See the [onboarding questions](../../templates/onboarding.md) for the complete
decision set.

**Check:** A new agent can tell that another integration-permission question is
unnecessary after the agreed checks and review pass. Publishing a release still
requires the owner's answer.

## 2. Write a ready issue

The milestone is “Inspect local files with predictable output.” The following
issue contributes one independently reviewable improvement.

> **Title:** Explain a missing input file without a stack trace
>
> **Outcome:** A person who mistypes a path understands the failure and can
> correct it.
>
> **Scope:** Change the missing-file error from `parcel inspect`. Preserve the
> successful output contract. Do not add path search or automatic recovery.
>
> **Acceptance:**
>
> 1. For a missing file, the command exits with code `2`, writes no standard
>    output, and writes one diagnostic line to standard error.
> 2. The diagnostic identifies the requested path and says the file was not
>    found. It contains no stack trace.
> 3. Inspecting an existing valid file keeps its documented output and exit code.
>
> **Context:** Read the command's current reference page and the existing CLI
> test conventions. Error handling is the relevant implementation area.
>
> **Dependencies:** None.
>
> **Verification:** Add a missing-file command regression and retain the valid
> file regression. Run focused tests, then the required local checks. Update
> the command reference and verify its example.
>
> **Completion:** Integrate the accepted change after the required review and
> checks. Release publication is outside this issue.

Use the [work-item template](../../templates/work-item.md) in a real project.

**Check:** The agent can explain the behavior to build and the behavior to
preserve. “Improve errors” alone would not supply that information. This issue
does not require a new language, service, abstraction, or planning document.

## 3. Define independent checks before implementation

The agent writes a command-level regression from the acceptance criteria. The
test supplies a path that does not exist, invokes the command, and asserts the
exit code and both output streams. It uses an owned fixture and does not delete
or depend on a person's files.

In this fictional scenario, the first run fails because the existing command
returns code `1` and prints a stack trace. That is a useful red result: it
demonstrates the missing behavior. A compilation failure caused by a misspelled
test name would not demonstrate it.

The agent records the real command, source revision, failure, and reason in the
issue when doing this in an actual project. It then makes the smallest change
that satisfies the test and keeps the existing valid-file assertion intact.

**Check:** The test describes user-visible behavior. It does not simply assert
that a new helper function was called.

## 4. Make an interruption recoverable

Suppose the session ends after the regression fails and before implementation.
The issue continuation comment would contain:

> **Illustrative continuation:** Missing-file regression is written and fails
> for the expected behavior difference. Implementation has not started. The
> working revision and exact test command are attached in the actual issue.
> Next: implement the missing-file diagnostic, rerun the focused checks, then
> run the required local checks. No blocker or policy decision is outstanding.

In real work, include resolvable source and evidence references rather than the
descriptive stand-ins above. The next agent reads the issue and comments,
confirms the working state, and continues. It does not invent a second backlog
or ask the owner to repeat the accepted policy.

## 5. Review the completed evidence

After implementation and documentation, the illustrative evidence mapping is:

| Acceptance | Evidence to record in a real review |
| --- | --- |
| Exit `2`, empty standard output, one diagnostic line | Exact missing-file regression command and passing result |
| Requested path, file-not-found reason, no stack trace | Assertions on standard error in that same regression |
| Valid input stays compatible | Existing valid-file regression command and passing result |
| Reference matches behavior | Executed example and inspection of the rendered documentation |

This table describes the required evidence; it is not a claim that these tests
exist or passed here. Record actual failed, passed, skipped, and unavailable
checks distinctly. Follow the [verification standard](../reference/verification.md).

The reviewer checks the acceptance, the implementation, the meaningful red and
green evidence, and the updated reference. If the agent notices an unrelated
encoding bug, it creates a separate bounded issue and does not expand this one.

## 6. Complete the work at the agreed boundary

The agent integrates after the required checks and review pass. It closes the
completed issue and updates the milestone only as justified by its exit
criteria. It reports the behavior delivered, verification, and any material
limits in a concise message a person can understand.

Publishing a release is a separate action under Parcel's accepted policy. The
agent asks when that action is requested; it does not reinterpret integration
permission as release permission.

You have now followed the path from a user's need to a bounded issue, observable
acceptance, recoverable execution, evidence, and completion. To use it for your
project, continue with [Adopt Agent Temper](../how-to/adopt.md).
