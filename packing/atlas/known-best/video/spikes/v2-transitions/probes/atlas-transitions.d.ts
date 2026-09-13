import type { AtlasTransitions } from "../../../../../../../packages/workbench/src/api/workbench-api.js";

declare global {
  type AtlasPhysics =
    import("../../../../../../../packages/workbench/src/api/workbench-api.js").AtlasPhysics;

  interface Window {
    atlasTransitions: AtlasTransitions;
    /** Samples parked by the gap-bar probes for collection by a later probe. */
    __samples: number[][];
  }

  /** CSS Fonts 4 descriptor used by the font-face probe but absent from `lib.dom.d.ts`. */
  interface FontFace {
    sizeAdjust: string;
  }
}
