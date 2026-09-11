// The whole drawn frame: every square's transform, and the container it sits in.
() => ({
  squares: Array.from(document.querySelectorAll('#squares g[data-identity]'))
    .filter((e) => e.style.display !== 'none')
    .map((e) => e.dataset.identity + '@' + e.getAttribute('transform')),
  box: document.getElementById('container').getAttribute('width'),
})
