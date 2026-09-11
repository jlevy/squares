// Every button in the controls, as [its place, what names it, left, top, width, height]
// rounded to a hundredth of a pixel: the shape a control moving would change.
() => Array.from(document.querySelectorAll('#controls button')).map((b, i) => {
  const r = b.getBoundingClientRect();
  return [i, b.id || b.textContent.trim().slice(0, 18),
          Math.round(r.left * 100) / 100, Math.round(r.top * 100) / 100,
          Math.round(r.width * 100) / 100, Math.round(r.height * 100) / 100];
})
