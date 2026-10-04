/** What `atlas-view.js` wires in a page, which `atlas-grid.js` hands it. A browser-only
 * declaration file: the Node program that shares `types.d.ts` has no DOM. */

/** One atlas block's parts: the block, the box of tiles and the tablist of views. */
interface SiteAtlasParts {
  block: HTMLElement;
  cells: HTMLElement;
  tabs: HTMLElement;
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

/** One atlas block's drawing parts: the block, the box of tiles, the tablist of drawings
 * and the template of regularized tiles. */
interface SiteAtlasLayerParts {
  block: HTMLElement;
  cells: HTMLElement;
  tabs: HTMLElement;
  template: HTMLTemplateElement;
}

/** A mounted block's one act: make every placed tile the drawing the block is in. */
interface SiteAtlasLayers {
  apply(): void;
}

interface SiteAtlasLayerApi {
  mount(parts: SiteAtlasLayerParts): SiteAtlasLayers;
}
