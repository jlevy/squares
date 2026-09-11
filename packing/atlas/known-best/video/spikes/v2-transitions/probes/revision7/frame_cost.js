// What a whole frame costs while the bar is live, over 200 seeks. Takes {index}.
(o) => {
  const A = window.atlasTransitions;
  A.select(o.index);
  A.setStyle("bodies");
  A.setSnap(true);
  A.seek(1.7);
  const t0 = performance.now();
  for (let k = 0; k < 200; k++) {
    A.seek(1.2 + (k % 100) * 0.01);
  }
  const per = (performance.now() - t0) / 200;
  return { per, spark: document.getElementById("gap-spark") !== null, side: A.gapBar().side };
};
