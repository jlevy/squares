// The arriving square and the container, as [its opacity, the mark's opacity, the mark's
// stroke width, the container's side]. Takes {identity}.
(o) => [
  Number(document.querySelector('#squares g[data-identity="' + o.identity + '"]').getAttribute('opacity')),
  document.getElementById('mark').getAttribute('opacity'),
  document.getElementById('mark').firstElementChild.getAttribute('stroke-width'),
  parseFloat(document.getElementById('container').getAttribute('width')),
]
