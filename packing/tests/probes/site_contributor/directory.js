// Profile narrative font, account identifiers, and responsive table containment.
() => {
  const article = document.querySelector("article.site-contributor-directory");
  const intro = article?.querySelector(":scope > p");
  const table = article?.querySelector("table");
  const wrap = table?.closest(".site-table-wrap");
  const accounts = [...(table?.querySelectorAll("td.site-profile-links") ?? [])].map((cell) => {
    const rect = cell.getBoundingClientRect();
    return {
      width: rect.width,
      links: [...cell.querySelectorAll("a span")].map((label) => {
        const style = getComputedStyle(label);
        const edge = label.getBoundingClientRect();
        return {
          lines: label.getClientRects().length,
          nowrap: style.whiteSpace,
          inside: edge.left >= rect.left - 0.5 && edge.right <= rect.right + 0.5,
        };
      }),
    };
  });
  return {
    intro: intro?.textContent,
    introFont: intro ? getComputedStyle(intro).fontFamily : null,
    tableFont: table ? getComputedStyle(table).fontFamily : null,
    accounts,
    tableWidth: table?.getBoundingClientRect().width ?? 0,
    wrapperWidth: wrap?.getBoundingClientRect().width ?? 0,
    overflow: document.documentElement.scrollWidth - innerWidth,
  };
};
