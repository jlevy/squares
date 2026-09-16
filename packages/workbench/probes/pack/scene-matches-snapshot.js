// Whether the Pack API's snapshot is the scene the stage draws: one `#pack-squares > g` per pose,
// each translated to its pose's centre relative to the container's origin and rotated by its
// angle in degrees, all to within 1e-9.
() => {
  /** @typedef {import("../../src/api/pack-api.js").PackWorkbenchApi} PackWorkbenchApi */
  const api = /** @type {Window & {packWorkbench?: PackWorkbenchApi}} */ (window).packWorkbench;
  if (api === undefined) {
    throw new Error("probe requires window.packWorkbench");
  }
  const snapshot = api.state().snapshot;
  const nodes = [...document.querySelectorAll("#pack-squares > g")];
  if (nodes.length !== snapshot.poses.length) {
    return false;
  }
  return snapshot.poses.every((pose, index) => {
    const match = nodes[index]
      .getAttribute("transform")
      ?.match(/^translate\(([^ ]+) ([^)]+)\) rotate\(([^)]+)\)/);
    if (!match) {
      return false;
    }
    return (
      Math.abs(Number(match[1]) - (pose.x - snapshot.container.originX)) < 1e-9 &&
      Math.abs(Number(match[2]) - (pose.y - snapshot.container.originY)) < 1e-9 &&
      Math.abs(Number(match[3]) - (pose.angle * 180) / Math.PI) < 1e-9
    );
  });
};
