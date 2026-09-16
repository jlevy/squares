// Which of these elements are drawn rather than merely present: laid out with an area, and not
// taken out by `display`, `visibility` or a zero opacity on themselves or anything above them.
// Each entry is [id, whether it is drawn, whether it carries the `hidden` attribute], so a caller
// can hold the picture against what the page's own markup says. o.ids is the list to ask about.
/** @param {{ids: string[]}} o */
(o) =>
  o.ids.map((id) => {
    const element = document.getElementById(id);
    if (element == null) {
      throw new Error(`probe requires #${id}`);
    }
    const box = element.getBoundingClientRect();
    const drawn =
      box.width > 0 &&
      box.height > 0 &&
      element.checkVisibility({ opacityProperty: true, visibilityProperty: true });
    return [id, drawn, element.hasAttribute("hidden")];
  });
