() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
