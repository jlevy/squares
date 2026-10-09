// The global `test_site_atlas_views`'s probes install and read.

/** What `watch` records when the atlas's box of tiles is first put in the page. */
interface AtlasViewSeen {
  view: string | null;
  size: string | null;
  scale: string | null;
  per_line: string;
  tiles: number;
  moving: number;
}

declare var atlasViewsSeen: AtlasViewSeen[] | undefined;
