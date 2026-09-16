// A head script: records in `__squaresHeatDraws` the id of every `prove-` heat-map canvas an
// image is drawn into, so the print check can compare the canvases drawn with those CSS shows.
() => {
  const draw = CanvasRenderingContext2D.prototype.drawImage;
  globalThis.__squaresHeatDraws = [];
  CanvasRenderingContext2D.prototype.drawImage = /** @type {typeof draw} */ (
    /**
     * @this {CanvasRenderingContext2D}
     * @param {Parameters<typeof draw>} args
     */
    function (...args) {
      if (this.canvas.id.startsWith("prove-")) {
        /** @type {string[]} */ (__squaresHeatDraws).push(this.canvas.id);
      }
      return draw.apply(this, args);
    }
  );
};
