// The instrumentation `check_math_startup`'s init script (`startup.js`) installs as
// `__mathStartup`: what it counts and times while the page starts, and `finish`, which stops
// it and returns the report.

/** One observed call: a font load, a runtime call, or a KaTeX render. */
interface SquaresMathStartupCall {
  kind?: "face" | "set";
  start_ms: number;
  request?: string;
  source?: string;
  target?: string | null;
  outcome?: "pending" | "resolved" | "rejected" | "threw";
  end_ms?: number;
  error?: string;
  duration_ms?: number;
}

/** Where one tracked text character was on one sampled frame. */
interface SquaresMathStartupPosition {
  at_ms: number;
  x: number;
  y: number;
  bottom: number;
  local_x: number;
  local_y: number;
  local_bottom: number;
}

/** One persistent text character beside mathematics, and how far it has moved. */
interface SquaresMathStartupAnchor {
  id: string;
  category: "prose" | "caption" | "parameter";
  text: string;
  character: string | undefined;
  offset: number;
  block: string;
  samples: number;
  initial: SquaresMathStartupPosition | null;
  final: SquaresMathStartupPosition | null;
  max_absolute_px: number;
  max_local_px: number;
  max_start_x_px: number;
  max_start_y_px: number;
  max_bottom_px: number;
  bounds?: Partial<
    Record<Exclude<keyof SquaresMathStartupPosition, "at_ms">, { min: number; max: number }>
  >;
}

/** The anchor fields that hold a largest displacement. */
type SquaresMathStartupAnchorExtent =
  | "max_absolute_px"
  | "max_local_px"
  | "max_start_x_px"
  | "max_start_y_px"
  | "max_bottom_px";

/** The viewport and certificate state on one frame. */
interface SquaresMathStartupSnapshot {
  at_ms: number;
  width: number;
  height: number;
  scroll_x: number;
  scroll_y: number;
  document_scroll_x: number;
  document_scroll_y: number;
  visibility: DocumentVisibilityState;
  focused: boolean;
  hash: string;
  document_ready_state: DocumentReadyState;
  math_ready: boolean;
  certificate_elements: number;
  active_certificates: (string | undefined)[];
}

interface SquaresMathStartupState {
  mode: string;
  metrics: Record<string, number | null | undefined>;
  counters: {
    frames: number;
    font_hooks: number;
    katex_hooks: number;
    runtime_hooks: number;
    katex_calls: number;
    ready_calls: number;
    render_calls: number;
    hydrate_calls: number;
    hydrate_hooks: number;
    anchor_samples: number;
  };
  capabilities: { longtask: boolean; layout_shift: boolean };
  fonts: SquaresMathStartupCall[];
  ready: SquaresMathStartupCall[];
  renders: SquaresMathStartupCall[];
  hydrates: SquaresMathStartupCall[];
  katex: SquaresMathStartupCall[];
  longtasks: object[];
  shifts: object[];
  targets: object[];
  anchors: SquaresMathStartupAnchor[];
  snapshots: SquaresMathStartupSnapshot[];
  errors: string[];
  stop: boolean;
  pre_reveal_frame_observed: boolean;
  pending_observed: boolean;
  settlement_state?: "pending" | "resolved" | "rejected";
  finish?: () => object;
  source?: { url: string; title: string; revision_url: string | null };
}

declare var __mathStartup: SquaresMathStartupState | undefined;
