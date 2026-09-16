// A block the print column cannot contain, appended to the page. Given its margins and its
// width outright, because the column centres its blocks and caps their measure: a block
// merely handed a width comes back centred at half the overhang, which is how the first
// draft of this control quietly measured nothing. The same pass stretches one real list
// bullet to reproduce the glyph-to-box regression without another browser.
//
// Takes `{over, name, bullet}`: the overhang in CSS pixels, the block's class, and the class
// the stretched bullet is given.
/** @param {PrintLayoutSelfCheckSpec} spec */
(spec) => {
  const root = document.documentElement;
  const page = document.querySelector(".kpress");
  if (!page) {
    throw new Error("no .kpress column to overflow");
  }
  const el = document.createElement("div");
  el.className = spec.name;
  el.textContent = "print layout self-check";
  el.style.setProperty("margin", "0", "important");
  el.style.setProperty("max-width", "none", "important");
  page.appendChild(el);
  /* Measured after insertion rather than assumed: the width that overhangs the page by
     `over` is the one that reaches `over` past it from wherever the column starts. */
  const start = el.getBoundingClientRect().left;
  el.style.setProperty("width", `${root.clientWidth + spec.over - start}px`, "important");
  const bullet = page.querySelector("ul > li");
  if (!bullet) {
    throw new Error("no unordered-list bullet to stretch");
  }
  bullet.classList.add(spec.bullet);
  const style = document.createElement("style");
  style.textContent = `.${spec.bullet}::before {
    content: "" !important; background: currentColor !important;
    width: 3px !important; height: 1lh !important; top: 0 !important;
  }`;
  document.head.appendChild(style);
};
