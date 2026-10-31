# Contribute to Agent Temper

Start with a bounded [GitHub issue](https://github.com/gonz0w/agent-temper/issues).
Read its comments, the [project policy](PROJECT.md), and the [method](METHOD.md).
An issue must explain the outcome, scope, acceptance, dependencies, and validation.

Use the [bounded delivery workflow](docs/reference/workflow.md#select-ready-work).
Related issues may share one PR with explicit membership and completion conditions.
Record unrelated discoveries for later selection; do not grow an accepted batch.

## Make a useful change

1. Record a short approach in the issue. Ask about missing policy before affected work.
2. Make one coherent change. Keep source claims, proposed rules, and observed results distinct.
3. Update the affected examples and instructions. Prefer clearer text to another tool.
4. Run the relevant checks and `python3 tools/verify.py` from the repository root.
5. Open a PR to `main`. Link each completed issue with its own closing line and map
   its acceptance to actual verification.
6. Obtain a separate review of the final change, resolve findings, and wait for
   current required CI. Merge only under [the recorded authority](PROJECT.md).

The [review template](templates/review.md) provides the expected evidence shape.
Record commands, results, skipped/unavailable checks, and limits. Prose needs real
source/link/reader checks, not artificial runtime tests. Changes to executable
checks need meaningful regression tests run red before implementation and green
afterward. Preserve expectations through refactoring.

## Write for readers

Follow the [documentation method](docs/reference/documentation.md). Keep the root
README short enough to find the first useful action. Put details at their canonical
home and link them. Use relative links for repository documents. Keep live work
status in GitHub; examples must be clearly fictional.

The core method must remain independent of GitHub, Git, agent products, languages,
and operating systems. Put concrete commands and service behavior in profiles or
task guides. A new rule should address a demonstrated failure or a necessary
contract, with explanation proportionate to its cost.

## Rights and public content

By contributing, you confirm you may contribute the material under
[BSD-3-Clause](LICENSE). Retain required attribution. Do not upload secrets,
private project content, personal environment details, or third-party standards.
Follow [SECURITY.md](SECURITY.md) for sensitive findings.

