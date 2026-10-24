# Retrofit an existing project

Use this guide after the project owner authorizes adoption. It produces an
explicit transition from existing practices to a pinned Agent Temper method.
It does not authorize changes to every repository that shares an owner.

Before you start, read the current repository instructions, active work, open
reviews, supported contracts, and evidence-retention rules. Use the current
authorized tracker for the retrofit work item.

1. **Identify the actual conflicts.** Inventory existing agent entry points,
   policies, trackers, CI entry points, README links, and decision records.
   Record concrete contradictions and duplicates in the retrofit issue. A
   different filename or directory layout is not by itself a defect.
2. **Resolve policy through Q&A.** Use the project-policy template from the
   [adoption guide](adopt.md). Retain existing approved decisions unless the
   authorized decision maker changes them. Ask about missing authority,
   conflicting policies, and the treatment of active work.
3. **Define the transition boundary.** State which documents and trackers will
   become authoritative, which rules are superseded, and when the change takes
   effect. Map active work and dependencies to their new records if a tracker
   changes. Preserve identifiers or links that let readers follow the history.
4. **Adopt a pinned bundle.** Follow [Adopt Agent Temper](adopt.md). Keep local
   extensions and approved exceptions outside the upstream copy. Do not silently
   replace stronger security, recovery, licensing, or evidence requirements.
5. **Repair navigation and remove competing instructions.** Replace obsolete
   entry points with concise pointers where readers still need them. Preserve
   consequential history and executed evidence in their required locations.
   Label historical material as historical; it must not assign new work.
6. **Validate the new route.** Start from the README and agent entry point as a
   fresh reader. Select a ready issue, find the policy, locate the required
   commands, and explain completion. Check moved links, packaging references,
   and any affected build paths. Confirm unrelated work is unchanged.
7. **Integrate through the existing authorized process.** Record checks and the
   final mapping of authority in the retrofit issue. After integration, confirm
   the expected tracker records and navigation work. Retain a clear way to
   restore the previous policy revision if the transition has a defect.

Reorganize directories only when the accepted issue identifies a concrete
navigation, ownership, packaging, or maintenance problem. Move a coherent set,
update its references in the same change, and preserve provenance. Broader
cleanup belongs in separate bounded issues.

An unresolved policy question blocks work that depends on the answer. It does
not authorize an agent to choose a new policy, discard history, or reopen an
already settled decision merely because the agent is new.
