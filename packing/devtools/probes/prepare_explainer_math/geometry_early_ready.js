// The font evidence for every reserved box visible while the math-font transfers are held.
// For each distinct glyph request in a box: `document.fonts.check`, the declared faces of its
// families, and, where the check says ready, the faces a bounded `document.fonts.load`
// resolves to.
async () => {
  const result = [];
  /** @param {string} name */
  const familyName = (name) => name.trim().replace(/^["']|["']$/g, "");
  for (const box of /** @type {HTMLElement[]} */ (globalThis.__squaresGeometryBoxes)) {
    if (getComputedStyle(box).visibility === "hidden") {
      continue;
    }
    /** @type {Map<string, { text: string, families: string[] }>} */
    const requests = new Map();
    const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
    for (let text = walker.nextNode(); text; text = walker.nextNode()) {
      if (!text.textContent || !text.parentElement) {
        continue;
      }
      const style = getComputedStyle(text.parentElement);
      const spec =
        `${style.fontStyle} ${style.fontWeight} ` + `${style.fontSize} ${style.fontFamily}`;
      const request = requests.get(spec) || {
        text: "",
        families: style.fontFamily.split(",").map(familyName),
      };
      request.text += text.textContent;
      requests.set(spec, request);
    }
    const evidence = [];
    for (const [spec, request] of requests) {
      const { text, families } = request;
      const check = document.fonts.check(spec, text);
      const declared = [...document.fonts]
        .filter((face) => families.includes(familyName(face.family)))
        .map((face) => ({
          family: face.family,
          status: face.status,
          style: face.style,
          weight: face.weight,
          unicode_range: face.unicodeRange,
        }));
      /** @type {FontFace[]} */
      let faces = [];
      /** @type {ReturnType<typeof setTimeout> | undefined} */
      let timer;
      if (check) {
        // A reported-ready glyph must resolve to an actually loaded declared
        // face, without releasing any transfer held by the geometry probe.
        try {
          faces = await Promise.race([
            document.fonts.load(spec, text),
            /** @type {Promise<FontFace[]>} */ (
              new Promise((resolve) => {
                timer = setTimeout(() => resolve([]), 500);
              })
            ),
          ]);
        } finally {
          clearTimeout(timer);
        }
      }
      evidence.push({
        spec,
        text,
        check,
        declared_faces: declared,
        faces: faces.map((face) => ({ family: face.family, status: face.status })),
      });
    }
    result.push({
      key: Number(box.dataset.squaresGeometryKey),
      source:
        /** @type {HTMLElement | null} */ (box.closest("[data-kpress-math-source]"))?.dataset
          .kpressMathSource || "",
      requests: evidence,
    });
  }
  return result;
};
