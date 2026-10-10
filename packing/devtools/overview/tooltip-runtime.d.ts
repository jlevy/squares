/** The checked KPress frame exposes its existing placement function for badge overlays. */
declare var siteKpressTooltipPosition:
  | ((anchor: HTMLAnchorElement, tooltip: HTMLElement) => void)
  | undefined;
declare function positionTooltip(anchor: HTMLAnchorElement, tooltip: HTMLElement): void;
declare const behaviors: { override(name: string, bind: () => undefined): void };
