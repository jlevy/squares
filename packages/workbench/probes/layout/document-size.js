// The full document must fit the viewport; clipped overflow can hide a control or the live status.
() =>
  new Promise((resolve) => {
    requestAnimationFrame(() =>
      requestAnimationFrame(() =>
        resolve({
          viewport: window.innerWidth,
          width: document.documentElement.scrollWidth,
          controlsWidth: document.getElementById("controls")?.scrollWidth ?? null,
        }),
      ),
    );
  });
