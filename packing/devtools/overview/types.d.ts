/** Types shared by the site's table script and its Node tests. */

type SiteTableSortType = "num" | "text";

interface SiteTableFilter {
  key: string;
  /**
   * How the control's value is held against the row's: equal to it, a flag that must be
   * set, a numeric bound, a first day the row's ISO date may be (which orders as it
   * reads), a number the row's list of numbers and ranges must hold, or a name the
   * row's list of names must have.
   */
  kind: "equals" | "flag" | "min" | "max" | "since" | "covers" | "has";
  value: string;
}

interface SiteTableApi {
  compareKeys(left: string, right: string, type: SiteTableSortType): number;
  sortOrder(
    keys: readonly string[],
    type: SiteTableSortType,
    direction: "ascending" | "descending",
  ): number[];
  covers(list: string, value: number): boolean;
  rowMatches(
    row: Readonly<Record<string, string | undefined>>,
    filters: readonly SiteTableFilter[],
  ): boolean;
  countText(shown: number, total: number, noun: string): string;
  localDay(now: Date): string;
  ageCutoff(today: string, days: string): string;
  controlParam(key: string, bound: string | null): string;
  init(): void;
}

declare var SiteTable: SiteTableApi;

/** The render-time sentinel `kpress-client.js` stands in for kpress's flattened client
 * (`render_overview.kpress_client_script`), as the explainer's own frame declares it. */
declare function __SQUARES_KPRESS_CLIENT_JS__(): void;

/** kpress's math enhancement, a classic script's top-level function. */
declare function enhanceMath(): Promise<void> | undefined;

/** The atlas's two views (`atlas-view.js`): the grid, and the triangle of rows by k. */
type AtlasView = "grid" | "triangle";

/** The atlas's three sizes of tile (`atlas-view.js`), Medium the default. */
type AtlasSize = "small" | "medium" | "large";

/**
 * Where a case stands in the triangle for the tiles a line holds: its row k, its line
 * from the top of the triangle, its column from the left, and whether its line opens a
 * row after the first.
 */
interface AtlasTrianglePlace {
  row: number;
  line: number;
  column: number;
  opens: boolean;
}

/** As much of a box as a move is worked out from: a `DOMRect` has all three. */
interface AtlasBox {
  left: number;
  top: number;
  width: number;
}

/** A tile's transform at the start of a move: a translation in pixels and a scale. */
interface AtlasMove {
  x: number;
  y: number;
  scale: number;
}

/** The pure functions of `atlas-view.js`, which the Node tests run with no document. */
interface SiteAtlasViewApi {
  row(n: number): number;
  widest(last: number): number;
  perLine(width: number, least: number, most: number, gap?: number): number;
  perLineAt(width: number, least: number, most: number, scale: number, gap?: number): number;
  place(n: number, per: number): AtlasTrianglePlace;
  viewOf(search: string): AtlasView;
  searchFor(search: string, view: AtlasView): string;
  sizeOf(search: string): AtlasSize;
  searchForSize(search: string, size: AtlasSize): string;
  stepTo(key: string, from: number, count: number): number;
  lengthPx(text: string, rootPx: number): number;
  milliseconds(text: string): number;
  moveFrom(first: AtlasBox, last: AtlasBox, holder: AtlasBox): AtlasMove;
  still(move: AtlasMove): boolean;
}

declare var SiteAtlasView: SiteAtlasViewApi;
