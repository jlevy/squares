# Architecture

Squarl currently has three services:

- `squarl`: the GoMLX application, running with the XLA/CUDA backend and GPU passthrough.
- `web`: a Go server with an embedded Vite/PixiJS live packing canvas.
- `tensorboard`: a CPU-only dashboard reading run metrics from the shared data directory.

The main and web Go modules live in the sibling `squarl/` and `web/` directories. Compose bind-mounts the repository
and runs the main service from `squarl/`. Its image creates a user from `DOCKERCOMPOSE_UID` and
`DOCKERCOMPOSE_GID`, preventing container tools from creating root-owned source files.
The CUDA image prioritizes Docker's host-injected `libcuda` over its bundled forward-compatibility library. This uses
CUDA 13.x minor-version compatibility on the supported GeForce GPUs, which require an NVIDIA 580-series or newer
driver.

The native CUDA domain layer represents one candidate for the fixed n=17 problem as 17 contiguous `Square` values
plus their common side length. The container is `[0, 1] x [0, 1]`. Each square remains exactly three `float`s: its
centre `(x, y)` and a counter-clockwise angle canonicalized to `[0, pi/2)`. CUDA targets only compute capability 12.0.

CUDA actions can translate or rotate one square, or the contact-connected component containing a selected square.
Contacts are derived from the incoming geometry before contraction. Each action contracts the common side length,
using an action factor clamped to `[0, 1]`, changes the selected geometry, then directly computes the maximum legal
side length from wall bounds and pairwise separating-axis bounds. It re-expands to `max(0, s_max - 1e-6)` without
moving the resulting centres. A zero side length is the legal fallback for degenerate geometry.

When episode tracing is enabled, the action kernel copies the exact contracted and transformed packings and selected
square mask to dedicated device buffers before legal re-expansion. These snapshots are copied to the host only for
the arrangement observer; ordinary planner and training paths do not add trace transfers.

Group rotation is rigid around the arithmetic centre of its member squares. A batched kernel applies one
device-copyable action per packing and returns the new side length and score `17 * s^2`, the covered container area.
No-op is a fifth action kind and still runs the measure-and-legalise path.

The first seven actions and the eighth all use only this cheap legalisation.
CUDA runs the rotation-enabled wall-pressure polisher twice per episode: once
on a copy of the initial state and once on a copy of the raw state after action
eight. The model still acts on the untouched initial state and its legal action
successors. One CUDA block owns each polished copy, moves virtual walls inward,
and performs many damped position-based constraint iterations without host
round trips. Wall penetrations and square overlaps produce centre corrections
and contact-point angular corrections. Failed wall steps are reduced, while
small deterministic escape perturbations help break contact locks; only
settled states advance the walls. Polishing first restores the maximum legal
side length for the incoming geometry, so its result is independent of both
the packing's batch position and any earlier contraction of its side length.

Every pressure trial is measured exactly with wall bounds and pairwise SAT.
The best measured trial is normalized by its rotated-corner bounding square,
with `2e-6` clearance, and re-legalized before return. The acted state remains
unchanged. Thus all model inputs are unpolished, and every returned terminal
polished result is legal.

An optional [topology-aware deep polisher](deep-polishing.md) runs sparsely on
promising fast-polished states. It freezes one inferred directed SAT separator
per pair, solves every centre and container width together in a float64 LP,
then refines clustered and finally independent angles while repeatedly
re-solving that LP. Only nearly tied SAT branches are searched. Direct and
float32-padded candidates must survive two deterministic CUDA replays plus an
independent geometry check; otherwise the legal fast-polished state remains
the fallback.

The GoMLX [packing model](model.md) is an edge-aware graph transformer over square, wall, and global nodes. It scores
a CUDA-generated set of 205 candidates: no-op, plus four translations and two rotations for each square in individual
and contact-group forms.

The experimental [monotone planner](monotone-planner.md) can instead use the
network only to shortlist actions. It restores arbitrary legal packings into a
reusable CUDA workspace, regenerates contact-dependent candidates, applies and
polishes shortlisted afterstates, and accepts only exact width improvements.
The environment restore operation changes no geometry and reopens candidate
generation after an earlier workspace has finished.

The bounded [horizon-4 actor–critic pilot](horizon4-rl-pilot.md) uses the fast
single-view scorer directly. It pads only for tensor shape, masks logits to
the current unique canonical actions, treats no-op as stop, and samples one
action without exact reranking. CUDA polishing supplies each logarithmic
width reward; GoMLX recomputes selected log-probabilities, fits the value
baseline and applies the clipped Adam update.

The stabilized pilot factorises that actor into stop/continue, dynamically
available family, and candidate-within-family distributions. Their
log-probabilities add for a non-stop action. It reports each entropy
separately; the Huber critic and policy use separately clipped gradients.

The bounded [horizon-8 curriculum](horizon8-curriculum.md) resumes one proven
hierarchical policy with fresh optimiser state for every seed. It forces
actions at newly introduced depths before enabling the learned stop gate
after four actions in the final phase.

The [same-horizon horizon-8 run](horizon8-same-horizon-rl.md) instead masks
stop and non-rotation families throughout. Four sampled trajectories share
each root, and leave-one-out group-relative returns train only the conditional
rotation candidate policy. A source-distribution KL penalty constrains the
fine-tune; fixed greedy and sampled cohorts select separate checkpoints.

For each requested batch, Go generates 64 random seeds on the host and sends
them to CUDA to start 64 device-resident packings. At fixed `s = 1/7`, CUDA
adds randomly oriented squares sequentially and rejects any centre/angle
candidate that crosses a wall or overlaps an earlier square. A small clearance
keeps centres apart; a sparse randomized grid is the bounded-attempt fallback.
Initialization does not invoke action contraction or re-expansion. Its
separate polished copy is used only as the reward baseline.

CUDA then derives model inputs and legalises every selected action. An episode
contains eight actions with no intermediate reward. After final polishing,
CUDA returns `log(final_polished_side / initial_polished_side)`; Go assigns
that credit to all eight decisions. Training samples from the candidate
softmax. Go retains each complete candidate set, replays all eight stored
states through GoMLX, and uses the selected log-probabilities in a
batch-normalised REINFORCE loss with an entropy bonus. Adam updates the model
once per batch after global gradient clipping. Frozen evaluation is a separate
greedy mode.

Each process run shares one timestamped identifier across its artifacts. GoMLX checkpoints are retained under
`data/models/<run>/` every 32 model versions and once for the final version. A manifest maps model versions to GoMLX
checkpoint pairs. CUDA retains each episode's raw initial, polished initial,
final unpolished, and final polished geometries. Only final polished states
are record-eligible. Go
compares them across the run and atomically replaces
`data/arrangements/<run>.json` whenever the common side length improves. Under
a cross-process file lock, it also replaces
`data/best-ever.json` only for a strict all-time improvement.
The checkpoints also retain Adam moments and step, GoMLX's categorical
sampling state, the run configuration, and best-packing metadata. A run can be
resumed from its latest checkpoint without resetting Adam.

Every replay-verified run best is POSTed as JSON to the web service at
`/api/arrangements`. The backend validates each arrangement. The strongest
episode from the most recently active run is retained at
`/api/arrangements/live`, while the all-time record is retained independently
at `/api/arrangements/best-ever/live`. The
best complete eight-action episode in every batch is also atomically saved at
`data/episodes/<run>/latest.json`; strict replay improvements update
`best.json`. On startup the newest `latest.json` identifies the active run,
its `best.json` restores the first stream, and `data/best-ever.json` restores
the second. Production searches outside the normal episode runner must use
`artifacts.MonitorLiveArrangement` for the same persistence and publication
contract. Each traced update includes the
raw and polished initial states, a complete phase-level trace of all eight
actions, the terminal polish, an optional deep-refinement endpoint, and whether
it set the all-time record. Saved and live episodes therefore replay
identically. The two PixiJS [episode debugger](episode-debugger.md) players
reconnect automatically and independently provide playback, phase stepping,
speed control, and timeline scrubbing. The
record payload also carries John Bidwell's
best-known n=17 container width, `4.67553009360455`. A strictly narrower result is shown
prominently as a world-record candidate requiring independent verification;
the optimum is not proven. A float32-safe copy of Bidwell's construction is
stored at `data/world-record.json` for direct comparison; see
[the reference notes](world-record-reference.md). See also the
[published packing table](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html)
and [Erich Friedman's survey](https://erich-friedman.github.io/papers/squares/squares.html).

The main process also writes TensorBoard event files under
`data/tensorboard/<run>/`. Every completed batch reports final unpolished and
polished side lengths, polishing gains, covered area, mean and p95 final
container width (`1/s`), polished endpoint scores, reward distribution,
improvement fraction, policy loss, entropy, gradient and parameter-update
norms, selected-action probabilities, action-type frequencies, learning rate,
batch size, and model version. TensorBoard recursively watches these streams.
