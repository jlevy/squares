/**
 * A draggable separator between two stacked regions.
 *
 * The look and the no-layout-space strip follow metabrowser's resize handle
 * (`src/metabrowser/static/styles.css`, `.resize-handle`). The behaviour goes further than
 * that handle does: pointer events with capture, so a drag survives passing over the stage's
 * SVG; a keyboard-operable `role="separator"`; a double-click that returns the page to its
 * automatic layout; and a position that is clamped every time it is placed, so a caller that
 * re-reads its bounds on a window resize keeps the separator inside them.
 */

/** The range a separator may be placed in, in CSS pixels from the top of the viewport. */
export interface SeparatorBounds {
  readonly min: number;
  readonly max: number;
}

/** How far one arrow key moves the separator, and one arrow key with Shift held. */
export const SEPARATOR_STEP = 16;
export const SEPARATOR_LARGE_STEP = 64;

/** Keeps a position inside its bounds. An empty range, max below min, collapses to min. */
export function clampSeparator(position: number, bounds: SeparatorBounds): number {
  if (![position, bounds.min, bounds.max].every(Number.isFinite)) {
    throw new RangeError("separator position and bounds must be finite");
  }
  return Math.min(Math.max(position, bounds.min), Math.max(bounds.min, bounds.max));
}

/**
 * Where a key moves a horizontal separator: up and down by a step, a larger one with Shift,
 * and Home and End to either bound. Null for a key the separator does not use.
 */
export function keyedSeparatorPosition(
  key: string,
  position: number,
  bounds: SeparatorBounds,
  large: boolean,
): number | null {
  const step = large ? SEPARATOR_LARGE_STEP : SEPARATOR_STEP;
  switch (key) {
    case "ArrowUp":
      return clampSeparator(position - step, bounds);
    case "ArrowDown":
      return clampSeparator(position + step, bounds);
    case "Home":
      return clampSeparator(bounds.min, bounds);
    case "End":
      return clampSeparator(bounds.max, bounds);
    default:
      return null;
  }
}

export interface ResizeHandleOptions {
  readonly document: Document;
  readonly handle: HTMLElement;
  /** Where the separator is now, in CSS pixels from the top of the viewport. */
  position(): number;
  /** Where it may go, read afresh on every placement. */
  bounds(): SeparatorBounds;
  /** Moves the separator to a clamped position, or back to the automatic layout on null. */
  place(position: number | null): void;
  /** The spoken value, for `aria-valuetext`. */
  describe(position: number): string;
}

export interface ResizeHandle {
  /** Writes the current position and bounds into the handle's ARIA state. */
  sync(): void;
  dispose(): void;
}

export function mountResizeHandle(options: ResizeHandleOptions): ResizeHandle {
  const { document, handle } = options;
  let drag: { pointerId: number; startY: number; startPosition: number } | null = null;

  const sync = (): void => {
    const bounds = options.bounds();
    const position = clampSeparator(options.position(), bounds);
    handle.setAttribute("aria-valuemin", String(Math.round(bounds.min)));
    handle.setAttribute("aria-valuemax", String(Math.round(Math.max(bounds.min, bounds.max))));
    handle.setAttribute("aria-valuenow", String(Math.round(position)));
    handle.setAttribute("aria-valuetext", options.describe(position));
  };
  const place = (position: number | null): void => {
    options.place(position === null ? null : clampSeparator(position, options.bounds()));
    sync();
  };
  const finish = (pointerId: number): void => {
    drag = null;
    if (handle.hasPointerCapture(pointerId)) {
      handle.releasePointerCapture(pointerId);
    }
    document.body.classList.remove("resizing");
  };

  const onPointerDown = (event: PointerEvent): void => {
    if (event.button !== 0) {
      return;
    }
    drag = { pointerId: event.pointerId, startY: event.clientY, startPosition: options.position() };
    handle.setPointerCapture(event.pointerId);
    document.body.classList.add("resizing");
    event.preventDefault();
  };
  const onPointerMove = (event: PointerEvent): void => {
    if (drag !== null && event.pointerId === drag.pointerId) {
      place(drag.startPosition + event.clientY - drag.startY);
    }
  };
  const onPointerEnd = (event: PointerEvent): void => {
    if (drag !== null && event.pointerId === drag.pointerId) {
      finish(event.pointerId);
    }
  };
  const onKeyDown = (event: KeyboardEvent): void => {
    const next = keyedSeparatorPosition(
      event.key,
      options.position(),
      options.bounds(),
      event.shiftKey,
    );
    if (next !== null) {
      // The key is the separator's alone. The page's shortcuts listen on the window, where Home
      // and End rewind or finish the step, or seek an imported animation.
      event.preventDefault();
      event.stopPropagation();
      place(next);
    }
  };
  const onDoubleClick = (): void => {
    place(null);
  };

  handle.addEventListener("pointerdown", onPointerDown);
  handle.addEventListener("pointermove", onPointerMove);
  handle.addEventListener("pointerup", onPointerEnd);
  handle.addEventListener("pointercancel", onPointerEnd);
  handle.addEventListener("keydown", onKeyDown);
  handle.addEventListener("dblclick", onDoubleClick);
  sync();

  return {
    sync,
    dispose() {
      if (drag !== null) {
        finish(drag.pointerId);
      }
      handle.removeEventListener("pointerdown", onPointerDown);
      handle.removeEventListener("pointermove", onPointerMove);
      handle.removeEventListener("pointerup", onPointerEnd);
      handle.removeEventListener("pointercancel", onPointerEnd);
      handle.removeEventListener("keydown", onKeyDown);
      handle.removeEventListener("dblclick", onDoubleClick);
    },
  };
}
