# Write documentation people can use

Use this guide when a change needs a new page or changes existing instructions.
The result is a focused document with verified facts and a clear place in the
project's navigation.

Before you start, read the accepted work item and the project's documentation
policy. Identify the implemented behavior or decision that the page describes.

1. **Name the reader's task.** Write one sentence stating what the reader will
   learn, do, look up, or understand. Choose the form from the
   [documentation standard](../reference/documentation.md).
2. **Find the existing source of the facts.** Update that page where possible.
   If a new page is needed, link to shared facts rather than copying them.
   Use the [how-to template](../../templates/how-to.md) for a procedure.
3. **Write the shortest complete path.** State prerequisites, then ordered
   actions and expected results. Place conditions before their actions. Put
   detailed rationale in an explanation page when it interrupts the task.
4. **Check the technical content.** Follow the procedure from its stated starting
   point in an appropriate disposable fixture. Confirm commands, filenames,
   outputs, links, supported versions, and material failure recovery. Do not
   execute an externally consequential step without the required authority.
5. **Read the rendered page.** Check heading order, table width, code blocks,
   image descriptions, and navigation. Read it as someone who has not seen the
   issue discussion. Remove anything that does not help that reader.
6. **Deliver it with evidence.** Update the relevant README or index link. Record
   the checks actually performed and any unavailable checks in the work item
   or review. Request the review required by project policy.

The page is ready when a reader can reach it, follow its stated path, and
recognize success without guessing. A link check alone is not sufficient.

If the implementation and an approved contract disagree, record the conflict in
the work item. Resolve which behavior is intended before presenting either one
as the current contract. For a documentation-only correction, use source and
procedure validation; do not invent a failing runtime test.
