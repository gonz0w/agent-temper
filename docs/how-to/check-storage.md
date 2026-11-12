# Check storage before generating output

The optional [storage guard](../../tools/storage_guard.py) uses Python 3.11+ and
its standard library. It reads metadata and Git objects; it never deletes files,
installs hooks, rewrites history, starts workloads or grants cleanup authority.
Copying this tool or adopting the lifecycle prose does not wire it into a runner.

## Choose and enforce a finite budget

In local project policy, record output roots including external run directories,
a combined peak allocation estimate for concurrent work, an allocated-output
budget, a minimum free-space reserve, and an owner for retained exceptions.
For a workstation, 20 GB of ordinary disposable output per repository and a
200 GB free-space reserve are starting recommendations, not universal defaults.
Image builders need a justified larger budget and shared input accounting. Small
CI workers need their own explicit limits. Bytes below use decimal GB.

Create the owned output directory, then run before the allocating step:

```sh
python3 tools/storage_guard.py preflight --output .build \
  --budget-bytes 20000000000 --reserve-bytes 200000000000 \
  --peak-bytes 2000000000
```

Repeat `--output` for other retained output locations on the same filesystem.
Run separately for different filesystems, each with its own peak and budget.
A missing directory, traversal error or invalid limit fails closed. Exit 0 means
the measured snapshot fits; 1 means a limit failed; 2 means checks were unavailable.
Stop dependent allocation on either nonzero result. The command prints compact
byte accounting for the work record, not a new retained binary report.

The scan counts allocated blocks once per inode and does not follow symlinks.
List symlink targets explicitly when they hold output. Nested mounts require a
separate invocation. Shared copy-on-write blocks can be counted more than once;
this is a conservative budget measurement, not guaranteed recoverable space.
A scan is not atomic and reserves no space. The runner must coordinate concurrent
writers, estimate their combined peak and recheck before new substantial stages.
It must not bypass a failed check by omitting output roots or lowering estimates.

## Keep generated binaries out of new Git changes

Run after staging and before committing:

```sh
python3 tools/storage_guard.py staged --repo .
```

Git is required for this subcommand only. The guard checks newly staged or changed
index blobs, including partially staged content. It refuses blobs larger than
10 MiB and common disk/media extensions, including small sparse-image stand-ins.
An explicit `--max-blob-bytes` chooses another documented local limit. A genuine
source asset can use `--allow assets/example.img` only with an exact path and a
recorded local justification. An exception is not permission to commit test dumps.
Do not use wildcard exceptions. The check skips unchanged history and submodule
commits; it cannot assess a submodule's own content. It does not clean old objects.

The `staged` command is a pre-commit check. A clean CI index has nothing staged.
Use `python3 tools/storage_guard.py tree --repo .` after checkout to check every
blob in the current committed tree instead. Agent Temper runs this in its existing
Verify workflow. This also checks preexisting tracked assets, so consumer adoption
must review asset exceptions before enabling it. Neither command audits historic
or unreachable objects, nor prevents transfer of the checkout itself.
Ignore rules complement the guard but cannot block force-added or already tracked
artifacts. No hook installation or security configuration change is selected here.

## Finish owned runs without accumulating old data

A consumer runner should create a unique disposable workspace and retain only
small text command/result records, source/input digests, and diagnostics needed
for outstanding failures. Keep necessary source fixtures and reproducers. Make
cleanup run after success, failure and interruption, with exit-status preservation.
A later interrupted-run reconciliation must verify ownership before cleanup.
Cleanup can remove only that runner's expressly disposable files under existing
authority. Never use a repository-wide wildcard, age alone, or an ignored path as
proof that data is disposable. A runner must not remove shared input or backing
images. Preserve all bases referenced by surviving VM overlays and all active,
release, debugging or recovery holds. Prefer one verified canonical download
per identity and owned overlays instead of full copies for each attempt.

At handoff report allocated output before/after, free space, what remains and why,
and the event that permits its cleanup. If required evidence prevents meeting a
budget, stop new generation instead of discarding it. Integration into actual
runners requires consumer review, negative tests and their existing acceptance
gates; neither this example nor central integration proves consumer rollout.
