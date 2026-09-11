// Where the plot draws the law: the knee and pull handles, whether the pull is drawn at
// all, the touching mark, and the number the push axis tops out at.
() => ({
  knee: [
    Number(document.getElementById("lp-knee").getAttribute("cx")),
    Number(document.getElementById("lp-knee").getAttribute("cy")),
  ],
  pull: [
    Number(document.getElementById("lp-pull").getAttribute("cx")),
    Number(document.getElementById("lp-pull").getAttribute("cy")),
  ],
  shown: document.getElementById("lp-pull").style.display !== "none",
  cross: Number(document.getElementById("lp-cross").getAttribute("cx")),
  top: Number(document.getElementById("lp-top").textContent),
});
