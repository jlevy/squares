// A completed News transition has its target height; expanded content sizes itself.
(/** @type {{id: string, open: boolean}} */ { id, open }) => {
  const card = document.getElementById(id);
  const body = card?.querySelector(".site-news-body");
  const button = card?.querySelector(".site-news-expand");
  if (!(body instanceof HTMLElement) || !(button instanceof HTMLButtonElement)) {
    return false;
  }
  const target = open
    ? body.scrollHeight
    : Math.min(body.scrollHeight, 10 * Number.parseFloat(getComputedStyle(body).lineHeight));
  return (
    button.getAttribute("aria-expanded") === String(open) &&
    Math.abs(body.clientHeight - target) <= 1 &&
    (!open || body.style.maxBlockSize === "")
  );
};
