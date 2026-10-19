# Handoff: the Low-`n` Review, the Efficiency Block, and the 2880 Rung, 22 September 2026

Written at the end of session 151 for whoever picks this up.
Branch `claude/happy-johnson-i2ridl`, cut from `origin/main` at `97efd26f`.

The important division is between **one bound that moved and is gate-certified**, **four
cells that returned measured negatives**, and **a register entry nobody has written**.
They are not the same object and should not travel together.

## Part 1: the bound that moved

**`s(11) >= 955000*sqrt(2073600042893309449)/359341754646249 = 3.826997548829543624`**,
against `T-026`’s registered $3.826447410572939744$. A movement of $+0.000550138257$.

The frozen `T-025` threshold atoms re-certify at the 2880-step net; the crossing shrink
does not rise under refinement, so halving the net gap moves the dilation-limit supremum
with no new mathematics.
Both retention routes accept the frozen bytes and agree at exactly 1 — interval
enclosure $(1, 1)$ over 5,761 directions and 23,785,079 boxes with no stalls, exact
route independently at direction 1828 — and the run’s own 1440 leg reproduces `T-026`’s
surd exactly as a control.

`RETAINABLE`, `sha256 fefcf8ac23456442f855b5bb9188fc16db3b2bf5380e0e0bd1f472ba17665219`.
The receipt is `results/agenda-041/exp-226-n11-net2880-receipt.md`.

### What is left to land it

**Nobody has written the register entry, and that was deliberate.** The certificate is
accepted and the corollary value is computed and printed by
`devtools.dilation_corollary`, but no `T-id` is claimed, `results.yaml` is untouched,
and no evidence entries exist.
A session that wants the rung registered needs to:

1. take the next id and put its row **last**. `devtools/check_results.py:186-189` builds
   the expected ids as `T-001..T-N` and compares them to the ids *in file order*, so an
   id is its row’s position and an insertion anywhere else fails.
   The rule that ids are never renumbered except on merge collision is
   `conventions.md:88-90`; the `T-032` move is commit `611804c2d`. An earlier revision
   of this handoff attributed the rule to `X-041`, which does not contain it;
2. write the claim in the shape `T-026`’s uses, as a **supremum** — the theorem supplies
   no individual certificate at that side and does not establish a strict inequality
   there, and the tool says so in its own output;
3. carry the limit record, which **is written and complete**:
   `results/agenda-041/exp-226-n11-dilation-limit-corollary-net2880.json`, 32 m 50 s to
   replay all six source conditions (1, 1', 2', 3, 4 and 5'). It binds to the
   certificate by `sha256 fefcf8ac…`, carries the sharpened-containment identity with
   its monotonicity step, the strict dilation family over its rational factor domain,
   and the density, embedding and order steps that take the family to the supremum.
   It records `endpoint_certificate: False`.

The certificate bytes are under `results/agenda-041/`, not under `cases/`. Moving them
to `cases/n11_threshold_certificate/` is the convention `T-026` follows and is part of
registering, not part of this session.

## Part 2: four measured negatives, each with its witness

None of these moved a bound, and each is worth more than an absence.

- **The $n = 17$ triples are load-bearing** (`H-235`). With `threshold_orbits` emptied
  the least point-only charge is $370792263/500000000 = 0.741585$ against $0.861183$, at
  row 5130. Row 0 alone already refutes.
- **The parent-centre restriction is load-bearing**, with an exact witness at row 6512
  charging $199827543/200000000$ against $M/17 = 0.999907492$, and no rescaling saves
  it. Two lanes derived that independently and agreed to the last digit.
  Read unrestricted through the gate’s exact route the measure’s least charge is
  $0.305414321$ at direction 0, so it is refuted at every net.
- **Re-pricing is capped.** Any re-priced measure on the artifact’s support at fixed
  $(L, A)$ has mass at least $33945829752/2000000005 = 16.972914834$, against the
  artifact’s $16.998078606$. The whole avenue is worth at most $0.0252$ of mass, about
  $+0.0034$ in the bound, and the floor had not converged.
  **The slate’s weight should move off `A2` and onto the sites side.**
- **The grid escape is the null, and total.** At $n = 12$, $20$, $21$ all fifteen runs
  and all 120 chains returned the grid exactly, spread zero, and the quench returns the
  integer again.

## Part 3: what is now known to be blocked, and by what

- **The gate cannot reach external measures at this scale.** `MAX_INTERVAL_ATOMS` is
  4,096 and the external $n = 17$ measure expands to 6,744 point atoms; retention needs
  both routes, so no measure above the cap can be retained as the gate is built.
  `AtomData.of` is the point route’s loader too, so this binds first-party colgen at
  this scale as well. The fix is chunking the boxes-by-atoms mask, not raising the cap.
- **The $n = 27$/`n = 28` candidate is refused on agreement, not on the bound.** The
  retained $n = 29$ candidate at $548/100$ certifies every `n >= 27` by Condition 2 —
  the tool prints that itself — and a $103/100$ re-bump clears its Condition 5 stall
  completely at the theorem’s own threshold.
  The gate still refuses because it encloses against the *exact minimum*, where the
  shortfall is relative and reweighting moves both ends together.
  All 272 stalls are in direction 0, below the `1e-12` resolution floor.
  Whether an escape from the agreement requirement is sound policy is a `W7` question
  for the gate’s owner; `D-435` is why it is asked in both modes.
- **`fold_ceiling_family` is one-sided.** A fold at or above $n$ proves a ceiling; a
  fold below $n$ proves nothing.
  `X-041`’s `A6` kill rests on the invalid negative branch.

## Part 4: three corrections a next agent must not re-introduce

1. **`H-228` is not refuted.** An earlier draft of `X-042` said so; the argument uses
   the interior convention and `H-228` is stated for closed unit squares.
   It stays blocked, and what the episode leaves is a specification constraint: the
   `BC-365` verifier must decide closed cores.
2. **The $n = 19$ “0.073 short” figure is the annealer’s stopping point, not the
   repository’s best.** Polishing `exp-202`’s own archived poses reaches $4.915913$;
   four times the budget reaches $4.888119$, `2.501e-03` from Wainwright.
   Where the annealer only just escapes the grid, its reported side is not a local
   optimum.
3. **The $4.888109$ Stromquist $n = 19$ value is not in this repository.** It travelled
   through this block’s briefs and nothing verifies it.

## Practical notes for the next agent

- **A fresh clone cannot run the loop.** Five preconditions, now checked by
  `devtools.check_bootstrap` and documented in `AGENTS.md`. A sixth is not in the check:
  the Rust engine is unbuilt, which blocks every upper-bound experiment —
  `cargo build --release --manifest-path sqsearch/Cargo.toml`, 19 s. A seventh is not in
  it either: `SQUARES_BROWSER_EXECUTABLE` is unset, which fails the Chromium workbench
  check; pointed at
  `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell` that check
  passes in full. Both belong in `check_bootstrap`.
- **Two container facts that look like code failures and are not.** The subprocess
  signal tests fail here in isolation as well as under load — “worker process group
  remained alive after SIGKILL”, with pid 1 being `process_api` rather than an init that
  reaps — and the release test asserting `PUBLICATION_REVISION`’s length fails on any
  complete clone of this repository, which now abbreviates to nine characters
  (`origin/main` is `97efd26f5`). The second is pre-existing and the shallow clone was
  hiding it.
- **The `1.38x` on the deep gate is the hosted runner pool, not drift.** `OR-17`’s text
  is corrected. The cheapest remaining win there is running the gate **once per tree
  rather than once per pull-request event**; two runs spent 45 minutes each on
  byte-identical `030d109a`.
- `packing-validate --edit` on this box reports well above its 240 s ceiling whenever
  lanes are running, reported and not enforced because the shape is four CPUs against a
  two-CPU reference. **No figure from this session is the one to write into
  `gate-budgets.yaml`.**
- `devtools/check_bootstrap.py` has no unit tests and nothing in CI exercises it.
  That is the accepted cost of keeping it out of every tier, and it deserves a follow-up
  bead.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
