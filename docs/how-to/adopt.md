# Adopt Agent Temper

Use this guide to establish the method for one project. The result is a local,
offline-readable copy of a reviewed upstream revision, an approved project
policy, and a short agent entry point.

Adoption changes how the project defines and delivers work. It does not choose
the project's language, replace its product contracts, or grant new integration
or release authority.

## Before you start

Obtain authorization to adopt the method. Create a bounded adoption work item in
the project's current tracker. For an existing project, first follow the
inventory and policy steps in [Retrofit an existing project](retrofit.md).

Select a reviewed Agent Temper source revision. Until a release is published,
use an exact reviewed commit; do not assume a version tag exists. A branch name,
moving tag, or “latest” is not an immutable pin. If a release is selected later,
record its underlying immutable source identity as well as its release name.

The core is independent of version control. The example below retrieves a
revision from this Git-hosted repository. A project that uses another version
control system can import the same files and record the same source identity
and checksums in its own system.

## 1. Resolve project decisions

Work through the [onboarding questions](../../templates/onboarding.md) with the
authorized decision maker. Existing clear, approved policy can supply answers.
Ask about missing or contradictory decisions before work depends on them.

Record the answers in `PROJECT.md`, using the
[project-policy template](../../templates/project-policy.md). Include the work
tracker, languages, supported platforms, checks, review requirements, and agent
authority for integration and release. Record who may change each policy and
how a change becomes effective.

Keep the distinction between an unresolved decision and a decision that
delegates routine choices to agents. Once accepted, these answers persist
across agents and sessions. An upstream update does not change them.

## 2. Copy and identify the upstream bundle

Keep upstream files under `.agent-temper/` with their original paths:

```text
.agent-temper/
  LICENSE
  METHOD.md
  SOURCE.md
  SHA256SUMS
  docs/reference/
  profiles/
```

`METHOD.md`, `docs/reference/`, `profiles/`, and `LICENSE` are the upstream
bundle. `SOURCE.md` and `SHA256SUMS` are local provenance records. The bundle's
internal relative links remain usable offline. Links to external sources still
need network access.

For this optional shell example, you need Git, `tar`, and either `shasum` or
`sha256sum`. No new runtime package is required. Start in the consumer project's
root. Set and export `AGENT_TEMPER_SOURCE` to the source checkout directory and
`AGENT_TEMPER_REVISION` to the full reviewed commit ID. The destination
`.agent-temper` must not already exist.

```sh
sh <<'SH'
set -eu
: "${AGENT_TEMPER_SOURCE:?Set the Agent Temper source checkout directory}"
: "${AGENT_TEMPER_REVISION:?Set the full reviewed commit ID}"
test ! -e .agent-temper
revision=$(git -C "$AGENT_TEMPER_SOURCE" rev-parse --verify \
  "$AGENT_TEMPER_REVISION^{commit}")
test "$revision" = "$AGENT_TEMPER_REVISION"
if command -v shasum >/dev/null 2>&1; then
  hash_file() { shasum -a 256 "$1"; }
elif command -v sha256sum >/dev/null 2>&1; then
  hash_file() { sha256sum "$1"; }
else
  printf '%s\n' 'Install or use an approved SHA-256 tool first.' >&2
  exit 1
fi
archive=$(mktemp)
trap 'rm -f "$archive"' 0
git -C "$AGENT_TEMPER_SOURCE" archive --format=tar --output="$archive" \
  "$revision" METHOD.md docs/reference profiles LICENSE
mkdir .agent-temper
tar -xf "$archive" -C .agent-temper
(
  cd .agent-temper
  find METHOD.md docs/reference profiles LICENSE -type f -print |
    LC_ALL=C sort |
    while IFS= read -r path; do hash_file "$path"; done > SHA256SUMS
  printf '# Agent Temper source\n\nRepository: https://github.com/gonz0w/agent-temper\n\nRevision: `%s`\n\nSource: https://github.com/gonz0w/agent-temper/tree/%s\n\nManifest: `SHA256SUMS` (SHA-256 per upstream file).\n' \
    "$revision" "$revision" > SOURCE.md
)
SH
```

Expected result: `.agent-temper/SOURCE.md` identifies the reviewed source, and
`SHA256SUMS` lists every copied upstream file. The copy comes from the committed
revision, so uncommitted changes in the source checkout are excluded. Review
the diff and manifest before accepting them. Checksums detect byte changes;
they do not by themselves establish that a source is trustworthy.

If the command fails after creating `.agent-temper`, inspect the partial copy
before retrying. Do not overwrite an existing adoption with this procedure;
use [Update Agent Temper](update.md).

## 3. Add local entry points

Use the templates from the same selected revision. Copy
`templates/project-policy.md` to `PROJECT.md` and `templates/AGENTS.md` to
`AGENTS.md` only when those destination files do not exist. For existing files,
edit their content through the approved transition instead of overwriting them.

For a new project, this command extracts the two templates from the pinned
source rather than the source checkout's working files:

```sh
sh <<'SH'
set -eu
: "${AGENT_TEMPER_SOURCE:?Set the Agent Temper source checkout directory}"
: "${AGENT_TEMPER_REVISION:?Set the full reviewed commit ID}"
test ! -e PROJECT.md
test ! -e AGENTS.md
git -C "$AGENT_TEMPER_SOURCE" show \
  "$AGENT_TEMPER_REVISION:templates/project-policy.md" > PROJECT.md
git -C "$AGENT_TEMPER_SOURCE" show \
  "$AGENT_TEMPER_REVISION:templates/AGENTS.md" > AGENTS.md
SH
```

Replace all template placeholders. Make the agent entry point link to
`.agent-temper/METHOD.md`, the selected profile, and `PROJECT.md`. Add a short
README link so people can find the policy. Retain only the templates the project
actually uses; they are local project content after adaptation.

Keep project extensions outside `.agent-temper/`. An exception must name the
upstream rule, the replacement, its scope, reason, approving authority, and any
expiry or review condition. A conflict is not resolved by whichever document
the agent happens to read first. Use the precedence and decision rules in
[the method](../../METHOD.md).

## 4. Verify and accept adoption

From `.agent-temper`, run `shasum -a 256 -c SHA256SUMS`, or
`sha256sum -c SHA256SUMS` when using that tool. Each listed upstream file should
report `OK`. Review the file list too: a checksum check alone does not detect an
extra file. Confirm that no unexpected policy was added inside the bundle.

Follow the local agent entry point with network access unavailable. Confirm
that the method, selected profile, and project policy can be read and their
internal links work. Then select a sample ready work item and identify its
acceptance, required checks, review, and integration authority. Do not claim a
live remote tracker is available offline.

Record the revision, manifest review, checks, resolved decisions, and any
limitations in the adoption work item. Integrate using the project's approved
process. The resulting source revision is the project's adopted authority;
future upstream changes require an explicit update.
