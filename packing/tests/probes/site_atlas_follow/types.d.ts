// What `test_site_atlas_follow`'s probes read from a triangle that follows the scroll.

/** One reading of the atlas block and the page around it. */
interface AtlasFollowReading {
  /** `data-atlas-follow` on the block: "scroll", "held", or null when it never followed. */
  follow: string | null;
  /** Whether the root asked for following before the programs ran. */
  armed: boolean;
  /** Whether the triangle is drawn zoomed (`data-atlas-zoom`). */
  zoomed: boolean;
  view: string | null;
  size: string | null;
  explicit: boolean;
  /** The size tab marked selected. */
  shown: string | null;
  /** The zoom the rows are drawn at, 1 for none. */
  scale: number;
  /** The scroller's position: 0 at its start, the right edge, negative to the left. */
  pan: number;
  scrollY: number;
  /** The first tile's drawn width and the first case number's drawn size, in pixels. */
  tile: number;
  number: number;
  /** The focus line, from the window's top, and where it stands in the laid-out rows. */
  line: number;
  point: number;
  /** Where the left end of the row at the focus line stands from the block's left edge,
   * as a share of the block's width, and where the window's middle stands along that
   * row, as a share of its drawn width. */
  leftEnd: number;
  across: number;
  headerHidden: boolean;
  moving: number;
}

/** The pure functions of `overview/atlas-view.js` the probes read the triangle with. */
declare var SiteAtlasView: {
  focusLine(height: number, start: number, scrolled: number): number;
  along(tops: readonly number[], at: number): { index: number; through: number };
  between(from: number, to: number, through: number): number;
};
