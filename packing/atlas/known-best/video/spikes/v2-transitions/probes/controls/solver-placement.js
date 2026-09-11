// Where the solver select sits: which box holds it, whether that is the step-animation
// group, what the box's neighbours are called, and whether the select has a width of its own.
() => {
  const sel = document.getElementById('style-select');
  const box = sel.closest('.subpanel');
  const row = box.parentElement;
  const title = (e) => { const t = e.querySelector('.box-title'); return t ? t.textContent.trim() : null; };
  return {title: title(box), inStepGroup: box.id === 'step-anim-box',
          siblings: Array.from(row.children).filter((e) => e.classList.contains('subpanel')).map(title),
          width: getComputedStyle(sel).width};
}
