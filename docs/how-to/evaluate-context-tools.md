# Evaluate optional context tools

Use this guide to decide whether prompt caching, conversation compaction or
symbol navigation helps a project. These capabilities are optional. Start with
the existing client and scoped source search; add an integration only for a
present need. Follow the project's authority before installing tools, spending
money or changing configuration.

## 1. Identify the capability and the problem

In the owning work item, record the client/version, supported language and
configuration, observed problem, proposed change and unavailable measurements.
Distinguish a documented feature, an installed executable, a working integration
and a measured improvement on accepted tasks. Each needs different evidence.

| Capability | Question to answer | Useful fallback |
| --- | --- | --- |
| Prompt caching | Does this client reuse eligible input, and can the proposed change affect that reuse? | Keep current behavior and load only relevant material. |
| Compaction | Does a shorter conversation preserve correct continuation? | Use the canonical work record and current source to resume. |
| Symbol navigation | Does this integration find the required definitions and references for this project? | Use paths, scoped text search and direct source inspection. |

An unavailable control is a limit, not a setting to invent. Markdown instructions
cannot enable a provider capability or prove that a client used it.

## 2. Keep cacheable context correct

If the harness controls message construction, keep necessary stable instructions
and tool definitions consistently ordered. Append changing task material where
the supported message format permits it. Preserve instruction priority and all
required content. Do not pad prompts to reach a cache threshold.

Read changed policy and source even when doing so changes a reusable prefix.
Cached input does not establish that a previous observation remains current.
A fresh session is not proof of a cold cache. Check actual usage, eligible
boundaries and expiry when the client exposes them; otherwise record them as
unavailable. Retain automatic behavior unless a measured problem justifies tuning.

For example, [OpenAI prompt caching](https://developers.openai.com/api/docs/guides/prompt-caching)
is enabled by default on supported models. Explicit breakpoint and lifetime
controls depend on the model and API. Their existence does not make them valid
Codex configuration fields or controls in every agent client.

## 3. Check continuation through compaction

Before a long-task comparison, make the canonical work record sufficient to
resume: selected scope, source identity, unresolved review, failed or unavailable
checks and next action. A summary points to those records; it does not replace
required reading or become another work authority.

Compare the existing approach with the proposed compaction point. Check that the
agent retains exclusions, required negative cases and unresolved failures. Then
change source and policy between continuations and check that it rechecks them
and invalidates stale evidence. Include compaction generation, rereading,
recovery and effects on caching in the comparison. Do not require manual
compaction after every turn or tune a threshold from context size alone.

Codex documents [automatic compaction settings](https://learn.chatgpt.com/docs/config-file/config-reference)
and a [manual compact command](https://learn.chatgpt.com/docs/reference/slash-commands).
Check the intended client. An API's [opaque compacted context](https://developers.openai.com/api/docs/guides/compaction)
is different from a readable handoff; neither establishes correct continuation
without checking outcomes.

## 4. Check symbol coverage and freshness

Check the integration's language support, build flags, project root, index scope
and readiness. A tool may cover open files while missing other project files.
Compare results with independently identified declarations, definitions and
callers. Include unrelated names, comments and strings. Change a caller and check
that new locations appear and obsolete locations disappear.

Inspect surrounding contracts and search for configuration, generated or dynamic
references that the symbol tool may miss. Verify a proposed rename separately;
a reference lookup does not prove rename safety. Keep text search available when
the tool is absent, incomplete or slower to prepare than the task warrants.

For C/C++, [clangd describes its navigation features](https://clangd.llvm.org/features).
[Serena](https://oraios.github.io/serena/01-about/025_features.html) offers optional
agent-facing symbol tools, but its [installation and language dependencies](https://oraios.github.io/serena/02-usage/010_installation.html)
are additional project choices. An integration layer does not establish backend
coverage or remove the need for correct project configuration.

## 5. Record the decision

Use the existing [comparison procedure](../reference/verification.md#compare-agent-workflows)
and optional [work-item sections](../../templates/workflow-comparison.md).
Fix quality, checks, review, permitted tools, budget and stopping rules before
execution. Include setup, indexing, context processing, unsuccessful attempts,
review and repair. Preserve provider token definitions and distinguish cash
charges from subscription usage. Smaller output or a higher cache-hit rate is
not proof of lower whole-task cost.

Record retain, change or investigate with the actual evidence and limits. An
unexecuted quality or performance check remains unverified. Adoption by another
project still needs its own reviewed selection.

**Fictional reader example:** A small documentation project retains text search
and automatic cache behavior. A larger C project considers symbol navigation,
but its trial misses a required caller. It keeps the fallback and investigates
coverage before relying on the tool, even if the response is short and fast.
