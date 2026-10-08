/** Capture native close before its queued toggle event; optionally reopen a cached row.
 * @param {{reopen: number | null}} options
 */
async ({ reopen }) => {
  const popover = document.querySelector("[data-case-popover]");
  if (!(popover instanceof HTMLElement)) {
    throw new Error("No case popover");
  }
  const state = () => ({
    open: popover.matches(":popover-open"),
    expanded: [...document.querySelectorAll('tr[data-case-row][aria-expanded="true"]')].map((row) =>
      row.getAttribute("data-case-row"),
    ),
  });
  popover.hidePopover();
  const closed = state();
  if (reopen !== null) {
    const row = document.querySelector(`tr[data-case-row="${reopen}"]`);
    if (!(row instanceof HTMLElement)) {
      throw new Error("No reopening row");
    }
    row.click();
    // The cached record's promise resolves in this microtask checkpoint, before toggle.
    await Promise.resolve();
  }
  return { closed, reopened: state() };
};
