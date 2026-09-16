// The stage's whole markup, which is what a seek has to reproduce exactly.
() => {
  const stage = document.getElementById("stage");
  if (stage == null) {
    throw new Error("probe requires #stage");
  }
  return stage.innerHTML;
};
