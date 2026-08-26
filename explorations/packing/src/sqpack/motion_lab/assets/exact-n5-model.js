"use strict";
function scalar(value) { return Number(value.decimal); }
function baseAngle(square) { return Number(square.orientation.radians || 0); }

function posesAt(scene, progress, tangent) {
  const extent = scalar(scene.parameter.upper);
  const parameter = extent * progress;
  return scene.squares.map((square) => {
    const x = scalar(square.centre_start.x) + parameter * scalar(square.centre_derivative.x);
    const y = scalar(square.centre_start.y) + parameter * scalar(square.centre_derivative.y);
    const velocity = scalar(square.angle_derivative_at_zero);
    let angle = baseAngle(square);
    if (scene.mode === "certified-path" && square.orientation.kind === "rational-half-angle") {
      angle = tangent ? scene.sigma * parameter : 2 * Math.atan(scene.sigma * parameter / 2);
    } else if (scene.mode === "second-order-obstruction" && tangent) {
      angle += velocity * parameter;
    }
    return { id: square.id, x, y, angle };
  });
}
function phaseAt(scene, progress) {
  if (scene.mode === "second-order-obstruction" || progress === 0) return "base";
  if (progress === 1) return "endpoint";
  return "open_interval";
}

function sceneControlState(scene) {
  const certifiedPath = scene.mode === "certified-path";
  return {
    ownerDisabled: certifiedPath,
    playDisabled: !certifiedPath,
    branchHidden: certifiedPath,
  };
}

function normalizedPercent(progress) {
  return (progress * 100).toFixed(1).replace(/\.0$/, "");
}

function parameterValueText(scene, progress) {
  const value = scalar(scene.parameter.upper) * progress;
  return `${normalizedPercent(progress)}% of interval; ${scene.parameter.name} = ${value.toFixed(7)}`;
}

function stageDescriptionText(scene, progress) {
  const percent = normalizedPercent(progress);
  const phase = phaseAt(scene, progress);
  const contacts = (scene.contacts[phase] || [])
    .map((pair) => `${pair[0]}–${pair[1]}`)
    .join(", ");
  if (scene.mode === "second-order-obstruction") {
    return `Five unit squares in a fixed square container, showing +W at ${scene.stratum}. `
      + `The solid packing stays at its base pose; the dashed first-order predictor is `
      + `shown at ${percent}% of the display scale and is obstructed at second order. `
      + `Base contact pairs: ${contacts}.`;
  }
  return `Five unit squares in a fixed square container, showing ${scene.class} at `
    + `${scene.stratum}, ${percent}% through the certified path. Solid squares show the `
    + `exact pose; dashed squares, when enabled, show the first-order tangent predictor. `
    + `Active contact pairs: ${contacts}.`;
}
