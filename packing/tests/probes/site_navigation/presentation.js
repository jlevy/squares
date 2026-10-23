// Shared heading roles, profile tally flow, and case-property tag geometry.
() => {
  /** @param {Element} element */
  const style = (element) => {
    const computed = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return {
      family: computed.fontFamily,
      style: computed.fontStyle,
      weight: computed.fontWeight,
      size: computed.fontSize,
      top: rect.top,
      bottom: rect.bottom,
      width: rect.width,
      height: rect.height,
      label: element.getAttribute("aria-label"),
    };
  };
  const exposition = document.querySelector("#exposition");
  const resources = document.querySelector("#resources");
  const tag = document.querySelector(".site-chip");
  return {
    profileHeadings: [...document.querySelectorAll(".site-contributor h2")].map(style),
    exposition: exposition ? style(exposition) : null,
    tallies: [...document.querySelectorAll(".site-profile-tally > span")].map(style),
    resourcesTop: resources?.getBoundingClientRect().top,
    badges: [...document.querySelectorAll(".site-case-badges .site-atlas-badge")].map(style),
    tag: tag ? style(tag) : null,
    overflow: document.documentElement.scrollWidth > innerWidth,
  };
};
