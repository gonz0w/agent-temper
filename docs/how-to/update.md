# Update an adopted method

Use this guide to move one project from its recorded Agent Temper revision to
another reviewed revision. Local decisions stay in effect until an authorized
change explicitly replaces them.

Before you start, read the current `.agent-temper/SOURCE.md`, its checksum
manifest, `PROJECT.md`, and the project's policy-change authority. Open a
bounded update work item in the authorized tracker.

Before editing, record the scope, applicable gates, and authority using the
[adoption preflight](preflight-adoption.md). Keep that record in the owning issue.

1. **Verify the current copy.** Run its recorded SHA-256 check and inspect the
   file inventory. If files differ, establish why before replacing them. Preserve
   legitimate local changes as explicit policy extensions; do not silently
   erase them or treat an edited bundle as a clean upstream source.
2. **Select the candidate.** Record an immutable upstream source identity and,
   when applicable, its release name. Read the changes between the adopted and
   candidate revisions, including removed rules and affected templates.
3. **Assess the effect on this project.** Identify changed obligations, command
   requirements, current exceptions, and active work. Resolve new policy gaps
   or conflicts with the authorized decision maker. Recheck selected profile and
   extension dependencies, compatibility, local mappings, and verification. New
   files in the candidate bundle do not select new profiles. Record deliberate
   supersession where a previous decision changes.
4. **Prepare the candidate separately.** Follow the copy procedure in
   [Adopt Agent Temper](adopt.md) from an empty disposable directory. Preserve
   the bundle paths and generate a new `SOURCE.md` and `SHA256SUMS`. Compare its
   contents with the current copy before replacing the tracked bundle.
5. **Update the project coherently.** Replace the upstream bundle as a unit.
   Update local references, explicit exceptions, and selected templates only
   where the accepted update requires it. Remove upstream files deleted by the
   new revision. Removing or replacing a selected profile needs the recorded
   change authority and a coherent update to dependent rules and references. Keep
   a recoverable source revision of the previous adoption.
   If selecting or updating Codex routing, follow [Configure Codex](configure-codex.md).
   Merge adapted `.codex/agents/` files separately from the upstream bundle; a
   bundle update does not install roles or change the active chat's model.
6. **Verify the result.** Check the manifest and inventory, follow internal links
   offline, and walk a representative ready work item through the revised
   rules. Run any local checks affected by the change. Record actual results
   and unresolved limitations in the update work item.
7. **Review and integrate.** Use the project's recorded authority. Record the
   effective revision and any transition rule for already active work. Close
   the update item when its acceptance criteria are met.

Expected result: the project has one identified upstream revision and one set
of explicit local decisions. There is no automatic update from a moving branch.

If the candidate is rejected, leave the adopted revision in place and record
the reason in the update item. Use the
[adoption feedback route](../reference/extensions.md#feed-useful-findings-back) when
the finding justifies a shared improvement. If a defect appears after integration,
restore the previous adopted revision through the project's normal change process,
including any local policy change that the rollback requires.
