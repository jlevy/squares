// How far a style's cached trajectory ends from the n + 1 poses, and how many bodies it
// simulated. Takes {index, style}.
(o) => {
  const data = JSON.parse(document.getElementById('atlas-data').textContent);
  const info = window.atlasTransitions.physics(o.index, o.style);
  const pair = data.pairs[o.index];
  const target = data.frames[String(pair.n + 1)].squares;
  let maxPos = 0, maxAng = 0;
  info.final.forEach((f, i) => {
    const t = i < pair.n ? target[pair.map[i]] : target[pair.new];
    maxPos = Math.max(maxPos, Math.hypot(f[0] - t[0], f[1] - t[1]));
    const d = ((f[2] - t[2]) % 90 + 90) % 90;
    maxAng = Math.max(maxAng, Math.min(d, 90 - d));
  });
  return { maxPos, maxAng, bodies: info.bodies, squares: pair.n + 1 };
}
