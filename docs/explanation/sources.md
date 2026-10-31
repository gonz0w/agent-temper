# Sources and acknowledgements

Initial sources reviewed on 2026-10-23. These sources inform the design; they do
not automatically override the [method](../../METHOD.md) or a project's recorded adoption.
The prose and templates in this repository are original. External publications
retain their own licenses, copyrights, and trademarks.

| Source | How it informs Agent Temper |
| --- | --- |
| [Diataxis](https://diataxis.fr/) | Distinguish learning, completing a task, looking up facts, and understanding reasons. |
| [Applying Diataxis through work](https://diataxis.fr/how-to-use-diataxis/) | Improve useful documentation incrementally; avoid empty mandatory structures. |
| [ASD-STE100 official site](https://www.asd-ste100.org/) | Inform clear technical instructions and consistent terminology. The standard and dictionary are not included. |
| [ASD-STE100 downloads](https://asd-ste100.org/STE_downloads.html) | Obtain the official standard if a project separately requires formal conformance. |
| [GitHub agent task guidance](https://docs.github.com/en/copilot/tutorials/cloud-agent/get-the-best-results) | Define clear problems, bounded tasks, and acceptance criteria. |
| [GitHub issue closing behavior](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) | Map integration and issue closure accurately in the GitHub profile. |
| [OpenAI best practices](https://learn.chatgpt.com/guides/best-practices) | Keep agent instructions practical and concise, with useful verification context. |
| [Anthropic best practices](https://code.claude.com/docs/en/best-practices) | Give agents observable checks and inspect evidence rather than accepting assertions. |
| [DORA: small batches](https://dora.dev/capabilities/working-in-small-batches/) | Favor bounded changes and fast feedback. |
| [Martin Fowler: Yagni](https://martinfowler.com/bliki/Yagni.html) | Defer speculative capabilities while maintaining a design that supports current needs. |
| [Study of AGENTS.md efficiency](https://arxiv.org/abs/2601.20404) | One empirical study observed efficiency improvements under its evaluated conditions. |
| [Evaluation of repository context files](https://arxiv.org/abs/2602.11988) | Another study found no general task-success improvement and higher inference costs. Evaluate guidance on real work. |

The following primary sources were reviewed on 2026-10-24 for the product and
repository guides. The DORA small-batches source above was also rechecked.

| Source | Selected practice and adaptation |
| --- | --- |
| [Teresa Torres: Product discovery](https://www.producttalk.org/product-discovery/) | Distinguish user needs from solutions and test consequential assumptions. Use bounded discovery where the product direction is uncertain. |
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Make intended behavior explicit and carry it through implementation and verification. Its separate feature, bug, and assessment routes inform conditional guidance; its tools and file hierarchy are not adopted. |
| [DORA: User-centric focus](https://dora.dev/capabilities/user-centric-focus/) | Connect delivery to user needs and feedback. Record an outcome evaluation separately from implementation acceptance. |
| [C4 model: Diagrams](https://c4model.com/diagrams) | Select only useful architecture views. A repository map can link relationships and source without requiring every diagram level. |
| [Google SRE: Release engineering](https://sre.google/sre-book/release-engineering/) | Identify release inputs and artifacts, make procedures repeatable, and prepare verification and recovery. Adapt the practice to the project's scale and authority. |
| [GitHub: Administering issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/administering-issues) | Ground concrete issue intake, duplicate handling, and closure operations in the existing GitHub profile. |

The optional Codex profile and configuration guide use these official sources,
reviewed on 2026-10-24. Model routes are starting recommendations, not benchmarks.

| Source | Selected practice and adaptation |
| --- | --- |
| [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) | Standalone project role files, explicit model/effort, and inherited permission boundaries. |
| [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference) | Optional defaults and concurrency settings; preserve existing configuration. |
| [Codex configuration basics](https://learn.chatgpt.com/docs/config-file/config-basic) | Project trust and configuration precedence. |
| [OpenAI model selection](https://learn.chatgpt.com/docs/model-selection) | Match task difficulty and cost constraints, then evaluate the whole result. |

The bounded delivery guidance uses these primary sources, reviewed on 2026-10-31.
It selects individual practices rather than claiming full adoption of a framework.

| Source | Selected practice and adaptation |
| --- | --- |
| [The Kanban Guide, May 2025](https://kanbanguides.org/the-kanban-guide/2025.5/) | Explicit start/finish policies and work-in-progress control. Temper uses a project-adjustable default per integration lead; it prescribes no universal team capacity or service-level forecast. |
| [Shape Up: Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03) | Set outcome and effort boundaries before expanding a solution. Temper retains an authoritative issue backlog and project-specific budgets. |
| [Shape Up: The Betting Table](https://basecamp.com/shapeup/2.2-chapter-08) | Deliberate selection and a limit on automatic extensions. Temper checkpoints and replans exhausted attempts; it does not impose six-week cycles or waive required quality gates. |

Vendor guidance supplies examples, not required products. The research studies use
different tasks and setups and do not establish the effect of Agent Temper.
Official pages can move or restrict automated access. Offline link checks do not
prove that an external page remains reachable; verify external sources when their
claims matter to a change.

