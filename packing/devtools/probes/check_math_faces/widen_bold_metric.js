// Self-test: KPress's 650 advance for `D` is now a quarter em wider than the drawn glyph.
() => {
  const metrics =
    /** @type {{ sans: { "Main-Bold": Record<number, [number, number, number, number, number]> } }} */ (
      globalThis.kpressKatexTextMetrics
    );
  /** @type {[number, number, number, number, number]} */ (metrics.sans["Main-Bold"][68])[4] +=
    0.25;
};
