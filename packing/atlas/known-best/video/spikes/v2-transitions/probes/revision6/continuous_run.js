// A run left to cross three pair boundaries, reporting where it got to and how it was set.
// Resolves once it has crossed them, or once it has stopped playing.
() =>
  new Promise((resolve) => {
    const A = window.atlasTransitions;
    A.goTo(A.pairs()[0].n);
    A.setStyle("bodies");
    A.setDesaturate(false);
    A.playAll();
    const start = A.state().pair;
    const step = () => {
      const s = A.state();
      if (s.pair >= start + 3 || !s.playing) {
        A.stopAll();
        resolve({ pair: s.pair, start, style: s.style, desaturate: s.desaturate });
      } else {
        requestAnimationFrame(step);
      }
    };
    requestAnimationFrame(step);
  });
