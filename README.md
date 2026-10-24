# Agent Temper

**The engineering discipline for software agents.**

Clear issues. Simple designs. Verified delivery.

Agent Temper gives software agents a repeatable way to turn an agreed outcome into
working software that people can understand, review, and maintain. It covers work
tracking, project decisions, implementation, testing, documentation, review, and
delivery. Each project chooses its tools and records its policies once.

The method is independent of language, version control, forge, and agent vendor.
The first concrete profile uses GitHub Issues and pull requests. Reading and using
the method requires no installed tool, service, or agent framework.

## Start here

| Your goal | Start with |
| --- | --- |
| Understand the method | [The core method](METHOD.md) |
| See a complete example | [Take an issue through delivery](docs/tutorials/first-issue.md) |
| Set up a project | [Adopt Agent Temper](docs/how-to/adopt.md) and [onboarding questions](templates/onboarding.md) |
| Improve an existing repository | [Retrofit a project](docs/how-to/retrofit.md) |
| Write useful documentation | [Documentation method](docs/reference/documentation.md) |
| Contribute here | [Contribution guide](CONTRIBUTING.md) and [project policy](PROJECT.md) |

## What changes when a project adopts it

- Work has one authoritative tracker, bounded outcomes, and observable acceptance.
- Agents ask about missing or conflicting project policy before dependent work.
- Recorded decisions persist until an authorized change replaces them.
- Implementation stays within the agreed scope and uses the smallest suitable design.
- Tests, documentation, and review show what the change actually delivers.
- People receive clear setup instructions, understandable changes, and honest limits.

Adoption is an explicit project change. It does not change permissions, select a
language, migrate a backlog, or authorize deployment. Projects pin a reviewed
framework revision and keep their own choices in a project policy.

## Status and scope

This is the initial draft. The method, templates, and local checks are available
for evaluation. Cross-project effectiveness has not yet been established by pilots.
There is no published release to pin; use an exact reviewed source revision until
a release is approved. See [work in GitHub](https://github.com/gonz0w/agent-temper/issues)
for current assignments and [milestones](https://github.com/gonz0w/agent-temper/milestones)
for capability goals.

The repository contains original guidance, reusable Markdown templates, and small
Python checks. It does not contain an agent runtime, a hosted documentation stack,
or a required collection of development tools.

## Validate a checkout

Use Python 3.11 or later. From the repository root, run:

```sh
python3 tools/verify.py
```

This runs the checker regression tests and offline document checks. It needs no
network connection, package installation, or Git metadata. See
[check coverage and limits](tools/README.md). A passing result does not establish
the correctness of the method or formal ASD-STE100 compliance.

## Find your way

- [Documentation index](docs/README.md): learning, task guides, reference, and rationale.
- [Templates](templates/README.md): copy only the documents a project needs.
- [GitHub profile](profiles/github.md): map the method to issues and reviews.
- [Sources and acknowledgements](docs/explanation/sources.md): where the ideas came from.
- [Security](SECURITY.md), [contributing](CONTRIBUTING.md), and [BSD-3-Clause license](LICENSE).

