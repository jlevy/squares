// Scrolls an element to the middle of the viewport, so a touch lands on it and a swipe
// starting on it has page left to scroll in both directions.
/** @param {Element} el */
(el) => el.scrollIntoView({ block: "center" });
