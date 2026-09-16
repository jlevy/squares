// Self-test: declare the sans composite's 650 slot and make both paragraphs sans, the
// supported sans reading face.
() => {
  document.fonts.add(new FontFace("KPress Math Text Sans", "local(Arial)", { weight: "650" }));
  document.body.style.setProperty("--kpress-font-prose", '"Source Sans 3 Variable", sans-serif');
  /** @type {Element} */ (document.querySelector("#a")).className = "sans";
};
