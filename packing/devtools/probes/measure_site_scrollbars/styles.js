/** @param {string[]} selectors */
(selectors) =>
  selectors.map((selector) => {
    const element = document.querySelector(selector);
    if (!(element instanceof HTMLElement)) {
      return { selector, missing: true };
    }
    const style = getComputedStyle(element);
    const track = getComputedStyle(element, "::-webkit-scrollbar-track");
    return {
      selector,
      width: style.scrollbarWidth,
      colors: style.scrollbarColor,
      track: track.backgroundColor,
      overflowingX: element.scrollWidth > element.clientWidth,
      overflowingY: element.scrollHeight > element.clientHeight,
    };
  });
