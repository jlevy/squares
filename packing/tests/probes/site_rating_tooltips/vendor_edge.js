() => {
  const badge = document.querySelector("#edge-table .site-significance");
  const id = badge?.getAttribute("aria-describedby");
  const tooltip = id ? document.getElementById(id) : null;
  const vendor = /** @type {typeof globalThis & {
    siteKpressTooltipPosition?: (anchor: HTMLAnchorElement, tooltip: HTMLElement) => void
  }} */ (globalThis);
  if (!(badge instanceof HTMLElement) || !tooltip || !vendor.siteKpressTooltipPosition) {
    throw new Error("Missing KPress tooltip placement fixture");
  }
  vendor.siteKpressTooltipPosition(/** @type {HTMLAnchorElement} */ (badge), tooltip);
  return tooltip.getBoundingClientRect().bottom;
};
