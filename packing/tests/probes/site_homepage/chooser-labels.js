// Where each compact chooser's words sit in their control: the middle of their capitals
// against the middle of the control's border box. The labels are set in capitals, so
// the cap height is what reads as the text. Each word's baseline and `1cap` are read
// from two empty markers set on its own line and removed at once.
() => {
  const controls = [
    ...document.querySelectorAll(
      '.site-tabs.site-chooser-small :is([role="tab"], button), .site-filter-trigger, .site-news-reset',
    ),
  ].filter((control) => control.getClientRects().length > 0);
  /** @param {Text} text @param {string} height */
  const marker = (text, height) => {
    const mark = document.createElement("span");
    mark.style.cssText = `display: inline-block; inline-size: 0; block-size: ${height}; vertical-align: baseline;`;
    text.after(mark);
    const rect = mark.getBoundingClientRect();
    mark.remove();
    return rect;
  };
  return controls.map((control) => {
    const box = control.getBoundingClientRect();
    const middle = box.top + box.height / 2;
    const walker = document.createTreeWalker(control, NodeFilter.SHOW_TEXT, {
      acceptNode: (node) =>
        node.textContent?.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP,
    });
    const words = [];
    for (let text = walker.nextNode(); text; text = walker.nextNode()) {
      if (!(text instanceof Text) || !text.parentElement) {
        continue;
      }
      const style = getComputedStyle(text.parentElement);
      // A marker beside a flex or grid container's own text would be an item of its own,
      // not a box on the text's line, and would read nothing.
      if (/flex|grid/.test(style.display)) {
        throw new Error(`"${text.textContent}" is not on a line a marker can share`);
      }
      const baseline = marker(text, "0px").bottom;
      const cap = marker(text, "1cap").height;
      words.push({
        text: (text.textContent ?? "").trim(),
        offset: baseline - cap / 2 - middle,
        transform: style.textTransform,
      });
    }
    return {
      label: (control.textContent ?? "").trim().replace(/\s+/g, " "),
      kind: control.matches(".site-filter-trigger")
        ? "trigger"
        : control.matches(".site-news-reset")
          ? "reset"
          : "tab",
      height: box.height,
      width: box.width,
      fontSize: Number.parseFloat(getComputedStyle(control).fontSize),
      words,
    };
  });
};
