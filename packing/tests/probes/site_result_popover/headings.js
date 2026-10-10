() => {
  const page = document.querySelector(".site-page");
  if (!page) {
    throw new Error("The reader document is missing its page hierarchy");
  }
  const sample = document.createElement("span");
  sample.style.fontFamily = "var(--kpress-font-sans)";
  page.append(sample);
  const sansFamily = getComputedStyle(sample).fontFamily;
  sample.remove();
  const headings = ["h1", "h2", "h3"].map((tag) => {
    const heading = page.querySelector(tag);
    if (!heading?.parentElement) {
      throw new Error(`The document has no ${tag} heading`);
    }
    const style = getComputedStyle(heading);
    return {
      tag,
      text: heading.textContent,
      fontSize: Number.parseFloat(style.fontSize),
      parentFontSize: Number.parseFloat(getComputedStyle(heading.parentElement).fontSize),
      fontFamily: style.fontFamily,
      fontWeight: style.fontWeight,
      fontStyle: style.fontStyle,
      textTransform: style.textTransform,
      letterSpacing: style.letterSpacing,
      lineHeight: Number.parseFloat(style.lineHeight),
    };
  });
  const navigation = document.querySelector(".site-nav");
  return {
    view: document.documentElement.getAttribute("data-site-view"),
    navigationVisible: (navigation?.getClientRects().length ?? 0) > 0,
    sansFamily,
    headings,
  };
};
