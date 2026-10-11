async () => {
  await document.fonts.ready;
  const row = document.querySelector(".site-homepage-atlas-actions");
  const action = row?.querySelector("a[download]");
  const icon = action?.querySelector('.site-icon-arrow[data-arrow="download"]');
  const style = action ? getComputedStyle(action) : null;
  const rect = action?.getBoundingClientRect();
  return {
    order: Array.from(row?.children ?? []).map((node) => node.textContent?.trim()),
    href: action?.getAttribute("href"),
    download: action?.hasAttribute("download"),
    uppercase: style?.textTransform,
    icon: icon ? getComputedStyle(icon).maskImage : null,
    icon_hidden: icon?.getAttribute("aria-hidden"),
    left: rect?.left,
    right: rect?.right,
    width: document.documentElement.clientWidth,
  };
};
