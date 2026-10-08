/** @param {{observer: {completed: Promise<void>}}} options */
async ({ observer }) => {
  await observer.completed;
  return {
    open: document.querySelector("[data-case-popover]")?.matches(":popover-open") ?? false,
    expanded: [...document.querySelectorAll('tr[data-case-row][aria-expanded="true"]')].map((row) =>
      row.getAttribute("data-case-row"),
    ),
    active: document.activeElement?.getAttribute("data-case-row"),
  };
};
