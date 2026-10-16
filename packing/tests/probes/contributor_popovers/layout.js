() => {
  const panel = document.querySelector("[data-contributor-popover]");
  if (!(panel instanceof HTMLElement)) {
    throw new Error("Missing contributor popover");
  }
  const box = panel.getBoundingClientRect();
  const ids = Array.from(document.querySelectorAll("[id]"), (node) => node.id);
  return {
    left: box.left,
    right: box.right,
    width: window.innerWidth,
    pageWidth: document.documentElement.scrollWidth,
    duplicateIds: ids.filter((id, index) => ids.indexOf(id) !== index),
  };
};
