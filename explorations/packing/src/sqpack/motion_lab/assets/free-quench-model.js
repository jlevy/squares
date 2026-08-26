(() => {
  "use strict";

  const EPSILON = 1e-10;
  const QUARTER_TURN = Math.PI / 2;
  const WALLS = ["left", "right", "bottom", "top"];

  function copyState(state) {
    return {
      side: state.side,
      squares: state.squares.map((square) => ({...square})),
      groups: state.groups.map((group) => [...group]),
      snapping_enabled: state.snapping_enabled,
    };
  }

  function groupFor(state, squareId) {
    const group = state.groups.find((value) => value.includes(squareId));
    if (!group) throw new Error(`unknown editor square ID: ${squareId}`);
    return group;
  }

  function axes(square) {
    const cosine = Math.cos(square.theta);
    const sine = Math.sin(square.theta);
    return [[cosine, sine], [-sine, cosine]];
  }

  function halfExtent(square, axis) {
    const [axisX, axisY] = axis;
    const cosine = Math.cos(square.theta);
    const sine = Math.sin(square.theta);
    return 0.5 * (
      Math.abs(axisX * cosine + axisY * sine)
      + Math.abs(-axisX * sine + axisY * cosine)
    );
  }

  function corners(square) {
    const cosine = Math.cos(square.theta);
    const sine = Math.sin(square.theta);
    return [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([signX, signY]) => [
      square.x + 0.5 * (signX * cosine - signY * sine),
      square.y + 0.5 * (signX * sine + signY * cosine),
    ]);
  }

  function pairGap(first, second) {
    const deltaX = first.x - second.x;
    const deltaY = first.y - second.y;
    return Math.max(...axes(first).concat(axes(second)).map((axis) => (
      Math.abs(deltaX * axis[0] + deltaY * axis[1])
      - halfExtent(first, axis)
      - halfExtent(second, axis)
    )));
  }

  function insideContainer(square, side) {
    const horizontal = halfExtent(square, [1, 0]);
    const vertical = halfExtent(square, [0, 1]);
    return square.x - horizontal >= -EPSILON
      && square.x + horizontal <= side + EPSILON
      && square.y - vertical >= -EPSILON
      && square.y + vertical <= side + EPSILON;
  }

  function editorDiagnostics(state) {
    const overlapPairs = [];
    for (let first = 0; first < state.squares.length; first += 1) {
      for (let second = first + 1; second < state.squares.length; second += 1) {
        if (pairGap(state.squares[first], state.squares[second]) < -EPSILON) {
          overlapPairs.push([
            state.squares[first].square_id,
            state.squares[second].square_id,
          ]);
        }
      }
    }
    return {
      overlap_pairs: overlapPairs,
      outside_square_ids: state.squares
        .filter((square) => !insideContainer(square, state.side))
        .map((square) => square.square_id),
    };
  }

  function translateGroup(state, squareId, dx, dy) {
    const output = copyState(state);
    const moving = new Set(groupFor(output, squareId));
    output.squares = output.squares.map((square) => (
      moving.has(square.square_id)
        ? {...square, x: square.x + dx, y: square.y + dy}
        : square
    ));
    return output;
  }

  function rotateGroup(state, squareId, delta) {
    const output = copyState(state);
    const group = groupFor(output, squareId);
    const moving = new Set(group);
    const members = output.squares.filter((square) => moving.has(square.square_id));
    const pivotX = members.reduce((sum, square) => sum + square.x, 0) / members.length;
    const pivotY = members.reduce((sum, square) => sum + square.y, 0) / members.length;
    const cosine = Math.cos(delta);
    const sine = Math.sin(delta);
    output.squares = output.squares.map((square) => {
      if (!moving.has(square.square_id)) return square;
      const offsetX = square.x - pivotX;
      const offsetY = square.y - pivotY;
      return {
        ...square,
        x: pivotX + cosine * offsetX - sine * offsetY,
        y: pivotY + sine * offsetX + cosine * offsetY,
        theta: square.theta + delta,
      };
    });
    return output;
  }

  function validCandidate(state, movingGroup, dx, dy) {
    const moved = translateGroup(state, movingGroup[0], dx, dy);
    const moving = new Set(movingGroup);
    if (moved.squares.some(
      (square) => moving.has(square.square_id) && !insideContainer(square, moved.side),
    )) return false;
    return !moved.squares.some((first) => moving.has(first.square_id)
      && moved.squares.some((second) => !moving.has(second.square_id)
        && pairGap(first, second) < -EPSILON));
  }

  function candidateRecord({
    dx,
    dy,
    distance,
    targetKind,
    targetId,
    movingGroup,
    stationaryGroup = [],
    rank,
  }) {
    return {
      result: {
        dx,
        dy,
        distance,
        target_kind: targetKind,
        target_id: String(targetId),
        moving_group: [...movingGroup],
        stationary_group: [...stationaryGroup],
      },
      rank,
    };
  }

  function squareCandidates(state, movingGroup, threshold) {
    const moving = new Set(movingGroup);
    const byId = new Map(state.squares.map((square) => [square.square_id, square]));
    const candidates = [];
    for (const movingId of movingGroup) {
      const first = byId.get(movingId);
      for (const second of state.squares) {
        if (moving.has(second.square_id)) continue;
        const stationaryGroup = groupFor(state, second.square_id);
        const deltaX = first.x - second.x;
        const deltaY = first.y - second.y;
        for (const [axisOrder, axis] of axes(first).concat(axes(second)).entries()) {
          const projection = deltaX * axis[0] + deltaY * axis[1];
          const sign = projection >= 0 ? 1 : -1;
          const contactProjection = sign * (
            halfExtent(first, axis) + halfExtent(second, axis)
          );
          const amount = contactProjection - projection;
          const dx = amount * axis[0];
          const dy = amount * axis[1];
          const distance = Math.abs(amount);
          const translated = {...first, x: first.x + dx, y: first.y + dy};
          if (distance <= threshold
            && validCandidate(state, movingGroup, dx, dy)
            && Math.abs(pairGap(translated, second)) <= EPSILON) {
            candidates.push(candidateRecord({
              dx,
              dy,
              distance,
              targetKind: "square",
              targetId: second.square_id,
              movingGroup,
              stationaryGroup,
              rank: [distance, second.square_id, movingId, axisOrder, sign < 0 ? 0 : 1],
            }));
          }
        }
        for (const [movingCorner, firstCorner] of corners(first).entries()) {
          for (const [stationaryCorner, secondCorner] of corners(second).entries()) {
            const dx = secondCorner[0] - firstCorner[0];
            const dy = secondCorner[1] - firstCorner[1];
            const distance = Math.hypot(dx, dy);
            const translated = {...first, x: first.x + dx, y: first.y + dy};
            if (distance <= threshold
              && validCandidate(state, movingGroup, dx, dy)
              && Math.abs(pairGap(translated, second)) <= EPSILON) {
              candidates.push(candidateRecord({
                dx,
                dy,
                distance,
                targetKind: "square",
                targetId: second.square_id,
                movingGroup,
                stationaryGroup,
                rank: [
                  distance,
                  second.square_id,
                  movingId,
                  4 + movingCorner * 4 + stationaryCorner,
                  0,
                ],
              }));
            }
          }
        }
      }
    }
    return candidates;
  }

  function wallCandidates(state, movingGroup, threshold) {
    const byId = new Map(state.squares.map((square) => [square.square_id, square]));
    const candidates = [];
    for (const movingId of movingGroup) {
      const square = byId.get(movingId);
      const horizontal = halfExtent(square, [1, 0]);
      const vertical = halfExtent(square, [0, 1]);
      const translations = [
        [horizontal - square.x, 0],
        [state.side - horizontal - square.x, 0],
        [0, vertical - square.y],
        [0, state.side - vertical - square.y],
      ];
      for (const [wallOrder, [dx, dy]] of translations.entries()) {
        const distance = Math.hypot(dx, dy);
        if (distance <= threshold && validCandidate(state, movingGroup, dx, dy)) {
          candidates.push(candidateRecord({
            dx,
            dy,
            distance,
            targetKind: "wall",
            targetId: WALLS[wallOrder],
            movingGroup,
            rank: [distance, state.squares.length + wallOrder, movingId, 0, 0],
          }));
        }
      }
    }
    return candidates;
  }

  function compareRanks(first, second) {
    for (let index = 0; index < first.length; index += 1) {
      if (first[index] !== second[index]) return first[index] - second[index];
    }
    return 0;
  }

  function applyBestSnap(state, movingSquareId, threshold) {
    if (!Number.isFinite(threshold) || threshold < 0) {
      throw new Error("snap threshold must be finite and non-negative");
    }
    const movingGroup = groupFor(state, movingSquareId);
    if (!state.snapping_enabled) return {state: copyState(state), result: null};
    const candidates = squareCandidates(state, movingGroup, threshold)
      .concat(wallCandidates(state, movingGroup, threshold));
    if (candidates.length === 0) return {state: copyState(state), result: null};
    candidates.sort((first, second) => compareRanks(first.rank, second.rank));
    const selected = candidates[0].result;
    const output = translateGroup(state, movingSquareId, selected.dx, selected.dy);
    if (selected.target_kind === "square") {
      const merged = [...selected.moving_group, ...selected.stationary_group]
        .sort((first, second) => first - second);
      const mergedIds = new Set(merged);
      output.groups = output.groups
        .filter((group) => !group.some((squareId) => mergedIds.has(squareId)))
        .concat([merged])
        .sort((first, second) => first[0] - second[0]);
    }
    return {state: output, result: selected};
  }

  function releaseQuenchRequest(state, maxSweeps, timeBudget) {
    const foldedAngles = state.squares.map((square) => (
      (square.theta % QUARTER_TURN + QUARTER_TURN) % QUARTER_TURN
    ));
    return {
      contract: "packing.squares:QuenchRequest/v1",
      schema_version: 1,
      side: state.side,
      x: state.squares.map((square) => square.x),
      y: state.squares.map((square) => square.y),
      theta: foldedAngles,
      solver: "quench-bracket",
      max_sweeps: maxSweeps,
      time_budget: timeBudget,
    };
  }

  function stateFromScenario(scenario) {
    const frame = scenario.initial_frame;
    return {
      side: frame.container_side,
      squares: frame.squares.map((square) => ({
        square_id: square.square_id,
        x: square.x,
        y: square.y,
        theta: square.theta,
      })),
      groups: frame.squares.map((square) => [square.square_id]),
      snapping_enabled: true,
    };
  }

  function phasePresentation(event) {
    const presentations = {
      setup: {label: "Setup released", variant: "setup"},
      "fixed-angle-lp": {label: "Fixed-angle LP", variant: "lp"},
      "angular-probe": {
        label: "Angular probe",
        variant: event.outcome === "rejected" ? "probe-rejected" : "probe",
      },
      "angle-accepted": {label: "Accepted rotation", variant: "accepted"},
      "cell-change": {label: "Cell change", variant: "cell"},
      stop: {label: "Stop", variant: "stop"},
    };
    return presentations[event.phase] || {label: event.phase, variant: "unknown"};
  }

  function selectPlaybackIndices(events, limit = 160) {
    if (!Number.isInteger(limit) || limit < 2) {
      throw new Error("playback event limit must be an integer of at least two");
    }
    if (events.length <= limit) return events.map((_, index) => index);
    const mandatoryPhases = new Set(["setup", "angle-accepted", "cell-change", "stop"]);
    const selected = new Set(events.flatMap((event, index) => (
      mandatoryPhases.has(event.phase) ? [index] : []
    )));
    const available = Math.max(0, limit - selected.size);
    if (available === 1) selected.add(Math.floor((events.length - 1) / 2));
    for (let slot = 0; slot < available && available > 1; slot += 1) {
      selected.add(Math.round(slot * (events.length - 1) / (available - 1)));
    }
    return [...selected].sort((first, second) => first - second);
  }

  function timelineWindow(length, index, radius = 20) {
    if (!Number.isInteger(length) || length < 1) throw new Error("timeline must not be empty");
    if (!Number.isInteger(index) || index < 0 || index >= length) {
      throw new Error("timeline index is outside the trace");
    }
    const width = Math.min(length, 2 * radius + 1);
    const start = Math.max(0, Math.min(index - radius, length - width));
    return {start, end: start + width};
  }

  globalThis.MotionLabEditor = Object.freeze({
    EPSILON,
    applyBestSnap,
    copyState,
    editorDiagnostics,
    groupFor,
    pairGap,
    phasePresentation,
    releaseQuenchRequest,
    rotateGroup,
    selectPlaybackIndices,
    stateFromScenario,
    timelineWindow,
    translateGroup,
  });
})();
