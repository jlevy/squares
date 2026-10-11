/** Globals shared by the explainer's classic scripts and render-time sentinels. */
declare function __SQUARES_KPRESS_CLIENT_JS__(): void;

declare const __SQUARES_ATOMS__: [number, number, number, number, number];
declare const __SQUARES_SCALE__: number;
declare const __SQUARES_L__: number;
declare const __SQUARES_B__: number;
declare const __SQUARES_LIMIT_NUM__: number;
declare const __SQUARES_LIMIT_DEN__: number;
declare const __SQUARES_STEPS__: number;
declare const __SQUARES_TIGHT__: number;
declare const __SQUARES_WITNESS_X__: number;
declare const __SQUARES_WITNESS_Y__: number;

interface Window {
  finishMathBootstrap: () => void;
  kpressInitTooltips?: (root: Document, options: { only: string }) => void;
  kpressInitCodeCopy?: (root: Document) => void;
}

declare const behaviors: { override(name: string, bind: () => undefined): void };
declare function initKpressTooltips(root: Document, options: { only: string }): void;
declare function initKpressCodeCopy(root: Document): void;
declare function positionTooltip(anchor: HTMLAnchorElement, tooltip: HTMLElement): void;
declare var siteKpressTooltipPosition:
  | ((anchor: HTMLAnchorElement, tooltip: HTMLElement) => void)
  | undefined;
