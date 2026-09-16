// Settlement, with a math snapshot taken at every phase it passes through. `settled` is
// `settled.js`'s function and `snapshot` is `math_snapshot.js`'s, both handed in as handles.
/**
 * @param {{ settled: (observe: (phase: string) => unknown) => Promise<void>, snapshot: SquaresMathSnapshotter }} o
 */
async ({ settled, snapshot }) => {
  /** @type {SquaresMathSnapshot[]} */
  const snapshots = [];
  const capture = snapshot;
  await settled((phase) => snapshots.push(capture(phase)));
  return snapshots;
};
