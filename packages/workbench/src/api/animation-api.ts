/** Imported animation state is separate from the retained catalogue's transition cursor. */
export interface AnimationPanelState {
  active: boolean;
  loaded: boolean;
  playing: boolean;
  time: number;
  durationSeconds: number | null;
  revision: number;
  n: number | null;
  guided: boolean | null;
  interpolated: boolean | null;
  valid: boolean | null;
}
