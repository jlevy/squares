// Where the plot draws the law: the knee and pull handles, whether the pull is drawn at
// all, the touching mark, and the number the push axis tops out at.
() => {
  /** @param {string} id */
  const element = (id) => {
    const found = document.getElementById(id);
    if (found == null) {
      throw new Error(`probe requires #${id}`);
    }
    return found;
  };
  const knee = element("lp-knee");
  const pull = element("lp-pull");
  return {
    knee: [Number(knee.getAttribute("cx")), Number(knee.getAttribute("cy"))],
    pull: [Number(pull.getAttribute("cx")), Number(pull.getAttribute("cy"))],
    shown: pull.style.display !== "none",
    cross: Number(element("lp-cross").getAttribute("cx")),
    top: Number(element("lp-top").textContent),
  };
};
