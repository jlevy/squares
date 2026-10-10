/** What `atlas-view.js` wires in a page, which `atlas-grid.js` hands it. A browser-only
 * declaration file: the Node program that shares `types.d.ts` has no DOM. */

/** One atlas block's parts: the block, the box of tiles, the tablist of views and the
 * tablist of sizes, which a page may lack. */
interface SiteAtlasParts {
  block: HTMLElement;
  cells: HTMLElement;
  tabs: HTMLElement | null;
  sizes: HTMLElement | null;
  /** Keep view/size state local and preserve the cells' ordinary semantics. */
  scoped?: boolean;
  /** Complete the visible preview with freshly measured capacity, before layout writes. */
  beforeArrange?: (capacity: number) => void;
  scales?: HTMLElement | null;
}

/** A mounted block's two acts: arrange the triangle for the width, and change the
 * layout with every tile moved from where it was to where it then is. */
interface SiteAtlasViews {
  arrange(): void;
  change(mutate: () => void): void;
}

interface SiteAtlasViewApi {
  mount(parts: SiteAtlasParts): SiteAtlasViews;
}
