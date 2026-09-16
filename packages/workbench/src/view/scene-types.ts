/** A renderer receives geometry and presentation decisions, never a solver or controller. */
export interface SceneSquare {
  index: number;
  identity: number;
  x: number;
  y: number;
  angleDegrees: number;
  opacity: number;
  scale: number;
}

export interface SceneMark {
  x: number;
  y: number;
  angleDegrees: number;
  scale: number;
  opacity: number;
  strokeWidth: number;
}

export interface SceneFrame {
  pairIndex: number;
  n: number;
  containerSide: number;
  /** SVG coordinates; the square layer reflects the mathematical y axis. */
  viewBox: { x: number; y: number; size: number };
  squares: readonly SceneSquare[];
  presentation: {
    drain: number;
    newTint: number;
    resting: number;
    homeward: boolean;
    mark: SceneMark | null;
    linksOpacity: number;
    ghostOpacity: number;
  };
  /** Motion metadata cannot confer numerical assurance on an interpolated frame. */
  motion: "direct-illustration" | "physical-illustration" | "packing-snapshot";
}

export interface PaintedSceneFrame {
  scene: SceneFrame;
  /** One checked CSS colour for each square, in scene order. */
  fills: readonly string[];
}

export interface TrajectoryReader {
  samplePose(index: number, progress: number): readonly [number, number, number];
  sampleSide(progress: number): number;
  missSide: number;
}
