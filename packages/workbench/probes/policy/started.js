// Whether the page initialised under its policy: the Pack and Search APIs exist, the Pack
// stage drew its squares, and the page's fonts, which are `data:` URIs, have loaded.
() =>
  document.fonts.ready.then(() => ({
    pack: typeof Reflect.get(window, "packWorkbench")?.state === "function",
    search: typeof Reflect.get(window, "searchWorkbench")?.state === "function",
    squares: document.querySelectorAll("#pack-squares > g").length,
    fonts: document.fonts.status,
  }));
