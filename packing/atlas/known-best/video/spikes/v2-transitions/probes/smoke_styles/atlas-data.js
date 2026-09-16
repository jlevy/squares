// The data the page embeds, parsed: every pair's map and every frame's poses.
() =>
  JSON.parse(
    /** @type {string} */ (
      /** @type {Element} */ (document.getElementById("atlas-data")).textContent
    ),
  );
