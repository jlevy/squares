// The boxes of the bar's own pieces, in the stage's own units: the track, the shaded open
// span, the two bound arrows and the two numerals.
() => {
  const s = document.getElementById('stage').getBoundingClientRect();
  const k = s.width / 1920;
  const box = (sel) => {
    const b = document.querySelector(sel).getBoundingClientRect();
    return {l: (b.left - s.left) / k, r: (b.right - s.left) / k,
            t: (b.top - s.top) / k, b: (b.bottom - s.top) / k};
  };
  return {track: box('.gapbar-plot .track'), open: box('#gapbar-open'),
          rec: box('#gapbar-record'), low: box('#gapbar-lower'),
          lowLabel: box('#gapbar-lower-label'), recLabel: box('#gapbar-record-label')};
}
