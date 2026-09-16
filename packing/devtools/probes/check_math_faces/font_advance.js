// A reference probe: returns the measurement of one run's advance, in em, from the face its
// computed style resolves to. The same measurement strategy as pinned KPress's
// tests/math_font_probe.py. Linux Chromium can snap a normal-size glyph's advance to a whole
// pixel, which erased the difference between the 400 and 650 D. Copy the resolved face into
// a large hidden sample and measure in em; the actual formula keeps its original layout and
// size.
() =>
  /** @param {Element} element */
  (element) => {
    const size = 4096;
    const style = getComputedStyle(element);
    const probe = document.createElement("span");
    probe.textContent = element.textContent;
    Object.assign(probe.style, {
      position: "fixed",
      visibility: "hidden",
      display: "inline-block",
      whiteSpace: "pre",
      width: "max-content",
      maxWidth: "none",
      fontFamily: style.fontFamily,
      fontStyle: style.fontStyle,
      fontWeight: style.fontWeight,
      fontStretch: style.fontStretch,
      fontKerning: style.fontKerning,
      fontFeatureSettings: style.fontFeatureSettings,
      fontVariationSettings: style.fontVariationSettings,
      fontSize: `${size}px`,
    });
    document.body.append(probe);
    try {
      return probe.getBoundingClientRect().width / size;
    } finally {
      probe.remove();
    }
  };
