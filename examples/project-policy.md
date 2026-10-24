# Example: Quay project policy

This fictional example illustrates a completed policy for a small inventory CLI.
Names, commands, permissions, and the revision below are illustrative. They are
not evidence of an existing project, release, approval, or successful execution.

## Adoption and purpose

Quay prints local inventory reports for small workshop operators. It does not
manage accounts, synchronize services, or make purchasing decisions.

The project adopts Agent Temper and its GitHub profile through `.agent-temper/`.
The illustrative upstream revision is
`1111111111111111111111111111111111111111`, a synthetic value that must never be
used for real adoption. A real project records a verified immutable upstream
commit and file manifest in `.agent-temper/SOURCE.md`.

The repository owner approves changes to this policy through an issue decision
and reviewed policy change. The product contract is `docs/reference/cli.md`;
architecture is `docs/explanation/design.md`. No adopted-rule exceptions apply.
Missing or conflicting required policy stops dependent work until the owner
answers. Settled decisions remain effective until explicitly revised.

## Technical and documentation decisions

- Python 3.12 is the only implementation language. Its standard library is the
  dependency baseline. Packaging configuration uses TOML.
- Linux and macOS are supported. Windows support is outside the current scope.
- Agents may organize internal functions within the existing CLI design. Adding
  a runtime dependency, language, network access, or persistent service needs
  owner approval.
- Input is local JSON. Reject malformed input; do not execute input as commands.
  Tests use synthetic data. Never commit real inventory or credentials.
- Original contributions use BSD-3-Clause. Contributors must have the right to
  submit included material; copied third-party assets need compatible licensing.
- README covers purpose, installation, quickstart, checks, and navigation. Docs
  separate tutorials, how-to guides, reference, and explanation. Instructions use
  STE-informed plain English without claiming ASD-STE100 compliance.

## Work and verification decisions

GitHub Issues are the sole live work authority. Use the adopted GitHub profile's
progress labels. The owner assigns `priority:high`, `priority:normal`, or
`priority:low`; select in that order, then by the oldest ready issue. An issue
must be owner-approved or within an already authorized milestone before starting.
The assignee or ownership comment names the current implementer. Blocking issues
are explicit.

Milestones describe complete user capabilities with exit conditions. Small
maintenance issues may have no milestone. Bugs require a failing reproduction;
new behavior uses test-first development. The owner must approve a bounded
exception with alternative evidence. Documentation uses source and link checks.

| Purpose | Command and environment |
| --- | --- |
| Setup | `python3.12 -m venv .venv`; no network dependency installation needed. |
| Focused tests | `.venv/bin/python -m unittest tests.test_report` |
| Full behavior tests | `.venv/bin/python -m unittest discover -s tests` |
| Formatting, lint, and static checks | `.venv/bin/python tools/check_source.py` checks the project's small source conventions and syntax; no separate type checker is required. |
| Documentation | `.venv/bin/python tools/check_docs.py` |
| Build | Not applicable: the distribution is Python source without a generated build. |

CI runs the same source, behavior, and documentation commands on both supported
systems. CLI output changes also require a recorded command-line example using
synthetic input. Network integration and production validation do not apply.
Acceptance, applicable checks, updated documentation, and independent review must
pass before integration; report any unavailable check instead of claiming a pass.

## Agent authority

Agents may implement accepted scope, add tests, update docs, create bounded issues,
commit, push working branches, and open pull requests. They may update progress
labels and dependency records. The owner approves priorities, milestone scope,
product tradeoffs, and policy changes.

A separate reviewer must inspect the final change and its evidence. Agents may
merge to `main` after all required checks and review pass. They must ask the owner
before publishing releases, creating version tags, or distributing packages.
There is no production service. Deployment, secret access, spending, destructive
actions, and communication outside authorized repository work require approval.
