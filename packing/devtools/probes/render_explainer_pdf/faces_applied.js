// The added print faces, settled: both the ones the document tree asks for and the ones only
// an `@page` margin box does. Layout is forced and two frames let through before the first
// wait, so the faces the new rules bring into use are loading; the margin-box families, which
// never enter `document.fonts.ready`, are then asked for by name and waited on again.
// `render_explainer_pdf._FACES_APPLIED`'s comment has the whole argument.
/** @param {[ReadonlyArray<readonly [string, string]>, string]} argument */
async ([tokens, sample]) => {
  void document.documentElement.offsetHeight;
  await new Promise((frame) => requestAnimationFrame(() => requestAnimationFrame(frame)));
  await document.fonts.ready;
  const root = getComputedStyle(document.documentElement);
  const stacks = tokens
    .map(([familyToken, weightToken]) => ({
      family: root.getPropertyValue(familyToken).trim(),
      weight: root.getPropertyValue(weightToken).trim() || root.fontWeight || "400",
    }))
    .filter((stack) => stack.family.length > 0);
  await Promise.all(
    stacks.map((stack) =>
      document.fonts.load(`${stack.weight} 1rem ${stack.family}`, sample).catch(() => undefined),
    ),
  );
  await document.fonts.ready;
  void document.documentElement.offsetHeight;
  return document.fonts.status;
};
