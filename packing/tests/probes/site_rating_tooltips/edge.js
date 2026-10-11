async () => {
  const badge = document.querySelector("#edge-table .site-significance");
  if (!(badge instanceof HTMLElement)) {
    throw new Error("Missing table badge");
  }
  window.scrollBy(0, badge.getBoundingClientRect().bottom - (window.innerHeight - 12));
  await new Promise((resolve) => requestAnimationFrame(resolve));
  badge.blur();
  badge.focus({ preventScroll: true });
  return badge.getBoundingClientRect().bottom;
};
