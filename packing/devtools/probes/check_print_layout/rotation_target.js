// A rotation handle as a touch target: at least 44px square, a named native button, not
// covered where a finger lands, and holding its touch drag while the canvas beside it still
// lets a vertical swipe scroll the page. Returns one line per defect found.
/** @param {HTMLElement} handle */
(handle) => {
  /** @type {string[]} */
  const found = [];
  const box = handle.getBoundingClientRect();
  if (box.width < 44 || box.height < 44) {
    found.push("rotation target is smaller than 44px");
  }
  if (handle.tagName !== "BUTTON" || !handle.getAttribute("aria-label")) {
    found.push("rotation target is not a named native button");
  }
  const hit = document.elementFromPoint(box.x + box.width / 2, box.y + box.height / 2);
  if (!handle.contains(hit)) {
    found.push("rotation target is covered by another element");
  }
  if (getComputedStyle(handle).touchAction !== "none") {
    found.push("rotation target allows the browser to cancel its touch drag");
  }
  const stage = /** @type {Element} */ (handle.closest(".stage"));
  const canvas = /** @type {HTMLCanvasElement} */ (stage.querySelector("canvas"));
  if (getComputedStyle(canvas).touchAction !== "pan-y") {
    found.push("the canvas no longer permits vertical touch scrolling");
  }
  return found;
};
