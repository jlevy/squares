// What the started workbench reports: how many pairs its API serves, and where the site
// note's home link resolves. `href` is read from the element, so it is already absolute.
() => {
  const home = document.querySelector("#site-note a");
  return {
    pairs: window.atlasTransitions.pairs().length,
    home: home instanceof HTMLAnchorElement ? home.href : null,
  };
};
