//! Simulated annealing that minimises the enclosing square directly.
//!
//! The formulation, and why it is this one. The obvious approach — fix a
//! container side, ask whether the squares fit, and binary-search the side —
//! needs an outer loop that decides when an anneal has failed, and it starts
//! from the trivial grid, which is exactly jammed: shrinking it by any amount at
//! all is infeasible, and only a wholly different, tilted configuration helps.
//! Two versions of that loop were built and measured here; the first crawled
//! (2.875 on `n = 5`, where the answer is 2.707) and the second never left the
//! grid basin at all.
//!
//! So the container is not a variable. The smallest axis-aligned square holding
//! a configuration is computable from the configuration itself, which turns the
//! whole problem into unconstrained minimisation of
//!
//!     F(config) = required_side(config) + lambda * total_overlap(config)
//!
//! with `lambda` ramped upward through the anneal. Every move that compacts the
//! packing is rewarded immediately, there is no feasibility oracle and no shrink
//! schedule, and the overlap penalty is *linear* — so a finite `lambda` has an
//! exact constrained optimum, where a squared penalty's gradient dies as the
//! overlap closes and never quite reaches zero.
//!
//! Everything a strategy would want to vary lives in `Params`, because in this
//! campaign the hypotheses are search strategies and this struct is the surface
//! they act on.

use crate::geom::{local_overlap, required_side, total_overlap, Config};
use crate::rng::Rng;

/// A candidate is screened as valid when total overlap is below this. It is a
/// screening threshold, never a claim: `sqpack` decides validity exactly.
pub const FEASIBLE_EPS: f64 = 1e-12;

#[derive(Clone, Debug)]
pub struct Params {
    /// Annealing steps per restart.
    pub steps: u64,
    /// Temperature schedule, in length units: a move of this size is typical.
    pub t_hot: f64,
    pub t_cold: f64,
    /// Overlap weight, ramped geometrically across the anneal. It must end high
    /// enough that no reduction in side is worth any overlap.
    pub lambda0: f64,
    pub lambda1: f64,
    /// Rotation step, as a multiple of the temperature (radians per length unit).
    pub move_rotate: f64,
    /// Probability a move rotates rather than translates.
    pub p_rotate: f64,
    /// Probability a restart reseeds from the chain's best rather than
    /// scattering fresh.
    pub p_reseed: f64,
    /// Hard cap on restarts, as a backstop only. The move budget is what is
    /// meant to bind: an earlier version capped restarts at 24, which made
    /// `--budget-moves` inert and silently gave "equal budget" comparisons
    /// unequal amounts of work.
    pub max_restarts: u64,
}

impl Default for Params {
    fn default() -> Self {
        Params {
            steps: 400_000,
            t_hot: 0.25,
            t_cold: 1e-9,
            lambda0: 2.0,
            lambda1: 1e6,
            move_rotate: 2.0,
            p_rotate: 0.35,
            p_reseed: 0.5,
            max_restarts: u64::MAX,
        }
    }
}

#[derive(Clone, Debug)]
pub struct Outcome {
    pub best_side: f64,
    pub best: Config,
    pub best_overlap: f64,
    pub restarts: u64,
    pub moves: u64,
    pub accepted: u64,
}

/// Scatter `n` squares at random poses inside a box of side `s0`.
fn scatter(c: &mut Config, s0: f64, rng: &mut Rng) {
    for k in 0..c.n {
        c.x[k] = rng.f64() * s0;
        c.y[k] = rng.f64() * s0;
        c.set_angle(k, rng.f64() * std::f64::consts::FRAC_PI_2);
    }
}

/// One anneal. Returns the best valid side seen, or `f64::INFINITY` if the run
/// never reached a valid configuration.
fn anneal(
    c: &mut Config, p: &Params, rng: &mut Rng,
    best: &mut Config, best_side: &mut f64, best_overlap: &mut f64,
    moves: &mut u64, accepted: &mut u64,
) {
    let cooling = (p.t_cold / p.t_hot).powf(1.0 / p.steps.max(1) as f64);
    let ramp = (p.lambda1 / p.lambda0).powf(1.0 / p.steps.max(1) as f64);
    let mut temperature = p.t_hot;
    let mut lambda = p.lambda0;

    let mut side = required_side(c);
    let mut overlap = total_overlap(c);
    let mut energy = side + lambda * overlap;

    for _ in 0..p.steps {
        let k = rng.below(c.n);
        let (ox, oy, ot) = (c.x[k], c.y[k], c.t[k]);
        let (ocos, osin) = (c.cos[k], c.sin[k]);

        let (nx, ny, nt, ncos, nsin);
        if rng.f64() < p.p_rotate {
            nx = ox;
            ny = oy;
            nt = ot + p.move_rotate * temperature * rng.signed();
            ncos = nt.cos();
            nsin = nt.sin();
        } else {
            nx = ox + temperature * rng.signed();
            ny = oy + temperature * rng.signed();
            nt = ot;
            ncos = ocos;
            nsin = osin;
        }

        // The overlap term is incremental (this square's n-1 pairs); the side
        // term needs the whole configuration, so apply the move, score, and roll
        // back if rejected. At n=11 the side scan is 11 operations against 10
        // pair tests, so this is cheaper than tracking extremes incrementally.
        let old_local = local_overlap(c, k, ox, oy, ocos, osin);
        let new_local = local_overlap(c, k, nx, ny, ncos, nsin);
        c.x[k] = nx; c.y[k] = ny; c.t[k] = nt; c.cos[k] = ncos; c.sin[k] = nsin;
        let new_side = required_side(c);
        let new_overlap = overlap - old_local + new_local;
        let new_energy = new_side + lambda * new_overlap;
        *moves += 1;

        let delta = new_energy - energy;
        if delta <= 0.0 || rng.f64() < (-delta / (temperature + 1e-300)).exp() {
            energy = new_energy;
            side = new_side;
            overlap = new_overlap;
            *accepted += 1;
            if overlap <= FEASIBLE_EPS && side < *best_side {
                *best_side = side;
                *best_overlap = overlap;
                best.x.copy_from_slice(&c.x);
                best.y.copy_from_slice(&c.y);
                best.t.copy_from_slice(&c.t);
                best.cos.copy_from_slice(&c.cos);
                best.sin.copy_from_slice(&c.sin);
            }
        } else {
            c.x[k] = ox; c.y[k] = oy; c.t[k] = ot; c.cos[k] = ocos; c.sin[k] = osin;
        }

        temperature *= cooling;
        lambda *= ramp;
    }
    let _ = side;
}

/// One chain: repeated anneals from scattered or reseeded starts.
pub fn run_chain(n: usize, seed: u64, chain: u64, p: &Params, budget_moves: u64) -> Outcome {
    let mut rng = Rng::keyed(seed, chain);
    let (grid, s0) = Config::grid(n);

    let mut best = grid.clone();
    let mut best_side = s0;
    let mut best_overlap = 0.0;
    let (mut moves, mut accepted, mut restarts) = (0u64, 0u64, 0u64);

    let mut c = Config::new(n);
    while moves < budget_moves && restarts < p.max_restarts {
        if restarts > 0 && rng.f64() < p.p_reseed {
            c = best.clone();
        } else {
            scatter(&mut c, s0, &mut rng);
        }
        restarts += 1;
        anneal(&mut c, p, &mut rng, &mut best, &mut best_side, &mut best_overlap,
               &mut moves, &mut accepted);
    }

    Outcome { best_side, best, best_overlap, restarts, moves, accepted }
}
