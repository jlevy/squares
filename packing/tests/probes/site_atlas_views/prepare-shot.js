// Decode every shown atlas drawing before a tall screenshot. Loading hints do not
// change tile geometry; they prevent offscreen lazy images from becoming blank evidence.
async () => {
  const drawings = [...document.querySelectorAll(".site-atlas-cell img")].filter(
    (drawing) => drawing instanceof HTMLImageElement && drawing.getClientRects().length > 0,
  );
  const failed = await Promise.all(
    drawings.map(async (drawing) => {
      if (!(drawing instanceof HTMLImageElement)) {
        return null;
      }
      drawing.loading = "eager";
      try {
        await drawing.decode();
        return null;
      } catch {
        return drawing.closest("[data-atlas-n]")?.getAttribute("data-atlas-n");
      }
    }),
  );
  return failed.filter((n) => n !== null);
};
