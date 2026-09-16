// Negative control for `--self-test`, injected into the page's head: drops every input event
// until fonts are released, so early slider input is lost.
() => {
  document.addEventListener(
    "input",
    (event) => {
      if (!(/** @type {SquaresMathLoadControl} */ (globalThis.__mathLoadControl).released)) {
        event.stopImmediatePropagation();
      }
    },
    true,
  );
};
