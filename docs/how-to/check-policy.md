# Check declared policy selections

Use the optional standalone `tools/check_policy.py` to inspect an explicitly
adopted local module selection record. It uses Python 3.11+ and the standard
library, reads inert files, and writes one JSON report to stdout. It performs no
network, Git, subprocess, consumer/role execution, check dispatch or file repair.
Reading the method requires none of these tools or metadata files.

## Select the record deliberately

First [compose the project policy](compose-policy.md). Keep rule prose in its
canonical Markdown home. For projects that benefit from structured selection,
use the [optional template](../../templates/policy-selection.toml), adapt its
placeholders and references, and obtain the normal owner approval. PROJECT must
explicitly name the record as its module selection home. Replace duplicated
selection lists with a pointer; do not create another permission authority.
Local module identity is bound to its containing consumer revision; retained
external provenance/trust remains a separate adoption/review responsibility.

The checker does not parse PROJECT prose, recognize approvals or establish that
the record was adopted. A passing report does not select it. Honor the consumer's
execution policy: an offline helper cannot permit itself on a prohibited host or
replace required native checks. The byte-integrity
[adoption auditor](audit-adoption.md) has a separate contract and is unchanged.

## Supply explicit inputs

Obtain the standalone script from reviewed Temper source through your approved
source process. Run it there or copy that single file to an approved tools
location; it needs no sibling module. The arguments are:

| Argument | Input |
| --- | --- |
| `--root` | Explicit physical project directory, absolute or relative to the caller. |
| `--manifest` | Project-relative `.toml` path; no absolute path or fragments. |
| `--as-of` | Explicit valid ISO calendar date `YYYY-MM-DD` used for comparison. The checker reads no clock and assumes no timezone. Use the project's agreed date convention and record it with the evidence. |

From the Temper checkout root, this command exercises the fictional Windows-game
selection files with a supplied comparison date:

```sh
python3 -B tools/check_policy.py --root examples/windows-game \
  --manifest policy.toml --as-of 2030-01-01
```

Expected result: exit 0, no errors and three declared modules: execution,
integration and verification. This exercises selection/reference structure only;
it does not run or qualify Windows, a game engine or a pipeline. Absolute root
and script paths work from an unrelated working directory. Inputs must remain
unchanged during inspection.

## Manifest contract

Schema 1 permits exactly `schema_version`, `modules` and optional `exceptions`.
`schema_version` must be integer 1; `modules` must be a list, including an explicit
empty `modules = []`. Entries declare selected modules; presence elsewhere in the
repository is irrelevant. The file contains no commands, includes or inheritance.

| Module field | Contract |
| --- | --- |
| `id` | Unique within modules; start with lowercase ASCII letter, then lowercase letters, digits, `.`, `_` or `-`; at most 64 characters. |
| `path` | Project-relative `.md` file containing the canonical policy text. |
| `owner` | Nonempty printable owner identifier, at most 128 characters. This is declared identity, not authenticated approval. |
| `requires` | Optional unique ID list, default empty; every required ID must be selected. |
| `conflicts` | Optional unique ID list, default empty; a conflict with a selected module is an error, including one-sided declarations. References to unselected modules are allowed. |

Module dependencies must form an acyclic graph. Mutual prose references do not
necessarily imply dependency; declare actual selection prerequisites coherently.
The tool reports declared cycles/conflicts and cannot discover undeclared natural
language contradictions, duplicate prose rule IDs or incorrect supersession.

Optional `[[exceptions]]` entries declare active allowances for inspection:

| Exception field | Contract |
| --- | --- |
| `id` | Same identifier shape; unique within exceptions. |
| `path` | Local `.md` approval/exception record; content is not interpreted. |
| `modules` | Nonempty unique list of selected module IDs. |
| `expires_on` | Optional ISO date string or TOML calendar date; valid through this date inclusive. Earlier than `--as-of` produces `expired_exception`. Timestamps are rejected. |
| `ends_when` | Optional nonempty printable event description, at most 128 characters. Its occurrence remains unverified and its prose is withheld from the report. |

At least one expiry field is required. Both may be present; an unexpired date
cannot establish that an event-limited allowance remains active. Actual approval,
rule/scope coverage, event expiry and current authority always require review.
Keep historical exceptions outside the declared active list and retain their
labeled records. Do not invent a date or approval to obtain a successful check.
Unknown fields, invalid types, repeated list IDs and oversized collections fail.

## Report and exit contracts

The report is deterministic for unchanged inputs and the same as-of date:

- `schema_version` and `as_of` identify this report and supplied comparison date.
- `modules` lists validated IDs, paths, owner identifiers and sorted relationships.
- `exceptions` lists validated IDs, paths, module IDs, date and event status.
- `errors` contains fixed messages/codes and safe collection/index or valid-ID
  locations, sorted by location and code. No document/event excerpts or absolute
  input paths are printed. Invalid arbitrary field names/values are withheld.
- `policy_conformance`, `selection_authority` and `execution_authority` always
  remain `unverified`; `limits` preserves interpretation boundaries.

Selected relative paths and owner identifiers are intentionally reported. Review
the report before sharing it; metadata can identify private projects or people.
Some valid entries may appear alongside errors; inspect the full report and exit.
Exit 0 means no supported mechanical error, including valid empty selection and
unverified event expiry. Exit 1 means inspection failed. Exit 2 is CLI usage,
including invalid as-of dates; argparse writes usage to stderr and may echo user
arguments. Do not publish that output blindly. No result grants action authority.

## Bounds and safety limits

Manifest size is at most 64 KiB; each referenced document is at most 256 KiB,
UTF-8 and regular. There are at most 64 modules and 64 exceptions, and each ID list
has at most 64 entries. Paths are at most 512 printable characters with exact
forward-slash-separated local components: no empty, `.` or `..` component,
backslash, drive/URI colon, query, fragment or absolute path. File spelling uses
lowercase `.md`/`.toml` suffixes; use the actual on-disk component spelling.
Roots, parent directories and inspected files must not be symlinks. Root parent
components are checked physically before simplification, including components
before `..`; valid traversal through real parent directories remains usable. Special files
and unreadable inputs fail before policy interpretation. No undeclared files or
Markdown links are scanned. Case-sensitive spelling depends on the filesystem;
reader/link review still checks portable names.

The tool checks components and regular-file types, and uses no-follow opens where
available. It is not a hostile concurrent-filesystem sandbox; keep inputs stable.
Normal reads may change access-time metadata. A successful source report supplies
no source authentication, policy approval, actual check selection, enforcement,
runtime, platform, release or security assurance. Available host/Linux fixture
checks do not establish a Windows execution support matrix.
