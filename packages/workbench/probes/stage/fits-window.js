// Where the stage sits against the window it has to fit inside.
() => {
  const stage = document.getElementById("stage");
  if (stage == null) {
    throw new Error("probe requires #stage");
  }
  const s = stage.getBoundingClientRect();
  return { top: s.top, bottom: s.bottom, h: window.innerHeight };
};
