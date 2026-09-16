// How far a style's cached trajectory ends from the n + 1 poses, and how many bodies it
// simulated. Takes {index, style}.
/** @param {{index: number, style: import("../../src/api/workbench-api.js").AtlasStyle}} o */
(o) => {
  const source = document.getElementById("atlas-data")?.textContent;
  if (source == null) {
    throw new Error("probe requires #atlas-data text");
  }
  const data = JSON.parse(source);
  const info = window.atlasTransitions.physics(o.index, o.style);
  const pair = data.pairs[o.index];
  const target = data.frames[String(pair.n + 1)].squares;
  let maxPos = 0,
    maxAng = 0;
  info.final.forEach((f, i) => {
    const t = i < pair.n ? target[pair.map[i]] : target[pair.new];
    maxPos = Math.max(maxPos, Math.hypot(f[0] - t[0], f[1] - t[1]));
    const d = (((f[2] - t[2]) % 90) + 90) % 90;
    maxAng = Math.max(maxAng, Math.min(d, 90 - d));
  });
  return { maxPos, maxAng, bodies: info.bodies, squares: pair.n + 1 };
};
