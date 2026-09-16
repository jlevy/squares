// Installed before parsing: holds successful font loads until `__mathLoadControl.release()`.
// Gate successful loads only when CSS actually matches a declared face. Empty
// unicode-range/system-family results remain immediate. CSS and the independent
// oracle can decode fonts normally; this tests the explicit readiness contract.
// `prepare_explainer_math.check_geometry` separately holds real font requests.
() => {
  /** @type {(value?: unknown) => void} */
  let release = () => undefined;
  const gate = new Promise((resolve) => {
    release = resolve;
  });
  // `nativeLoad` is added below, once the prototype's own `load` is in hand.
  const control = /** @type {SquaresMathLoadControl} */ ({
    heldLoads: 0,
    released: false,
    release() {
      this.released = true;
      release();
    },
  });
  globalThis.__mathLoadControl = control;
  const fontSet = Object.getPrototypeOf(document.fonts),
    loadSet = fontSet.load;
  control.nativeLoad = loadSet.bind(document.fonts);
  // Some pinned Chromium versions have no global FontFaceSet constructor.
  /** @param {Parameters<FontFaceSet["load"]>} args */
  fontSet.load = function (...args) {
    const promise = loadSet.apply(this, args);
    if (control.released) {
      return promise;
    }
    return promise.then((/** @type {FontFace[]} */ faces) => {
      if (!faces.length) {
        return faces;
      }
      control.heldLoads++;
      return gate.then(() => faces);
    });
  };
  const loadFace = FontFace.prototype.load;
  /** @this {FontFace} @param {unknown[]} args */
  FontFace.prototype.load = function (...args) {
    if (control.released) {
      return loadFace.apply(this, /** @type {[]} */ (args));
    }
    control.heldLoads++;
    return gate.then(() => loadFace.apply(this, /** @type {[]} */ (args)));
  };
};
