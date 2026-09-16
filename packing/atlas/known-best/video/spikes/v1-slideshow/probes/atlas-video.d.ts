// What the slideshow's page script, `assets/slideshow.js`, assigns to `window.atlasVideo`: the
// timeline API that `render_review.py` drives through its probes and that `test_candidate.py`'s
// harness exercises. The page script is checked against this declaration where it assigns the
// object, so the two cannot drift apart.

/** One instant of the slideshow: which n shows, which is fading in, and where the bar is. */
interface AtlasVideoState {
  time: number;
  n: number;
  /** The n fading in after this one, or 0 after the last. */
  next: number;
  /** How far through the fade, 0 through the dwell. */
  progress: number;
  phase: "fade" | "dwell";
  /** The n the facts panel shows, which cuts at the fade's midpoint; 0 past the last. */
  panel: number;
  /** The progress bar's position, 0 to 1. */
  bar: number;
}

interface AtlasVideoTiming {
  dwell: number;
  fade: number;
}

interface AtlasVideo {
  seek(seconds: number): AtlasVideoState;
  frameAt(index: number, fps: number): AtlasVideoState;
  duration(): number;
  play(): void;
  pause(): void;
  setTiming(options?: Partial<AtlasVideoTiming> | null): AtlasVideoTiming & { duration: number };
  stateAt(t: number): AtlasVideoState;
  barAt(t: number): number;
  setSettle(on: boolean): void;
  setCapture(on: boolean): void;
  timing(): AtlasVideoTiming;
  count: number;
  /** Resolves once the document's fonts have loaded. */
  ready: Promise<unknown>;
}

interface Window {
  atlasVideo: AtlasVideo;
}
