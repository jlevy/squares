/** What `atlas-view.js` wires in a page, which `atlas-grid.js` hands it. A browser-only
 * declaration file: the Node program that shares `types.d.ts` has no DOM. */

/** One atlas block's parts: the block, the box of tiles, the tablist of views and the
 * tablist of sizes, which a page may lack. */
interface SiteAtlasParts {
  block: HTMLElement;
  cells: HTMLElement;
  tabs: HTMLElement | null;
  sizes: HTMLElement | null;
  /** Keep view/size state local; geometry and FLIP remain shared with the dedicated Atlas. */
  scoped?: boolean;
  scales?: HTMLElement | null;
  drawings?: HTMLElement | null;
  /** Restart preparation for the sources selected by the drawing chooser. */
  onDrawingChange?: () => void;
}

/** A mounted block's two acts: arrange the triangle for the width, and change the
 * layout with every tile moved from where it was to where it then is. */
interface SiteAtlasViews {
  /** Font readiness captured during the initial layout read phase. */
  fontsReady: Promise<FontFaceSet>;
  arrange(): void;
  change(mutate: () => void): void;
  /** End scroll following: the reader has taken the atlas over. */
  hold(): void;
}

interface SiteAtlasViewApi {
  mount(parts: SiteAtlasParts): SiteAtlasViews;
}

/** The last reading of a triangle that follows the scroll (`atlas-view.js`): the scroll
 * since its stage was pinned, the point of the laid-out triangle at the focus line, the
 * focus line on the stage, the zoom, the pan as a right-to-left scroller reads it, the
 * reader's own share of the pan, the scroll at which the triangle's bottom reaches the
 * stage's, and how many times the triangle has been laid out. */
interface AtlasFollowReading {
  scrolled: number;
  point: number;
  line: number;
  zoom: number;
  pan: number;
  nudge: number;
  end: number;
  lays: number;
}

interface HTMLElement {
  atlasFollow?: AtlasFollowReading;
}
