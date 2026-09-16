// The ids of the `prove-` heat-map canvases CSS lays out.
() =>
  [...document.querySelectorAll("canvas[id^=prove-]")]
    .filter((node) => node.getClientRects().length)
    .map((node) => node.id);
