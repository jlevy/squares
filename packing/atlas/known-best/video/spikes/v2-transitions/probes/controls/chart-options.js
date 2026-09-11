// The two chart options, or null if either is missing from the page.
() => {
  const snap = document.getElementById("snap-toggle");
  const bias = document.getElementById("bias-toggle");
  return snap === null || bias === null ? null : { snap: snap.checked, bias: bias.checked };
};
