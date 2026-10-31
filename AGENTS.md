# Agent Temper contributor instructions

Read [PROJECT.md](PROJECT.md), [METHOD.md](METHOD.md), and the selected GitHub issue
with its comments before editing. This repository owns the portable method and
adoption kit. Other repositories are outside the current task unless the owner
explicitly authorizes their adoption work.

- GitHub Issues own all live work, dependencies, approaches, and continuation.
  Create a bounded issue before implementation; do not maintain local plans or
  progress logs. Keep examples explicitly fictional.
- Select an explicit delivery batch under PROJECT.md. Related issues may share
  one PR; give discoveries a disposition before implementation and leave unrelated
  work for milestone prioritization. Follow the workflow's attempt and stopping rules.
- Use the [workflow](docs/reference/workflow.md) and [GitHub profile](profiles/github.md).
  Missing or conflicting required policy stops affected work for owner Q&A.
  Recorded decisions persist; routine choices are delegated by PROJECT.md.
- Keep the method tool-neutral and the Markdown readable for people. Write original
  STE-informed instructions without claiming ASD-STE100 compliance. Follow the
  [documentation reference](docs/reference/documentation.md).
- Validate prose through links, source checks, examples, and reader review.
  For checker behavior changes, run meaningful tests red before implementation,
  then green. Never invent historical execution or weaken assertions to hide failure.
- Run `python3 tools/verify.py`. Use Python 3.11+ standard library only for repository
  tooling. No package installation or JavaScript/TypeScript tooling is needed.
- Changes target `main`, link completed issues, and map acceptance to actual evidence.
  A separate reviewer must examine the final change; record the review and limits.
  Agents may merge after required checks and resolved review. Ask the owner before
  publishing a tag/release, deploying, changing permissions, or expanding authority.
- Do not publish private source excerpts, personal paths, credentials, member data,
  or the copyrighted ASD-STE100 standard/dictionary. Public examples are synthetic.

