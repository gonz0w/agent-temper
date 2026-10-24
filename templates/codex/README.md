# Codex role templates

Use these only when the project explicitly selects the
[Codex profile](../../profiles/codex.md). Follow
[Configure Codex model routing](../../docs/how-to/configure-codex.md) to copy them
from a pinned revision, resolve local policy, and verify them in the intended client.
Files here are source templates; Codex does not load this directory as project roles.

| Template | Assignment |
| --- | --- |
| [temper_workflow.toml](agents/temper_workflow.toml) | Routine inspection and summaries with Luna. |
| [temper_implementer.toml](agents/temper_implementer.toml) | Bounded implementation and checks with Sol. |
| [temper_analyst.toml](agents/temper_analyst.toml) | Difficult investigation or separate complex review with Astra. |
| [temper_reviewer.toml](agents/temper_reviewer.toml) | Separate final review with Sol. |

After adaptation, these belong in the consumer's `.codex/agents/` and are local
project configuration. Preserve unrelated roles and personal settings. Set both
model and effort when changing a route, and record supported alternatives and
fallbacks in project policy. Template changes upstream do not replace local files.

The instructions assume the lead supplies the applicable policy, work item,
source context, acceptance, and ownership boundaries. They return evidence to
that lead. Model selection does not grant permissions, and read-only instructions
do not create an isolated read-only sandbox.

Parse with Python's standard-library `tomllib`, then verify discovery and actual
spawn settings in Codex using the guide. No API application, new package, or
user-level default change is required by these templates. Syntax validation alone
does not establish availability, correct routing, quality, or cost savings.
