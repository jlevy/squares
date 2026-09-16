# Squarl

Squarl is a reinforcement-learning library for the square-packing problem. It currently has a native CUDA
representation of 17 equal squares in a unit-square container and CUDA-native individual and contact-group actions.
Every action contracts, acts, and re-expands to a legal measured packing. A
non-mutating CUDA wall-pressure solver translates and rotates copies of the
initial and post-action-eight states. Their polished sizes provide the terminal
reward baseline and result, while only the final copy is record-eligible.
The GoMLX graph transformer supplies categorical policy logits for fixed
candidate action sets. The executable collects batches of 64 eight-action
episodes, calculates a polished terminal reward, and updates the policy with
batch-normalised REINFORCE, an entropy bonus, globally clipped gradients, and
Adam. Each initial state is constructed without overlap at `s = 1/7`.

The main Go application uses [GoMLX](https://github.com/gomlx/gomlx) with its XLA/CUDA backend. A separate Go web
application embeds a container-built Vite and PixiJS live packing visualizer.

## Run

The default environment targets the first CUDA device and maps container writes to the host user `1001:1001`.
Adjust the copied values when necessary:

```bash
cp .env.example .env
make docker-build
make run
```

`make run` performs one batch. Run any positive number of successive batches
under one run identifier with:

```sh
make train NO_OF_BATCHES=100
```

The underlying application flag is `--no-of-batches`, for example
`go run ./cmd/squarl --no-of-batches=100` from the main container after the
CUDA library has been built.

Rollouts always use the fast CUDA polisher. Enable sparse topology-aware deep
polishing for provisional records with `make train POLISH_MODE=deep`, or apply
it to one saved packing with `make deep-polish`; see
[deep polishing](docs/deep-polishing.md).

Long RL runs are currently paused behind the supervised one-step gate. Run
the fixed family/symmetry/distinct-state experiments with:

```sh
make isolate-one-step
```

The command reuses deterministic oracle outcomes under
`data/experiments/one-step-oracle-cache/`; populate only that cache with
`make collect-one-step-oracle`.

Training settings are configurable through Make variables:

```sh
make train NO_OF_BATCHES=100 BATCH_SIZE=64 LEARNING_RATE=0.0001 \
  ENTROPY_COEFFICIENT=0.01 GRADIENT_CLIP_NORM=1 TEMPERATURE=1
```

Continue Adam and model state from a saved run, or evaluate it without
updates using greedy actions:

```sh
make train RESUME_RUN=<run> NO_OF_BATCHES=100
make evaluate RESUME_RUN=<run> NO_OF_BATCHES=10
```

The live episode debugger is then available at <http://127.0.0.1:8081>. It
animates the policy input, selection, contraction, movement or rotation,
maximum legal re-expansion, and next policy input for every one of the eight
actions, followed by terminal polishing and optional deep refinement. Complete
traces are streamed over WebSockets into two independent players: the best
episode from the latest active run and the all-time best. Both provide
play/pause, phase stepping, speed control, and scrubbing; see the
[debugger primer](docs/episode-debugger.md). The record view reports container
width as `1/s`, marks all-time records, and
raises a prominent candidate banner below the published best-known n=17 width
of `4.67553009360455`. TensorBoard is available
separately at <http://127.0.0.1:6006>. Their host ports can be changed with `WEB_HOST_PORT` and
`TENSORBOARD_HOST_PORT`. Use `make shell` for a development shell, `make test` for the CUDA and Go tests, and
`make docker-down` to stop the services.

Each execution creates one run identifier. Model checkpoints go to
`data/models/<run>/`, while its best arrangement lineage is atomically updated
at `data/arrangements/<run>.json`. The cross-run record lives at
`data/best-ever.json`. Each run's latest and best complete replays live at
`data/episodes/<run>/latest.json` and `best.json`. TensorBoard event streams go to
`data/tensorboard/<run>/`. Checkpoints include the model, Adam state and step,
policy RNG state, training configuration, and best-packing metadata. Generated
data is ignored by Git.

Frontend assets are never built on the host. `docker/Dockerfile.web` builds them and embeds the result in the web
binary.

## Layout

| Path | Purpose |
|------|---------|
| `squarl/` | Main GoMLX application module and native CUDA domain types |
| `web/` | Go web server and Vite/PixiJS frontend module |
| `docker/` | Main and web container definitions |
| `docs/` | Brief project primers |
| `data/` | Ignored checkpoints, arrangements, and TensorBoard event streams |
