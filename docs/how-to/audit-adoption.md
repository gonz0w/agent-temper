# Audit an adoption without changing it

Use the optional offline auditor to compare one retained Agent Temper bundle with
a trusted local source copy and inspect explicitly selected Codex roles. It uses
Python 3.11+ and the standard library. It does not install, update, execute roles,
invoke Git or subprocesses, access the network, or write to either input.

## Prepare explicit inputs

First follow the [adoption preflight](preflight-adoption.md) in the owning issue.
Honor the consumer's execution policy: a read-only helper is not permission to run
Python on a prohibited host or replace a mandatory gate. This helper is optional,
outside the nine-file portable bundle, and not part of its checksum manifest.

Obtain `tools/audit_adoption.py` from a reviewed Temper source through your approved
source process. You can run it there or copy that single script to an approved
tools directory; it has no sibling-module dependency. Select a trusted source
export or clean checkout at the consumer's recorded full reviewed revision.
Prepare that copy through your existing authorized process, before the audit.
The auditor does not fetch, authenticate, or verify that checkout against Git.
A current upstream checkout at another revision is not the correct comparison.

Supply these inputs explicitly:

- `--consumer`: the consumer root containing `.agent-temper/`.
- `--source`: the local upstream source root containing the nine upstream files
  and, when comparing standard roles, their `templates/codex/agents/` files.
- `--revision`: the expected full 40-character lowercase hexadecimal revision.
  This compares a declaration, not a verified commit identity.
- `--role NAME`: repeat for each selected local role. Omit it for zero roles.
  Read the selection from approved policy yourself; the auditor never parses
  `PROJECT.md` or infers selection from files being present.

## Run the comparison

This fictional shell example runs from a parent directory containing `temper-source`
and `example-project`. Use your approved locations. It inspects one role only:

```sh
python3 -B temper-source/tools/audit_adoption.py \
  --consumer example-project \
  --source temper-source \
  --revision aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
  --role temper_product
```

The revision is synthetic; replace it with the reviewed source identity. Absolute
CLI paths also work from an unrelated working directory. Use physical directory
paths: inspected roots, parent directories and files must not be symlinks.
Parent components are retained for physical checking, including those before
`..`; traversal through real directories remains supported.
Keep inputs unchanged during the audit. No client or model needs to run.

Expected result for matching synthetic inputs: exit 0, `errors: []`,
`bundle_files_compared: 9`, the declared revision, and one role observation with
`template_comparison: "matches"`. Omitting `--role` produces `roles: []` without
inspecting `.codex/`. These are example expectations, not a real consumer audit.

## Interpret the JSON report

The command prints one deterministic JSON object to stdout, with no absolute
input paths or document/instruction excerpts. Diagnostics use fixed locations,
codes and messages; malformed manifest entries include their line number.
Unexpected entry names are withheld. Selected role names and model/effort
identifiers are intentionally reported; review the report before publishing it.

| Field | Meaning |
| --- | --- |
| `schema_version` | Report format version, currently 1. |
| `errors` | Audit failures, sorted by relative location, line and code. Repair or explain the input under local authority, then audit again. No repair is performed. |
| `bundle_files_compared` | Number of upstream files whose bytes could be compared, not the number that matched. Inspect `errors` too. |
| `declared_revision` | Supported SOURCE declaration matching the supplied revision, or null. It does not authenticate the supplied source. |
| `roles` | Observed name/model/effort for each valid selected local role, template comparison, changed required field names and whether additional fields differ. No field values from descriptions/instructions or additional fields are shown. |
| `limits` | Comparison boundaries that remain in force even with no errors. |
| `source_authenticity`, `policy_conformance`, `runtime_routing` | Always `unverified`. Model access, product behavior and actual selection are not exercised. |

Exit 0 means all supported inspections succeeded, including intentional valid local
customizations. Exit 1 means an input/comparison error was reported. Exit 2 means
CLI arguments could not be parsed; argparse writes usage diagnostics to stderr.
Usage errors can echo user-supplied arguments, so keep that output private too.
A successful report never grants merge authority or satisfies unspecified gates.

Role names must start with an ASCII letter and contain at most 64 ASCII letters,
digits, underscores or hyphens. Select each name once, with at most 32 roles.
Each TOML must have nonempty string `name`, `description`, `developer_instructions`,
`model` and `model_reasoning_effort`; `name` must match the selected filename.
Model/effort identifiers are limited to 128 ASCII letters, digits, `.`, `_`, `:`,
`/` or `-`, starting with a letter or digit. This checks identifier shape, not
provider support or valid effort choices for that model.

`matches` means parsed TOML values match the same-name source template; formatting
and comments are ignored. `customized` reports differences without rejecting
local choices. `unavailable` means no template comparison was possible; for a
renamed local role with no same-name template, this alone is not an error. Missing
standard `temper_` templates, malformed templates and unsafe inspected paths are
errors. Deliberate renames need human comparison with the intended upstream role.
Unselected roles, `.codex/config.toml` and role permissions at runtime are not checked.

## File contract and limits

This version expects these nine upstream files, plus local `SOURCE.md` and
`SHA256SUMS`, with no additional bundle entries:

```text
LICENSE
METHOD.md
docs/reference/documentation.md
docs/reference/extensions.md
docs/reference/verification.md
docs/reference/workflow.md
profiles/codex.md
profiles/github.md
profiles/strict-test-first.md
```

The manifest must list all nine files once. It may additionally list `SOURCE.md`
once, supporting both documented provenance layouts. Each line contains a
64-digit hexadecimal SHA-256 digest, one space, then a space or `*`, then an exact
listed relative filename. Uppercase digests are accepted. Blank/comment lines,
unknown paths, self-hashing, duplicates, absolute paths and traversal are rejected.
The checker never opens a path supplied by the manifest: it reads only fixed names.
A matching manifest alone cannot conceal a modified bundle from the source-byte
comparison. Neither comparison establishes source trust.

`SOURCE.md` must contain exactly one `Repository:` field with
`https://github.com/gonz0w/agent-temper`, and one `Revision:` field matching
`--revision`. A field may have a leading `- ` and its value may be backtick-wrapped.
Other prose, including source links, is not interpreted. Older/custom provenance
layouts need a deliberate reviewed adaptation or manual check; do not rewrite
historical records merely to obtain a successful report.

Each inspected file is limited to 1 MiB. Each bundle directory is limited to 32
entries, and only the fixed bundle directories are descended. Unexpected directory
contents are not traversed. Symlinks, special files, unreadable inputs, malformed
UTF-8 metadata and TOML are rejected. Bundle/source payload bytes need not be text.
Source files outside the nine names and selected templates are not inventoried.

This is a bounded comparison helper, not a hardened hostile-filesystem sandbox.
It checks path components and regular-file types and uses no-follow opens where
available. It does not defend against concurrent changes to parent directories.
Access-time metadata may change due to normal file reads. Reports are observations,
not policy interpretation, signature validation, proof of a clean checkout, or
[actual routing verification](configure-codex.md#4-check-configuration-and-actual-routing).
Use the [update procedure](update.md) for reviewed changes after investigating drift.
