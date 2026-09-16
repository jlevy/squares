//! A frozen copy of the move loop as it stood before any arm existed.
//!
//! The arms (simultaneous perturbation, wall pressure, the pair-test budget) were added
//! to `search` behind guards that must leave the control's arithmetic and random stream
//! untouched when every arm is off. Running the control against itself with the arm
//! flags spelled out at their defaults cannot test that: both runs pass through the same
//! guarded code with the same parameters, so the comparison cannot fail. This module is
//! an independent side for the comparison: the pre-arm `anneal` and `run_chain`, copied
//! from the engine as it was before the arms were added. Do not edit it to track later
//! changes to `search`; a change that alters the control's stream is what it catches.
//!
//! It shares `geom` and `rng` with the engine on purpose. The arms did not change them,
//! and sharing them keeps the comparison in one process and one libm, so a bitwise match
//! is a meaningful demand.

use crate::geom::{local_overlap_metered, required_side, total_overlap_metered, Config};
use crate::rng::Rng;
use crate::search::{Outcome, Params, FEASIBLE_EPS};

/// Scatter `n` squares at random poses inside a box of side `s0`.
fn scatter(c: &mut Config, s0: f64, rng: &mut Rng) {
    for k in 0..c.n {
        c.x[k] = rng.f64() * s0;
        c.y[k] = rng.f64() * s0;
        c.set_angle(k, rng.f64() * std::f64::consts::FRAC_PI_2);
    }
}

/// One pre-arm anneal. It reads only the fields `Params` had before the arms.
fn anneal(
    c: &mut Config,
    p: &Params,
    rng: &mut Rng,
    best: &mut Config,
    best_side: &mut f64,
    best_overlap: &mut f64,
    moves: &mut u64,
    accepted: &mut u64,
    pair_tests: &mut u64,
) {
    let cooling = (p.t_cold / p.t_hot).powf(1.0 / p.steps.max(1) as f64);
    let ramp = (p.lambda1 / p.lambda0).powf(1.0 / p.steps.max(1) as f64);
    let mut temperature = p.t_hot;
    let mut lambda = p.lambda0;

    let mut side = required_side(c);
    let mut overlap = total_overlap_metered(c, pair_tests);
    let mut energy = side + lambda * overlap;

    if overlap <= FEASIBLE_EPS && side < *best_side {
        *best_side = side;
        *best_overlap = overlap;
        best.x.copy_from_slice(&c.x);
        best.y.copy_from_slice(&c.y);
        best.t.copy_from_slice(&c.t);
        best.cos.copy_from_slice(&c.cos);
        best.sin.copy_from_slice(&c.sin);
    }

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

        let old_local = local_overlap_metered(c, k, ox, oy, ocos, osin, pair_tests);
        let new_local = local_overlap_metered(c, k, nx, ny, ncos, nsin, pair_tests);
        c.x[k] = nx;
        c.y[k] = ny;
        c.t[k] = nt;
        c.cos[k] = ncos;
        c.sin[k] = nsin;
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
            c.x[k] = ox;
            c.y[k] = oy;
            c.t[k] = ot;
            c.cos[k] = ocos;
            c.sin[k] = osin;
        }

        temperature *= cooling;
        lambda *= ramp;
    }
    let _ = side;
}

/// One pre-arm chain: the reference a control run of `search::run_chain` must match.
pub fn run_chain(n: usize, seed: u64, chain: u64, p: &Params, budget_moves: u64) -> Outcome {
    let mut rng = Rng::keyed(seed, chain);
    let (grid, s0) = Config::grid(n);

    let mut best = grid.clone();
    let mut best_side = s0;
    let mut best_overlap = 0.0;
    let (mut moves, mut accepted, mut restarts, mut pair_tests) = (0u64, 0u64, 0u64, 0u64);

    let mut c = Config::new(n);
    while moves < budget_moves && restarts < p.max_restarts {
        if restarts > 0 && rng.f64() < p.p_reseed {
            c = best.clone();
        } else {
            scatter(&mut c, s0, &mut rng);
        }
        restarts += 1;
        anneal(
            &mut c,
            p,
            &mut rng,
            &mut best,
            &mut best_side,
            &mut best_overlap,
            &mut moves,
            &mut accepted,
            &mut pair_tests,
        );
    }

    let best_overlap = total_overlap_metered(&best, &mut pair_tests);

    Outcome {
        best_side,
        best,
        best_overlap,
        restarts,
        moves,
        accepted,
        pair_tests,
    }
}

/// Whether two outcomes are the same run: every counter equal, and every reported float,
/// the best configuration's poses included, equal to the bit.
pub fn same_run(a: &Outcome, b: &Outcome) -> bool {
    let bits = |u: &[f64], v: &[f64]| {
        u.len() == v.len() && u.iter().zip(v).all(|(p, q)| p.to_bits() == q.to_bits())
    };
    a.best_side.to_bits() == b.best_side.to_bits()
        && a.best_overlap.to_bits() == b.best_overlap.to_bits()
        && a.moves == b.moves
        && a.accepted == b.accepted
        && a.restarts == b.restarts
        && a.pair_tests == b.pair_tests
        && bits(&a.best.x, &b.best.x)
        && bits(&a.best.y, &b.best.y)
        && bits(&a.best.t, &b.best.t)
}

#[cfg(test)]
mod tests {
    use super::{run_chain, same_run};
    use crate::search::{self, Params};

    fn small() -> Params {
        Params {
            steps: 2_000,
            ..Default::default()
        }
    }

    #[test]
    fn the_control_matches_the_frozen_pre_arm_loop() {
        let p = small();
        assert!(same_run(
            &search::run_chain(5, 42, 3, &p, 12_000),
            &run_chain(5, 42, 3, &p, 12_000)
        ));
    }

    #[test]
    fn an_arm_that_draws_on_the_control_path_fails_the_comparison() {
        // The smallest positive probability passes the arm's guard, so the draw happens
        // on every move and shifts the stream, while the perturbation itself never fires.
        // It is the mutation the comparison exists to catch.
        let drawing = Params {
            p_perturb: f64::MIN_POSITIVE,
            ..small()
        };
        assert!(!same_run(
            &search::run_chain(5, 42, 3, &drawing, 12_000),
            &run_chain(5, 42, 3, &small(), 12_000)
        ));
    }
}
