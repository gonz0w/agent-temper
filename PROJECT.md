# Agent Temper project policy

This file records the decisions for **this repository**. It is not a mandatory
technology or permission policy for projects that adopt Agent Temper.

## Purpose and scope

Provide a small portable method and adoption kit for agents developing software
that humans can use, understand, review, and maintain. The initial artifact is a
draft method, documentation, templates, and local validation. Consumer migration
and comparative pilots are later, separately scoped work. Do not claim measured
productivity improvements before those observations exist.

## Recorded decisions

Owner: `gonz0w`. On 2026-10-23 the owner confirmed public hosting, BSD-3-Clause,
integration after checks/review, owner approval for releases, and STE-informed
writing. The other choices below implement the authorized setup with a small
toolchain. These recorded choices persist until the authorized change process
replaces them; they are not all claimed as individual owner questionnaire answers.

| Area | Decision |
| --- | --- |
| Repository | Public `gonz0w/agent-temper`; separate from consumer repositories. |
| License | BSD-3-Clause for original code, prose, and templates; external sources retain their terms. |
| Work authority | GitHub Issues; one setup milestone and bounded executable issues. No local execution backlog or agent journal. |
| Source control | Git, default branch `main`, short-lived `codex/` branches, coherent descriptive commits; no mandatory Conventional Commits format. |
| Artifacts | Plain Markdown and optional consumer configuration templates; Python 3.11+ standard-library checks. No third-party packages or frontend/runtime stack. |
| Verification | `python3 tools/verify.py`; behavioral changes to checks use actual red/green regression tests; prose uses source/link/example/reader validation. |
| Review | A separate reviewer examines the final scope, evidence, and documents. An agent reviewer is permitted; review type and findings must be recorded. |
| Integration | Agents may merge an accepted issue after current required CI succeeds and review findings are resolved. Prefer squash merge for the bounded deliverable. |
| Release | Owner approval is required before publishing tags or releases. Initial setup does not authorize a release. |
| Deployment | No service or website deployment is in scope. Ask before introducing one. |
| Documentation | Reader-oriented structure with original STE-informed plain-English procedures. No formal ASD-STE100 compliance claim. |
| Standards adoption | This repository develops the method in METHOD.md. Consumers pin an immutable reviewed revision; upstream changes never silently change them. |

## Work selection

Use the progress labels in the GitHub profile. `priority:p0` identifies an urgent
authorized blocker, `priority:p1` current milestone work, and `priority:p2` later
work. Prioritize existing active work and reviews, then unblocked ready issues in
the current owner-accepted milestone. If otherwise equivalent, choose the older
issue number. Ask about a material priority conflict rather than inventing urgency.

An agent may mark accepted scope ready when its outcome, acceptance, checks,
dependencies, and authority are explicit. A new feature proposal or deferred item
does not become authorized merely because an agent supplied those fields. The
owner selects new milestones and expands product scope. Agents reconcile existing
milestone completion against its recorded exit criteria.

The Markdown/Python implementation choices follow the owner's requested lightweight
setup and existing dependency-free checks. Adding a runtime, language, service,
mandatory dependency, or materially different license requires an owner decision.

## Delegation and decision boundaries

Agents may investigate, propose issues, implement accepted scope, improve wording,
add relevant tests, update affected docs, create review branches/PRs, and resolve
routine implementation choices. They may create marked disposable local fixtures
and remove only their own fixtures after use. Parallel agents must have explicit
ownership and one lead for integration.

Ask the owner before changing core product direction, publishing releases,
deploying services, spending money, modifying access/security settings after initial
setup, destructive data/history operations, or modifying other repositories.
Initial repository creation, CI/protection configuration, and setup integration
were explicitly authorized. Do not infer future authority from that bootstrap.

If a required policy is missing or conflicts with applicable instructions, record
the question in the issue and ask the owner. Continue only independent work until
answered. Save the answer here or in a linked scoped policy before dependent work.
An issue comment alone is not a silent permanent override. State the old decision,
replacement, reason, authority, and affected documents when changing policy.

## Quality and support

The local verifier is tested on available host Python and Linux CI. Other systems
can read the method without any runtime. We do not claim a complete Python/OS
compatibility matrix from those checks. CI runs with a read-only token and no
third-party action. Branch protection requires the `Verify` status and a PR.
The recorded separate review supplies content review; GitHub approval count is
zero because a single-owner agent workflow cannot provide a second account's
approval automatically. Never describe this as enforced independent human review.

Required verification failures cannot be waived by the implementing agent. Record
an unavailable check or known baseline defect and obtain an explicit decision if
it prevents acceptance. An exception cannot fabricate evidence or expose secrets.

## Public information and maintenance

Use synthetic examples and primary-source references. Do not copy private project
material into this repository. Keep credentials, personal paths, logs, and tool
transcripts out of commits. Preserve third-party attribution and do not redistribute
ASD-STE100 or its dictionary under this repository's license.

Maintain documentation with the behavior it explains. Update policy through the
normal issue/review process, with owner decisions where required. Use observed
confusion, defects, and review burden to decide which rules should change.

