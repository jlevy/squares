// Resolves once the page's fonts have loaded, so no fill is read while a face is swapping in.
() => document.fonts.ready;
