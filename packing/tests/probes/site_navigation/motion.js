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
      keyframes: element
        .getAnimations()
        .flatMap((animation) =>
          animation.effect instanceof KeyframeEffect
            ? animation.effect.getKeyframes().map((frame) => frame.transform)
            : [],
        ),
    };
  };
  return {
    chevron: motion(document.querySelector('.site-nav-disclosure[aria-expanded="true"] svg')),
    panel: motion(document.querySelector('.site-nav-disclosure[aria-expanded="true"] + ul')),
    mobile: motion(document.querySelector(".site-nav-links")),
    labels: [
      ...document.querySelectorAll(
        "button:not(.site-card), a.site-action, a.site-popover-action, .site-tabs a",
      ),
    ]
      .filter((control) => control.textContent?.trim() && control.getClientRects().length > 0)
      .map((control) => {
        const style = getComputedStyle(control);
        return {
          label: control.textContent?.trim(),
          tracking: Number.parseFloat(style.letterSpacing) / Number.parseFloat(style.fontSize),
        };
      }),
    chevrons: Object.fromEntries(
      [...document.querySelectorAll(".site-nav-disclosure")].map((button) => [
        button.getAttribute("data-page"),
        motion(button.querySelector("svg")),
      ]),
    ),
  };
};
