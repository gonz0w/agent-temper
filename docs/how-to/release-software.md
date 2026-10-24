# Prepare a release and recovery procedure

Use this guide when an authorized project needs to publish or deploy software.
The result is a reviewed candidate, an executable project-specific procedure,
and a record of what was actually accepted. Preparation does not grant permission
to publish, deploy, contact users, or access production.

## Before you start

Read the project policy, accepted delivery issue, supported environments, and
existing release and incident procedures. Identify the release owner and each
required approval. Reuse those procedures; resolve missing decisions before the
action depends on them. A merged change alone is not a released product.

Use the [release record template](../../templates/release.md) in the authoritative
work item or release system. Link durable runbooks instead of copying them into
each release. Keep sensitive commands, credentials, and incident details in their
approved location; public records can identify evidence without exposing it.

## 1. Identify the candidate and delivery boundary

Record the immutable source revision, artifact identity or digest, build inputs,
supported target, and included changes. A release name alone may not identify the
bytes. When a build is required, use the project's maintained build procedure and
record its actual toolchain and dependency versions. State reproducibility limits.

Specify which events this work item accepts: integration, package publication,
deployment, or operation on a target. Keep later work linked and open. Select
checks for the product's real distribution path:

| Product | Check at the delivery boundary |
| --- | --- |
| Library | Install the candidate package in a supported consumer fixture and exercise its public interface. |
| Command-line tool | Install or unpack the candidate and run a representative command with known inputs and expected output. |
| Hosted service | Verify the deployed candidate on the permitted target, including a user task and relevant health signals. |

## 2. Prepare the checks and recovery path

Give each required check its working directory, environment, inputs, exact command
or manual steps, expected result, and stop condition. A smoke check is a small
test of the delivered artifact; it supplements the required test suite. Include
installation, configuration, compatibility, and migration checks where relevant.

Before changing a target, identify what would trigger recovery, who may perform
it, the retained known-good artifact, and the exact restoration and verification
procedure. Check that the artifact and recovery inputs are available. Record any
data backup and restoration rehearsal required by project policy.

An older binary may not read newly migrated data. If a change cannot be reversed
safely, state the safe-stop or forward-repair procedure and its authority. Do not
call that procedure a tested rollback. An unavailable required check blocks the
affected acceptance unless the project's authorized exception process resolves it.

## 3. Verify the candidate and obtain the required review

Exercise the candidate in an authorized fixture or staging environment. Record
the tested artifact, commands, outcomes, environment, and limitations. Keep test
failure, environment failure, and an unexecuted procedure distinct. If the artifact
or relevant inputs change, refresh the affected evidence.

Have the required reviewer inspect the release contents, evidence, compatibility,
recovery path, and user-facing instructions together. If publication or deployment
needs approval, present this concrete candidate and procedure to the authorized
decision maker. Follow recorded delegation when approval already exists.

## 4. Deliver and verify at the accepted boundary

Perform only the authorized delivery steps. Check that the published or deployed
identity matches the reviewed candidate. Run the specified checks at the actual
delivery boundary; a staging result does not establish production acceptance.

If a stop condition occurs, halt further rollout and follow the approved recovery
or incident procedure. Preserve diagnostic evidence in its permitted location.
Record the resulting state even when recovery is incomplete. A successful
rollback does not make the failed candidate acceptable.

## 5. Reconcile ownership and follow-up

Record what was published or deployed, where, when, by whom, and with what result.
Identify support and incident ownership, supported versions, known limitations,
and the next action for any unresolved issue. Close only work whose recorded
completion conditions are met. Track later rollout or product learning separately
through the [product discovery and feedback guide](discover-product.md).

## Fictional example: a command-line candidate

This is a paper exercise, not software supplied or commands executed by this
repository. Imagine **Tally**, a tool whose documented `total` command reads a CSV
column named `count`. Its release issue identifies candidate and known-good
artifacts by exact source and digest, and delegates replacement of a local test
installation to the release operator. Public publication still requires approval.

| Procedure in an owned test directory | Expected result or decision |
| --- | --- |
| Prepare `sample.csv` containing the header `count` followed by rows `1` and `2`. Run the installed candidate with `tally total sample.csv`. | Exit 0, standard output `3` followed by a newline, empty standard error; the input bytes stay unchanged. |
| Run `tally total absent.csv`, where that file does not exist. | Exit 2, empty standard output, one file-not-found diagnostic; no output file is created. |
| Suppose the valid-file check returns `2` as its total. | Record the candidate failure and stop publication. Do not change the expectation to fit the output. |
| Restore the recorded known-good installation using the project's verified installation procedure; rerun both checks. | Record the restored artifact identity and actual results. Leave the candidate repair issue open. |

The example assumes the command is read-only and the installation can be restored.
For a data-writing service, establish data compatibility and recovery separately.
Passing these two checks would establish only this smoke contract, not every
platform's support or the product's usefulness to users.
