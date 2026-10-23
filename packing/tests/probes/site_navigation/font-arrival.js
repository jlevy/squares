// Breadcrumb line boxes before and after the shared sans face arrives.
() =>
  [...document.querySelectorAll(".site-breadcrumbs li")].map((element) => {
    const range = document.createRange();
    range.selectNodeContents(element);
    const rect = element.getBoundingClientRect();
    return {
      text: element.textContent,
      family: getComputedStyle(element).fontFamily,
      size: getComputedStyle(element).fontSize,
      width: rect.width,
      height: rect.height,
      lines: [...range.getClientRects()].map((line) => ({
        width: line.width,
        y: line.y,
      })),
    };
  });
