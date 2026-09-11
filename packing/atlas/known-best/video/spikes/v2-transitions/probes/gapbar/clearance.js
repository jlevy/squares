// The room the gap bar and the headline have on the stage, in the stage's own units.
// The headline sits centred under the packing it names, so its clearance is measured from
// the picture rather than from the bar.
() => {
  const s = document.getElementById('stage').getBoundingClientRect();
  const k = s.width / 1920;
  const b = document.getElementById('gapbar').getBoundingClientRect();
  const e = document.getElementById('headline').getBoundingClientRect();
  // The DRAWN container, not the svg element: the element's box carries the view's own
  // padding, so the picture ends well above it and a clearance measured to the element
  // would refuse a headline that is nowhere near the packing.
  const pk = document.getElementById('container').getBoundingClientRect();
  const f = document.getElementById('facts').getBoundingClientRect();
  return {
    bottom: (b.bottom - s.top) / k, top: (b.top - s.top) / k,
    headTop: (e.top - s.top) / k, headBottom: (e.bottom - s.top) / k,
    packBottom: (pk.bottom - s.top) / k, stageBottom: s.height / k,
    right: (b.right - s.left) / k, panelRight: (f.right - s.left) / k,
    shown: getComputedStyle(document.getElementById('gapbar')).display !== 'none',
  };
}
