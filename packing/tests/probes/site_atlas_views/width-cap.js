// Negative control: reinstate the former Atlas width cap on the measured element.
() => {
  const atlas = document.querySelector(".site-page .site-atlas-grid");
  if (!(atlas instanceof HTMLElement)) {
    throw new Error("the measured Atlas is missing");
  }
  // This synthetic control must take effect synchronously, even under reduced motion.
  atlas.style.transition = "none";
  atlas.style.setProperty("--site-wide", "140rem");
  // Other wide-track rules can grow past that token; enforce the restored cap itself.
  atlas.style.maxWidth = "140rem";
  const style = getComputedStyle(atlas);
  return {
    measured: atlas === document.querySelector("[data-atlas-grid]"),
    root_font: getComputedStyle(document.documentElement).fontSize,
    max_width: style.maxWidth,
    min_width: style.minWidth,
    width: style.width,
    box_width: atlas.getBoundingClientRect().width,
  };
};
