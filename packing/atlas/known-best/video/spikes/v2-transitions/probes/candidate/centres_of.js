// The centre each of these identities is drawn at, in the order asked. Takes {identities}.
(o) => o.identities.map((id) => {
  const g = document.querySelector('#squares g[data-identity="' + id + '"]');
  const m = /translate\(([-\d.e]+) ([-\d.e]+)\)/.exec(g.getAttribute('transform'));
  return [parseFloat(m[1]), parseFloat(m[2])];
})
