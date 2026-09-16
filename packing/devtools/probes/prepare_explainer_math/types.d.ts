// What `prepare_explainer_math`'s probes install on a page and read back, and the shapes
// its measurement probes share.

/** One math slot as the build measured it: its key, inner HTML, and math attributes. */
interface SquaresPreparedFragment {
  key: number;
  html: string;
  attributes: Record<string, string>;
}

/** One base's measured font size and width, and the width normalised from a 16x sample. */
interface SquaresLinearGeometry {
  fontSize: number;
  width: number;
  linearWidth: number;
  textRendering: string;
}

/** `measure_math`: the slot measurement, carrying its measurement of one base. */
type SquaresMeasureMath = ((attributeNames: string[]) => SquaresPreparedFragment[]) & {
  linearGeometry(base: HTMLElement): SquaresLinearGeometry;
};

/** `geometry_font_trace`: when math was first requested, and what the gate held or saw fail. */
interface SquaresGeometryFontTrace {
  time_origin_ms: number;
  first_math_request_ms: number | null;
  before_snapshot_complete: boolean;
  root_watchdog_paused: boolean;
  queued_calls: number;
  rejections: { source: string; elapsed_ms: number; reason: string }[];
}

/** `queue_watchdog_hold`: the batches held from the host's scheduler. */
interface SquaresQueueControl {
  readonly count: number;
  release(): void;
}

declare var __squaresGeometryBoxes: HTMLElement[] | undefined;
declare var __squaresGeometryFontTrace: SquaresGeometryFontTrace | undefined;
declare var __squaresMarkGeometryBeforeSnapshotComplete: (() => void) | undefined;
declare var __squaresReleaseGeometryFontGate: (() => void) | undefined;
declare var __squaresQueueControl: SquaresQueueControl | undefined;
declare var __squaresQueuedControlNodes: HTMLElement[] | undefined;
declare var __brokenGeometry: [HTMLElement, string, string] | undefined;
declare var __squaresHeatDraws: string[] | undefined;
declare var __squaresRejectedFonts: number | undefined;
