// The box of the first element a selector matches, as [left, top, width, height].
// Takes {selector}.
(o) => {
  const b = document.querySelector(o.selector).getBoundingClientRect();
  return [b.left, b.top, b.width, b.height];
}
