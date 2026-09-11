// The scarlet mark, as [opacity, stroke width, the stroke colour as computed].
() => [
  document.getElementById('mark').getAttribute('opacity'),
  document.getElementById('mark').firstElementChild.getAttribute('stroke-width'),
  getComputedStyle(document.getElementById('mark').firstElementChild).stroke,
]
