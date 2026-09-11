// How many of the identity pool's elements are drawn rather than hidden.
() => Array.from(document.querySelectorAll('#squares g[data-identity]'))
  .filter(g => g.style.display !== 'none').length
