// How each of the mask's two classes is drawn, which is what makes the difference readable.
() => {
  const one = (k) => {
    const l = document.querySelector(`#mask-links line.${k}`);
    if (l === null) {
      return null;
    }
    const s = getComputedStyle(l);
    return [s.stroke, s.strokeWidth, s.strokeDasharray];
  };
  return { met: one("met"), unmet: one("unmet") };
};
