# Why the method has this shape

Agents need a clear outcome, relevant context, authority to act, and a way to check
their work. People need a coherent result and a usable explanation. Agent Temper
puts these needs in the same delivery loop.

## Separate durable meaning from live work

A project policy answers how a project operates. A work item answers what to do
next. A product reference answers how the software behaves. Copying live status
into all three creates competing instructions that age at different rates.
The method therefore assigns one owner to each kind of fact and links the rest.

## Use a small core and explicit local choices

Git, SVN, CVS, Jujutsu, and other systems represent history differently. Trackers
and agent products also change. The core uses work items, source identities,
reviews, and integration records; a profile maps those concepts to tools. A
source identity can be one revision or a manifest of file revisions and content.
No adapter is promised until its behavior is implemented and checked.

Projects choose languages and commands against their own requirements. A new
language or service is a continuing maintenance decision. A framework should
make that decision visible without imposing one stack on unrelated projects.

## Combine intent with feedback

An issue can be a sufficient specification for a small change. More complex
contracts need durable explanations. Test-first work gives fast feedback when
behavior can be exercised, but prose, exploratory research, and some environment
constraints need other evidence. The method requires honest validation rather
than a fabricated sequence of test results.

## Make adoption stable

An upstream edit must not silently change a project's operating rules. A pinned
offline copy makes the adopted material available to future agents and reviewers.
Updates are normal reviewed changes, with local Q&A where a new decision is needed.
The manifest helps detect accidental edits; it does not prove the source is trusted.

## Select practices for agent work

The supporting guides combine practices whose outputs can be inspected and resumed:

| Practice | Adaptation and reason |
| --- | --- |
| Continuous discovery | Separate needs, candidate solutions, assumptions, and observations so an agent can test an unknown before expanding implementation. |
| Specification-driven development | Keep agreed behavior and independent examples explicit, then reconcile implementation and evidence against them. A small issue can hold the specification. |
| DORA user focus and small batches | Deliver a usable increment and evaluate its intended benefit with a named owner and trigger. Passing technical checks does not establish that benefit. |
| C4 architecture views | Show only the boundaries and relationships needed to trace a task. Link source and tests from a compact map; diagrams are optional. |
| Release engineering | Tie delivery checks and recovery decisions to an identified artifact and target so a later agent can assess what happened. |

These are selected ideas, not wholesale framework adoption or a claim that one
method is best for all agents. Existing policy, tracker, and verification rules
remain authoritative. No additional runtime, mandatory document hierarchy, research
cadence, or release authority follows from the guides. The [sources](sources.md)
identify the primary material; adoption observations must establish local value.

## Evaluate before expanding

Instruction-file research has mixed results across tasks and agents. The sources
support useful hypotheses, not a promise that this particular framework improves
delivery. Pilots should examine completion, correction cycles, recovery after
interruption, escaped defects, review effort, and elapsed delivery time. Keep
rules that solve observed problems and simplify rules that create avoidable work.

See [sources](sources.md) for the research behind these choices.

