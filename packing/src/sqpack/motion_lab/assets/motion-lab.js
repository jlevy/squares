const byId = (id) => document.getElementById(id);
const scenarioRegistry = JSON.parse(byId("scenario-registry").textContent);
const scenarioDefinition = scenarioRegistry.scenarios.find(
  (scenario) => scenario.scenario_id === scenarioRegistry.default_scenario,
);
if (!scenarioDefinition) {
  throw new Error("Motion Lab default scenario is missing from its registry");
}
function scenarioHasCapability(capability) {
  return scenarioDefinition.capabilities.includes(capability);
}
const manifest = JSON.parse(byId("motion-data").textContent);
const scenes = new Map(manifest.scenes.map((scene) => [scene.id, scene]));
const motionSelect = byId("motion-select");
const stratumSelect = byId("stratum-select");
const ownerSelect = byId("owner-select");
const progressInput = byId("parameter-input");
const playButton = byId("play-button");
const restartButton = byId("restart-button");
const idsToggle = byId("ids-toggle");
const contactsToggle = byId("contacts-toggle");
const trailsToggle = byId("trails-toggle");
const tangentToggle = byId("tangent-toggle");
const liveRegion = byId("live-region");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const left = 42;
const bottom = 564;
const scale = 185;
const durationMilliseconds = 5000;
let animationFrame = null;
let animationStart = null;
let animationOrigin = 0;

playButton.hidden = !scenarioHasCapability("playback");
progressInput.disabled = !scenarioHasCapability("scrub");

function currentScene() { return scenes.get(`${motionSelect.value}:${stratumSelect.value}`); }
function currentProgress() { return Number(progressInput.value) / Number(progressInput.max); }
function transform(pose) {
  return `translate(${pose.x} ${pose.y}) rotate(${pose.angle * 180 / Math.PI})`;
}
function screenPoint(pose) { return [left + scale * pose.x, bottom - scale * pose.y]; }

function pairKey(pair) { return `${pair[0]}-${pair[1]}`; }
function contactLabel(pair) { return `${pair[0]}–${pair[1]}`; }

function setLine(line, first, second) {
  line.setAttribute("x1", first.x);
  line.setAttribute("y1", first.y);
  line.setAttribute("x2", second.x);
  line.setAttribute("y2", second.y);
}

function setShown(element, shown) {
  if (shown) element.removeAttribute("display");
  else element.setAttribute("display", "none");
}

function updateGeometry(scene, progress) {
  const obstruction = scene.mode === "second-order-obstruction";
  const actual = posesAt(scene, obstruction ? 0 : progress, false);
  const base = posesAt(scene, 0, false);
  const predictor = posesAt(scene, progress, true);
  const endpoint = posesAt(scene, 1, true);
  const extent = scalar(scene.parameter.upper);
  actual.forEach((pose, index) => {
    const square = byId(`square-${pose.id}`);
    square.setAttribute("transform", transform(pose));
    const ghost = byId(`ghost-${pose.id}`);
    ghost.setAttribute("transform", transform(predictor[index]));
    setShown(ghost, tangentToggle.checked && progress > 0);
    const label = byId(`label-${pose.id}`);
    const labelPoint = screenPoint(pose);
    label.setAttribute("x", labelPoint[0]);
    label.setAttribute("y", labelPoint[1] + 5);
    setShown(label, idsToggle.checked);
    const trail = byId(`trail-${pose.id}`);
    setLine(trail, base[index], endpoint[index]);
    const centreMoves = base[index].x !== endpoint[index].x || base[index].y !== endpoint[index].y;
    setShown(trail, trailsToggle.checked && centreMoves);
    const tangent = byId(`tangent-${pose.id}`);
    const start = base[index];
    const arrowEnd = {
      x: start.x + scalar(scene.squares[index].centre_derivative.x) * extent * .72,
      y: start.y + scalar(scene.squares[index].centre_derivative.y) * extent * .72,
    };
    setLine(tangent, start, arrowEnd);
    setShown(
      tangent,
      tangentToggle.checked && (start.x !== arrowEnd.x || start.y !== arrowEnd.y),
    );
  });
  setShown(byId("obstruction-badge"), obstruction);
  updateContacts(scene, progress, actual);
}

function updateContacts(scene, progress, poses) {
  const phase = phaseAt(scene, progress);
  const active = new Set((scene.contacts[phase] || []).map(pairKey));
  const persistent = new Set(["0-4", "2-4", "3-4"]);
  const obstruction = scene.mode === "second-order-obstruction";
  for (const key of ["0-3", "0-4", "1-4", "2-4", "3-4"]) {
    const line = byId(`contact-${key}`);
    const [first, second] = key.split("-").map(Number);
    setLine(line, poses[first], poses[second]);
    setShown(line, contactsToggle.checked && active.has(key));
    const stateClass = obstruction
      ? "base-only"
      : persistent.has(key)
        ? "persistent"
        : key === "1-4"
          ? "opening"
          : "closing";
    line.setAttribute("class", `contact-link ${stateClass}`);
  }
  const labels = (scene.contacts[phase] || []).map(contactLabel).join(", ");
  const event = obstruction
    ? "Base graph only; no feasible contact evolution is certified"
    : phase === "base"
      ? "1–4 opens immediately"
      : phase === "endpoint"
        ? "0–3 closes here"
        : "1–4 is open; 0–3 has not closed";
  byId("contacts-value").textContent = `${labels}. ${event}.`;
}

function updateReadout(scene, progress) {
  const value = scalar(scene.parameter.upper) * progress;
  progressInput.setAttribute("aria-valuetext", parameterValueText(scene, progress));
  byId("stage-description").textContent = stageDescriptionText(scene, progress);
  byId("scene-value").textContent = `${scene.class} at ${scene.stratum}`;
  byId("parameter-name").textContent = scene.parameter.name;
  byId("parameter-value").textContent = value.toFixed(7);
  byId("evidence-value").textContent = scene.evidence.status.replaceAll("-", " ");
  byId("source-value").textContent = scene.evidence.source_record;
  if (scene.evidence.geometry_source_record) {
    byId("source-value").textContent += `; ghost geometry: ${scene.evidence.geometry_source_record}`;
  }
  byId("claim-value").textContent = scene.evidence.claim;
  byId("claim-value").classList.toggle("obstructed", scene.mode === "second-order-obstruction");
  const controls = sceneControlState(scene);
  const rotating = controls.ownerDisabled;
  const angle = rotating ? 2 * Math.atan(scene.sigma * value / 2) * 180 / Math.PI : value * 180 / Math.PI;
  byId("angle-value").textContent = rotating
    ? `${angle.toFixed(5)}° on square 1; θ=2 atan(σu/2)`
    : `${angle.toFixed(5)}° linear ghost on squares 3 and 4`;
  ownerSelect.disabled = controls.ownerDisabled;
  playButton.disabled = controls.playDisabled;
  byId("branch-panel").hidden = controls.branchHidden;
  if (!rotating) {
    const branch = scene.branches[ownerSelect.value];
    const amount = scalar(branch.coefficient) * value * value;
    byId("branch-title").textContent = `${branch.label}: ${branch.quantity}`;
    byId("branch-formula").textContent = branch.formula;
    byId("branch-value").textContent = `displayed quadratic term: ${amount.toExponential(5)}`;
    byId("branch-note").textContent = branch.note;
  }
  byId("motion-note").textContent = reduceMotion
    ? "Reduced-motion preference detected: the lab starts paused; manual scrubbing remains available."
    : "The lab starts paused and runs one pass only after Play is pressed.";
}

function update() {
  const scene = currentScene();
  const progress = currentProgress();
  updateGeometry(scene, progress);
  updateReadout(scene, progress);
}

function stopPlayback() {
  if (animationFrame !== null) cancelAnimationFrame(animationFrame);
  animationFrame = null;
  animationStart = null;
  playButton.textContent = "Play";
}

function tick(timestamp) {
  if (animationStart === null) animationStart = timestamp;
  const elapsed = (timestamp - animationStart) / durationMilliseconds;
  const next = Math.min(1, animationOrigin + elapsed);
  progressInput.value = String(Math.round(next * Number(progressInput.max)));
  update();
  if (next >= 1) {
    stopPlayback();
    liveRegion.textContent = "Certified path reached its endpoint.";
    return;
  }
  animationFrame = requestAnimationFrame(tick);
}

function startPlayback() {
  if (currentScene().mode !== "certified-path") return;
  if (currentProgress() >= 1) progressInput.value = "0";
  animationOrigin = currentProgress();
  animationStart = null;
  playButton.textContent = "Pause";
  liveRegion.textContent = "Certified path playback started.";
  animationFrame = requestAnimationFrame(tick);
}

playButton.addEventListener("click", () => {
  if (animationFrame === null) startPlayback(); else stopPlayback();
});
restartButton.addEventListener("click", () => {
  stopPlayback();
  progressInput.value = "0";
  update();
  liveRegion.textContent = "Scene returned to its base configuration.";
});
progressInput.addEventListener("input", () => { stopPlayback(); update(); });
for (const select of [motionSelect, stratumSelect]) {
  select.addEventListener("change", () => {
    stopPlayback();
    progressInput.value = "0";
    update();
    liveRegion.textContent = `${currentScene().class} ${currentScene().stratum} scene selected.`;
  });
}
ownerSelect.addEventListener("change", update);
for (const toggle of [idsToggle, contactsToggle, trailsToggle, tangentToggle]) {
  toggle.addEventListener("change", update);
}
update();
