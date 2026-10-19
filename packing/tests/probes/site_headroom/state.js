() => {
  const header = document.querySelector(".site-headroom") ?? document.querySelector(".site-nav");
  const target = document.getElementById("header-target");
  if (!(header instanceof HTMLElement) || !target) {
    throw new Error("The header fixture is incomplete");
  }
  const box = header.getBoundingClientRect();
  return {
    enhanced: header.classList.contains("site-headroom"),
    hidden: header.classList.contains("site-headroom-hidden"),
    top: box.top,
    bottom: box.bottom,
    height: box.height,
    offset: Number.parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop),
    targetTop: target.getBoundingClientRect().top,
    targetPosition: target.getBoundingClientRect().top + window.scrollY,
    scroll: window.scrollY,
    maxScroll: document.documentElement.scrollHeight - window.innerHeight,
    transition: getComputedStyle(header).transitionDuration,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    tabsInside: !!header.querySelector("nav.site-tabs"),
  };
};
