// Paint the generated case summary under the real page stylesheet, then remove it.
// This exercises independent proof/construction accents without navigating a user tab.
/** @param {{html: string}} input */
(input) => {
  const page = document.querySelector(".site-page");
  if (!(page instanceof HTMLElement)) {
    return null;
  }
  const summary = document.createElement("section");
  summary.className = "site-case-summary site-atlas-pop";
  summary.innerHTML = input.html;
  page.append(summary);
  /** @param {string} selector */
  const color = (selector) => {
    const element = summary.querySelector(selector);
    return element ? getComputedStyle(element).color : null;
  };
  /** @param {string} token */
  const tokenColor = (token) => {
    const sample = document.createElement("span");
    sample.style.color = `var(${token})`;
    summary.append(sample);
    const value = getComputedStyle(sample).color;
    sample.remove();
    return value;
  };
  const reading = {
    colors: {
      recent: tokenColor("--site-new-result"),
      upper: tokenColor("--site-bound-upper"),
      dark: tokenColor("--kpress-doc-muted"),
      neutral: tokenColor("--kpress-doc-text"),
    },
    upper: color(".site-atlas-gap-values .is-upper"),
    lower_gap_label: summary.querySelector(".site-atlas-gap-values .is-lower")?.textContent,
    lower_bound_label: summary.querySelector(".site-atlas-pop-bound .is-lower mn")?.textContent,
    lower_citation: color(".site-atlas-pop-which.is-lower"),
    equality_upper: color(".site-atlas-pop-bound .is-exact-value"),
    badges: [...summary.querySelectorAll(".site-atlas-badge")].map((badge) => ({
      glyph: badge.textContent?.trim(),
      style: badge.getAttribute("data-style"),
      background: getComputedStyle(badge).backgroundColor,
    })),
  };
  summary.remove();
  return reading;
};
