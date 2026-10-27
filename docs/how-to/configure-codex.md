# Configure Codex model routing

Use this guide to add the optional [Codex profile](../../profiles/codex.md) to one
project. The result is explicit routing for routine support, implementation,
product-facing work, complex analysis, and separate review. The core method stays tool-neutral.

## Before you start

Before editing, record the scope, applicable gates, and authority using the
[adoption preflight](preflight-adoption.md). Keep that record in the owning issue.

Use the project's authorized adoption/update work item. For an existing adoption,
follow [Update Agent Temper](update.md) to select a reviewed immutable revision
that includes this profile. For a new adoption, follow [Adopt Agent Temper](adopt.md).
Updating the bundle alone does not install roles or select the profile.

Check the intended Codex client and account for custom subagents and the selected
models. Read the current [subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents).
Project `.codex/` configuration requires a trusted project; follow the client's
normal trust process and managed policy. See
[configuration precedence](https://learn.chatgpt.com/docs/config-file/config-basic).
Do not change trust or permissions merely to make a failed test pass.

## 1. Select the policy

In `PROJECT.md`, explicitly select `.agent-temper/profiles/codex.md`. Record the
roles and models you can use, reasoning effort, unavailable-model fallback,
resource limits, and authority to change those choices. The profile table gives
starting defaults; a project may choose supported alternatives.

For the product route, select `temper_product` with Terra/medium and explicitly
record `temper_implementer` with Sol/high as its unavailable-model/tool fallback.
Preserve the existing four routes. Check the Terra client requirement in the
[profile](../../profiles/codex.md#record-the-local-selection).

Inspect existing project and personal Codex roles and defaults for name conflicts.
Keep the `temper_` names distinct or record a deliberate local rename. Preserve
existing permission settings, integrations, and unrelated configuration.

## 2. Copy the role templates from the pin

Start in the consumer repository root. Use the same exported
`AGENT_TEMPER_SOURCE` and full `AGENT_TEMPER_REVISION` as the bundle procedure.
You need Git, a POSIX shell, and Python 3.11+ for the checks below. The five target
files must not exist; existing roles need a reviewed merge instead of this copy.
This copy also rejects symlinked configuration directories or role files. If the
project intentionally shares configuration through symlinks, review that layout
and merge the roles at its authorized destination instead.

```sh
sh <<'SH'
set -eu
: "${AGENT_TEMPER_SOURCE:?Set the Agent Temper source checkout directory}"
: "${AGENT_TEMPER_REVISION:?Set the full reviewed commit ID}"
revision=$(git -C "$AGENT_TEMPER_SOURCE" rev-parse --verify \
  "$AGENT_TEMPER_REVISION^{commit}")
test "$revision" = "$AGENT_TEMPER_REVISION"
test ! -L .codex
test ! -L .codex/agents
roles='temper_workflow temper_product temper_implementer temper_analyst temper_reviewer'
for role in $roles; do
  test ! -e ".codex/agents/$role.toml"
  test ! -L ".codex/agents/$role.toml"
  git -C "$AGENT_TEMPER_SOURCE" cat-file -e \
    "$revision:templates/codex/agents/$role.toml"
done
mkdir -p .codex/agents
for role in $roles; do
  git -C "$AGENT_TEMPER_SOURCE" show \
    "$revision:templates/codex/agents/$role.toml" > ".codex/agents/$role.toml"
done
SH
```

Expected result: five role files under `.codex/agents/`, taken from the pinned
commit. If copying fails partway through, inspect the partial result before
retrying. Remove only files created by that failed attempt, or finish the reviewed
merge manually. Do not overwrite an existing role or unrelated configuration.

For an existing four-role adoption, merge the revised profile and policy, then
copy only the new product template from the selected pin. Preserve the adapted
existing roles. Do not rerun the new-install copy block over existing files.

These are adapted local project files, outside `.agent-temper/` and its upstream
checksum manifest. Review them into the consumer repository with the policy.
Keep both model and effort explicit when customizing; change the local policy
mapping with them. Future framework updates do not automatically replace them.

## 3. Connect the agent entry point

Add a short instruction to the existing `AGENTS.md`, preserving its other rules.
For a project that accepted the default role names, this is example text:

```text
Apply the Codex routing profile selected in PROJECT.md. When useful, delegate
bounded routine inspection to temper_workflow, accepted product-facing work to
temper_product, accepted implementation to
temper_implementer, difficult analysis to temper_analyst, and final separate
review to temper_reviewer. Supply the issue, applicable policy, relevant files,
acceptance, and edit boundaries. Follow the profile's escalation and fallback
rules; the lead owns integration and verifies the returned evidence.
```

The standalone role files are sufficient for named roles on a supporting client.
Optionally merge these defaults into the existing `.codex/config.toml` if the
project wants Sol for otherwise unspecified subagents. Merge into an existing
`[agents]` table; do not append a second table or replace the whole file.

```toml
[agents]
default_subagent_model = "gpt-6.1-sol"
default_subagent_reasoning_effort = "high"
max_concurrent_threads_per_session = 3
```

This example limits concurrent spawned threads to three, excluding the primary.
Explicit spawn settings override these defaults; named role files override their
model/effort values. This does not select the primary chat's model. Choose a limit
under the project's resource policy. See the
[configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

## 4. Check configuration and actual routing

From the consumer repository root, parse the installed files:

```sh
python3 - <<'PY'
from pathlib import Path
import tomllib

roles = ('temper_workflow', 'temper_product', 'temper_implementer', 'temper_analyst', 'temper_reviewer')
for role in roles:
    path = Path('.codex/agents') / f'{role}.toml'
    data = tomllib.loads(path.read_text(encoding='utf-8'))
    for key in ('name', 'description', 'developer_instructions', 'model',
                'model_reasoning_effort'):
        assert isinstance(data.get(key), str) and data[key].strip(), (path, key)
    assert data['name'] == role, path
    print(f'{role}: {data["model"]} / {data["model_reasoning_effort"]}')
config = Path('.codex/config.toml')
if config.exists():
    tomllib.loads(config.read_text(encoding='utf-8'))
    print('Project config: TOML parsed')
PY
```

Expected result: five model/effort lines and no parse/assertion errors. Adapt the
role list if policy deliberately renamed roles. This checks syntax and required
fields, not model availability or Codex behavior.

Start a fresh Codex session in the consumer repository so it can discover the
new files. Ask it to delegate a bounded inspection to `temper_workflow`. Supply
the adoption issue and policy; ask for a summary of the selected routing rules
without edits. Inspect the actual spawned role and model/effort metadata exposed
by that client. Then exercise each other selected role with an appropriate
bounded task or read-only adoption check before relying on it for that role.

Record client/version, source revision, requested and observed settings, result,
and limits in the adoption issue. If the client lacks observable model metadata,
mark routing unverified. If roles or models are unavailable, use the recorded
fallback; do not infer success from the assistant claiming its model name.
Validate any runtime-specific spawn mapping separately. An existing chat or
already spawned agent does not automatically switch models after files change.

## 5. Accept and maintain the selection

Review the policy, agent instructions, and role files together. Run the project's
required checks, then integrate through its existing process. Keep a recoverable
previous revision. If the setup fails, restore only the affected local policy and
configuration through that process; leave unrelated configuration intact.

Assess benefit on representative work using the profile's evaluation guidance.
This kit provides routing defaults, not measured savings. Revisit settings with
client/model changes. Each existing repository needs its own explicit update;
an upstream merge or a new chat alone does not change its adopted pin or policy.
