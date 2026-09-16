# Packing model

The GoMLX model consumes 22 nodes in fixed order: 17 squares, left/right/bottom/top walls, then one global node.
Its inputs are:

| Tensor | Shape |
|---|---|
| Node features | `[batch, 22, node_features]` |
| Edge features | `[batch, 22, 22, edge_features]` |
| Candidate features | `[batch, candidates, action_features]` |
| Candidate group mask | `[batch, candidates, 17]` |
| Candidate seed | `[batch, candidates]` |

The base node schema contains a square/wall/global one-hot type, `(x, y)`, `cos(4θ)`, `sin(4θ)`, four wall
clearances, common side length, contact count, and minimum contact gap. The base edge schema contains `(Δx, Δy)`,
relative-angle cosine and sine, four separating-axis gaps, and contact status.

Candidate features begin with a five-value one-hot action type in CUDA order—move square, rotate square, move group,
rotate group, no-op—followed by `Δx`, `Δy`, `Δθ`, and contraction factor. CUDA supplies 205 candidates: no-op plus
12 actions per square. All three feature tensors may append extra values when their configured widths include them.

The packing encoder projects nodes to width 128 and applies four transformer blocks. Each block has four 32-wide
attention heads, a 512-wide feed-forward layer, residual connections, and layer normalization. A per-block edge MLP
produces one additive attention bias per head and ordered node pair.

Each candidate combines its encoded seed, the mean embedding selected by its group mask, the global embedding, a
learned action-type projection, and a continuous-action projection. Its shared
MLP is `256 → 128`, followed by a policy/value logit and an auxiliary
“beats no-op” logit. The encoder and candidate MLP are shared across every square and
candidate. The no-op's empty group mask also zeros its placeholder seed
embedding, so its score cannot depend on which physical square has index zero.
A separate `128 → 1` state-value head is present but is not yet used as a
baseline.

During training, the 205 logits are divided by a configurable temperature and sampled categorically. Every candidate
is real and valid, so this fixed candidate set needs no padding mask. Frozen evaluation uses `argmax`.

For each of the eight steps, collection stores the complete node, edge, candidate, group-mask, and seed tensors plus
the selected index, episode identifier, and step number. CUDA applies the sampled action but is never differentiated.
Initial and final copies are polished, and the episode reward is:

```text
log(final_polished_side / initial_polished_side)
```

Before a long training run, `make validate-rl` runs the gated CUDA validation
suite: a synthetic bandit, real packing reward/gradient sign checks, and
supervised plus REINFORCE one-step oracle learning. Its JSON report is written
to `data/experiments/rl-validation.json`. The command returns non-zero while
any gate fails; see [rl-validation.md](rl-validation.md) for the latest
recorded outcome.

The follow-up [one-step diagnosis](one-step-diagnosis.md) separates
memorisation, held-out generalisation, reward objectives, and action-family
calibration. Its deterministic CUDA harness is available as
`make diagnose-one-step`.

The stricter [one-step isolation gate](one-step-isolation.md) evaluates
within-family ranking, affine cross-family calibration, square and container
symmetries, and scaling to 8,192 distinct geometries across three objectives
and three model seeds. Use `make isolate-one-step`; the oracle cache can be
prepared separately with `make collect-one-step-oracle`. Multi-step RL remains
paused until this supervised gate beats no-op on untouched states.

The [top-K and candidate-afterstate gate](one-step-planning.md) tests exact
shortlist reranking and a graph encoder that sees physically applied candidate
geometry. Use `make plan-one-step`; its generated afterstate cache can be
prepared with `make collect-one-step-afterstates`. This experiment also leaves
REINFORCE and multi-step RL paused.

The [monotone shortlist planner](monotone-planner.md) turns that model into a
proposal ranker while keeping exact CUDA polishing as the decision-maker.
`make plan-monotone` compares learned and random shortlists, runs monotone
greedy and budget-matched beam planners, then trains a top-tail retrieval
objective on disjoint intermediate states. It does not run REINFORCE.

Training replays all stored states through the model. GoMLX gathers each selected log-probability inside the new
computation graph, sums the eight values per episode, and applies batch-normalised REINFORCE:

```text
advantage = stopGradient((reward - mean(reward)) / (stddev(reward) + epsilon))
loss = -mean(advantage * episode_log_probability) - entropy_coefficient * mean_entropy
```

Adam performs one globally clipped update per batch. A separate gradient preflight rejects non-finite rewards, loss,
or gradients before optimiser state can change. Versions divisible by 32 are checkpointed, as is the last version.
Checkpoints include model variables, Adam moments and step, policy RNG state, configuration, and serialized best
packing metadata.
