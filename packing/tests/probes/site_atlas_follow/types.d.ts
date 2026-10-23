// What `test_site_atlas_follow`'s probes read from a triangle that follows the scroll.

/** The pure functions of `overview/atlas-view.js` the probes read the triangle with. */
declare var SiteAtlasView: {
  along(tops: readonly number[], at: number): { index: number; through: number };
  curve(values: readonly number[], index: number, through: number): number;
};

/** The script's last reading of a following triangle (`site-atlas.d.ts`). */
interface HTMLElement {
  atlasFollow?: {
    scrolled: number;
    point: number;
    line: number;
    zoom: number;
    pan: number;
    nudge: number;
    end: number;
  };
}
