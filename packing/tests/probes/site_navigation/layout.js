() => {
  const nav = document.querySelector(".site-nav");
  const header = nav?.closest(".site-headroom") ?? nav;
  const panels = Array.from(document.querySelectorAll(".site-popover")).map((panel) => {
    const rect = panel.getBoundingClientRect();
    const style = getComputedStyle(panel);
    return {
      width: rect.width,
      left: rect.left,
      right: rect.right,
      measure: style.getPropertyValue("--kpress-measure"),
      overflow: panel.scrollWidth > panel.clientWidth,
    };
  });
  return {
    overflow: document.documentElement.scrollWidth > window.innerWidth,
    headerTop: header?.getBoundingClientRect().top ?? 0,
    headerBottom: header?.getBoundingClientRect().bottom ?? 0,
    panels,
  };
};
