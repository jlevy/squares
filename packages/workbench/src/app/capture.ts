import type { PaintedSceneFrame } from "../view/scene-types.js";
import { sceneSvg } from "../view/stage-renderer.ts";

export const CAPTURE_SCHEMA = "squares.workbench.capture/v1";

export interface CaptureTiming {
  startSeconds: number;
  durationSeconds: number;
  framesPerSecond: number;
  includeEndpoint: boolean;
  maxFrames: number;
}

export interface CaptureSource {
  commit: string;
  inputId: string;
  configurationId: string;
}

export interface CapturedFrame {
  index: number;
  seconds: number;
  n: number;
  motion: PaintedSceneFrame["scene"]["motion"];
  svg: string;
}

export interface CaptureReceipt {
  schema: typeof CAPTURE_SCHEMA;
  source: CaptureSource;
  timing: CaptureTiming;
  status: "completed" | "cancelled" | "failed";
  error: string | null;
  scheduledFrames: number;
  frames: CapturedFrame[];
}

/** Integer frame indices avoid accumulated clock drift; the terminal still is explicit. */
export function captureTimes(timing: CaptureTiming): number[] {
  if (
    !Number.isFinite(timing.startSeconds) ||
    timing.startSeconds < 0 ||
    !Number.isFinite(timing.durationSeconds) ||
    timing.durationSeconds < 0 ||
    !Number.isFinite(timing.framesPerSecond) ||
    timing.framesPerSecond <= 0 ||
    !Number.isSafeInteger(timing.maxFrames) ||
    timing.maxFrames < 1
  ) {
    throw new RangeError(
      "capture requires finite nonnegative times and positive bounded frame counts",
    );
  }
  const endpoint = timing.startSeconds + timing.durationSeconds;
  let regular = Math.ceil(timing.durationSeconds * timing.framesPerSecond);
  // A product rounded above an integer must not add the endpoint twice.
  if (regular > 0 && (regular - 1) / timing.framesPerSecond >= timing.durationSeconds) {
    regular--;
  }
  const count = timing.durationSeconds === 0 ? 1 : regular + Number(timing.includeEndpoint);
  if (!Number.isFinite(endpoint) || !Number.isSafeInteger(count) || count > timing.maxFrames) {
    throw new RangeError("capture exceeds its declared frame budget");
  }
  const times = Array.from({ length: count }, (_unused, index) =>
    index === regular || timing.durationSeconds === 0
      ? endpoint
      : timing.startSeconds + index / timing.framesPerSecond,
  );
  return times;
}

/** Capture calls the same pure seek function as playback; cancellation retains completed frames. */
export async function captureIllustration(options: {
  source: CaptureSource;
  timing: CaptureTiming;
  seek: (seconds: number) => PaintedSceneFrame;
  cancelled: () => boolean;
  writeFrame: (frame: CapturedFrame) => Promise<void>;
}): Promise<CaptureReceipt> {
  const { source, timing, seek, cancelled, writeFrame } = options;
  if (!/^[a-f0-9]{40}$/.test(source.commit) || !source.inputId || !source.configurationId) {
    throw new TypeError("capture requires its source commit, input and configuration identity");
  }
  const times = captureTimes(timing);
  const receipt: CaptureReceipt = {
    schema: CAPTURE_SCHEMA,
    source: { ...source },
    timing: { ...timing },
    status: "completed",
    error: null,
    scheduledFrames: times.length,
    frames: [],
  };
  for (const [index, seconds] of times.entries()) {
    if (cancelled()) {
      receipt.status = "cancelled";
      break;
    }
    try {
      const sampled = seek(seconds);
      const frame: CapturedFrame = {
        index,
        seconds,
        n: sampled.scene.n,
        motion: sampled.scene.motion,
        svg: sceneSvg(sampled),
      };
      await writeFrame(frame);
      receipt.frames.push(frame);
    } catch (error) {
      receipt.status = "failed";
      receipt.error = error instanceof Error ? error.message : String(error);
      break;
    }
  }
  return receipt;
}
