() => {
  /** @param {Element | null} element */
  const motion = (element) => {
    if (!element) {
      return null;
    }
    const style = getComputedStyle(element);
    return {
      duration: style.transitionDuration.split(", ").map((value) => Number.parseFloat(value)),
      properties: style.transitionProperty.split(", "),
      opacity: Number.parseFloat(style.opacity),
      transform: style.transform,
      animations: element.getAnimations().length,
    };
  };
  return {
    chevron: motion(document.querySelector('.site-nav-disclosure[aria-expanded="true"] svg')),
    panel: motion(document.querySelector('.site-nav-disclosure[aria-expanded="true"] + ul')),
    mobile: motion(document.querySelector(".site-nav-links")),
  };
};
