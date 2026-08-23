//! `sqsearch` — tier-1 screening search for `s(n)`, the side of the smallest
//! square holding `n` non-overlapping unit squares.
//!
//! This binary SCREENS. It works in `f64` and can never certify a packing,
//! because a record packing has pairs touching at exactly zero separation and no
//! floating-point check can decide those. Its job is to find basins fast and
//! hand them on: tier 2 polishes a basin numerically, tier 3 (`sqpack`) certifies
//! exactly over the packing's own algebraic number field. Only tier 3 may say
//! "record".
//!
//! Output is JSONL on stdout, one object per chain plus a final summary, so a
//! run is appended to a campaign's `results/` and lifted into an artifact
//! without retyping any number.

mod geom;
mod rng;
mod search;

use rayon::prelude::*;
use search::Params;

fn arg<T: std::str::FromStr>(args: &[String], name: &str, default: T) -> T {
    match args.iter().position(|a| a == name) {
        Some(i) if i + 1 < args.len() => args[i + 1]
            .parse()
            .unwrap_or_else(|_| panic!("bad value for {name}: {}", args[i + 1])),
        _ => default,
    }
}

fn json_params(p: &Params) -> String {
    format!(
        "{{\"steps\":{},\"t_hot\":{},\"t_cold\":{},\"lambda0\":{},\"lambda1\":{},\
\"move_rotate\":{},\"p_rotate\":{},\"p_reseed\":{},\"max_restarts\":{}}}",
        p.steps, p.t_hot, p.t_cold, p.lambda0, p.lambda1,
        p.move_rotate, p.p_rotate, p.p_reseed, p.max_restarts
    )
}

fn json_config(c: &geom::Config) -> String {
    let f = |v: &Vec<f64>| {
        v.iter().map(|z| format!("{z:.17e}")).collect::<Vec<_>>().join(",")
    };
    format!("\"x\":[{}],\"y\":[{}],\"t\":[{}]", f(&c.x), f(&c.y), f(&c.t))
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.iter().any(|a| a == "--selftest") {
        selftest();
        return;
    }
    if args.iter().any(|a| a == "--pairdump") {
        // Emit this crate's pair verdict on deterministic near-contact pairs, so the
        // Python oracle can check the two codebases against each other. sqsearch owns
        // move-loop *energy*, sqpack owns *validity*; this is where they must agree.
        pairdump(arg(&args, "--pairs", 20000u64), arg(&args, "--seed", 0x5EEDu64));
        return;
    }

    let n: usize = arg(&args, "--n", 11);
    let seed: u64 = arg(&args, "--seed", 0x5EED);
    let chains: u64 = arg(&args, "--chains", 16);
    let budget: u64 = arg(&args, "--budget-moves", 50_000_000);
    let threads: usize = arg(&args, "--threads", 0);

    let p = Params {
        steps: arg(&args, "--steps", 400_000),
        t_hot: arg(&args, "--t-hot", 0.25),
        t_cold: arg(&args, "--t-cold", 1e-9),
        lambda0: arg(&args, "--lambda0", 2.0),
        lambda1: arg(&args, "--lambda1", 1e6),
        move_rotate: arg(&args, "--move-rotate", 2.0),
        p_rotate: arg(&args, "--p-rotate", 0.35),
        p_reseed: arg(&args, "--p-reseed", 0.5),
        max_restarts: arg(&args, "--max-restarts", u64::MAX),
    };

    if threads > 0 {
        rayon::ThreadPoolBuilder::new().num_threads(threads).build_global().unwrap();
    }

    let started = std::time::Instant::now();
    let outcomes: Vec<_> = (0..chains)
        .into_par_iter()
        .map(|chain| (chain, search::run_chain(n, seed, chain, &p, budget)))
        .collect();
    let elapsed = started.elapsed().as_secs_f64();

    let mut best_side = f64::INFINITY;
    let mut best_chain = 0u64;
    let mut best_config = &outcomes[0].1.best;
    let mut best_overlap = f64::NAN;
    let (mut moves, mut anneals) = (0u64, 0u64);
    for (chain, o) in &outcomes {
        moves += o.moves;
        anneals += o.restarts;
        println!(
            "{{\"kind\":\"chain\",\"n\":{},\"seed\":{},\"chain\":{},\"best_side\":{:.17e},\
             \"overlap\":{:.3e},\"moves\":{},\"restarts\":{},\"accepted\":{},{}}}",
            n, seed, chain, o.best_side, o.best_overlap, o.moves, o.restarts, o.accepted,
            json_config(&o.best)
        );
        if o.best_side < best_side {
            best_side = o.best_side;
            best_chain = *chain;
            best_config = &o.best;
            best_overlap = o.best_overlap;
        }
    }

    println!(
        "{{\"kind\":\"summary\",\"n\":{n},\"seed\":{seed},\"chains\":{chains},\
\"best_side\":{best_side:.17e},\"best_chain\":{best_chain},\"moves\":{moves},\
\"anneals\":{anneals},\"seconds\":{elapsed:.3},\"moves_per_sec\":{rate:.0},\
\"best_overlap\":{overlap:.3e},{config},\"params\":{params}}}",
        rate = moves as f64 / elapsed,
        overlap = best_overlap,
        config = json_config(best_config),
        params = json_params(&p),
    );
}

/// Deterministic near-contact pairs and this crate's verdict on each, as JSONL.
///
/// Pairs are generated close to touching on purpose: that is the only regime where a
/// disagreement between the search energy and the validity predicate could hide.
fn pairdump(count: u64, seed: u64) {
    let mut r = rng::Rng::keyed(seed, 0);
    for _ in 0..count {
        let ti = r.f64() * std::f64::consts::TAU;
        let tj = r.f64() * std::f64::consts::TAU;
        let (ci, si, cj, sj) = (ti.cos(), ti.sin(), tj.cos(), tj.sin());
        // Place j near contact along a random direction: the sum of half-extents plus
        // a small signed jitter, so roughly half the pairs are just-overlapping.
        let dir = r.f64() * std::f64::consts::TAU;
        let h = 0.5 + 0.5 * ((ci * cj + si * sj).abs() + (si * cj - ci * sj).abs());
        let d = h * (1.0 + 0.02 * r.signed());
        let (xi, yi) = (0.0, 0.0);
        let (xj, yj) = (d * dir.cos(), d * dir.sin());
        let depth = geom::pair_depth(xi, yi, ci, si, xj, yj, cj, sj);
        println!(
            "{{\"xi\":{xi:.17e},\"yi\":{yi:.17e},\"ti\":{ti:.17e},\
\"xj\":{xj:.17e},\"yj\":{yj:.17e},\"tj\":{tj:.17e},\"depth\":{depth:.17e}}}"
        );
    }
}

/// Checks that must hold before any number this binary prints means anything.
fn selftest() {
    let mut failures = 0;

    // 1. The simplified four-axis form agrees with the naive one on random pairs.
    let mut r = rng::Rng::keyed(1, 1);
    let mut worst: f64 = 0.0;
    for _ in 0..200_000 {
        let (xi, yi, ti) = (r.signed() * 3.0, r.signed() * 3.0, r.f64() * 6.283);
        let (xj, yj, tj) = (r.signed() * 3.0, r.signed() * 3.0, r.f64() * 6.283);
        let (ci, si, cj, sj) = (ti.cos(), ti.sin(), tj.cos(), tj.sin());
        let fast = geom::pair_penalty(xi, yi, ci, si, xj, yj, cj, sj);
        let naive = naive_pair_penalty(xi, yi, ci, si, xj, yj, cj, sj);
        worst = worst.max((fast - naive).abs());
    }
    report("simplified SAT == naive SAT", worst < 1e-12, format!("max diff {worst:.3e}"), &mut failures);

    // 2. The n=4 grid is valid at s=2 and invalid just below it.
    let (c, s) = geom::Config::grid(4);
    report("grid(4) valid at s=2", geom::penalty(&c, s) == 0.0, format!("s={s}"), &mut failures);
    report("grid(4) invalid at s=2-1e-9", geom::penalty(&c, s - 1e-9) > 0.0, String::new(), &mut failures);

    // 3. A 45-degree square fits a container of side sqrt(2) and not less.
    let mut c = geom::Config::new(1);
    let d = std::f64::consts::SQRT_2;
    c.x[0] = d / 2.0;
    c.y[0] = d / 2.0;
    c.set_angle(0, std::f64::consts::FRAC_PI_4);
    report("tilted unit square fits sqrt(2)", geom::penalty(&c, d) < 1e-30, format!("{:.3e}", geom::penalty(&c, d)), &mut failures);
    report("and not sqrt(2)-1e-9", geom::penalty(&c, d - 1e-9) > 0.0, String::new(), &mut failures);

    // 4. Overlapping squares are detected with the right depth.
    let mut c = geom::Config::new(2);
    c.x[0] = 1.0; c.y[0] = 1.0; c.set_angle(0, 0.0);
    c.x[1] = 1.5; c.y[1] = 1.0; c.set_angle(1, 0.0);
    let expected = 0.25; // penetration 0.5, squared
    report("overlap depth 0.5 -> penalty 0.25", (geom::penalty(&c, 10.0) - expected).abs() < 1e-15,
           format!("{:.6}", geom::penalty(&c, 10.0)), &mut failures);

    // 5. Chains are reproducible from (seed, chain) alone.
    let p = Params { steps: 60_000, ..Default::default() };
    let a = search::run_chain(5, 42, 3, &p, 400_000);
    let b = search::run_chain(5, 42, 3, &p, 400_000);
    report("chain reproducible from (seed, chain)", a.best_side == b.best_side,
           format!("{:.17e}", a.best_side), &mut failures);

    // 6. Different chains of one seed explore differently.
    let d2 = search::run_chain(5, 42, 4, &p, 400_000);
    report("distinct chains explore differently", a.best_side != d2.best_side,
           format!("{:.9} vs {:.9}", a.best_side, d2.best_side), &mut failures);

    // 7. POSITIVE CONTROL. s(5) and s(10) are both proved to be m + 1/sqrt(2),
    //    attained by a non-trivial tilted family rather than by the grid. A
    //    searcher that cannot recover a case whose answer is known has not
    //    earned an opinion about one that is open, so this gates every run.
    let p = Params { steps: 300_000, ..Default::default() };
    let target5 = 2.0 + 1.0 / std::f64::consts::SQRT_2;
    let o5 = search::run_chain(5, 0x5EED, 0, &p, 20_000_000);
    report("positive control: recovers s(5)", o5.best_side - target5 < 1e-3,
           format!("{:.9} vs {:.9}, gap {:+.2e}", o5.best_side, target5, o5.best_side - target5),
           &mut failures);
    report("and never beats it", o5.best_side >= target5 - 1e-12,
           String::new(), &mut failures);

    // s(10) is the campaign's other positive control, but one chain needs a
    // real budget to land it reliably. It is measured as a recorded baseline
    // round rather than here, so this pre-flight check stays fast.

    // 8. Reported configurations are actually valid at the reported side.
    report("reported packing is overlap-free", o5.best_overlap <= search::FEASIBLE_EPS,
           format!("overlap {:.2e}", o5.best_overlap), &mut failures);
    report("reported overlap is recomputed, not accumulated",
           (geom::total_overlap(&o5.best) - o5.best_overlap).abs() < 1e-18,
           format!("{:.2e} vs stored {:.2e}", geom::total_overlap(&o5.best), o5.best_overlap),
           &mut failures);
    report("reported packing fits its reported side",
           geom::required_side(&o5.best) <= o5.best_side + 1e-12,
           format!("{:.12} <= {:.12}", geom::required_side(&o5.best), o5.best_side), &mut failures);

    println!("{}", if failures == 0 { "SELFTEST PASSED" } else { "SELFTEST FAILED" });
    if failures > 0 {
        std::process::exit(1);
    }
}

/// The four-axis separating-axis test written out longhand, used only by the
/// selftest to check the simplification the fast path relies on.
fn naive_pair_penalty(xi: f64, yi: f64, ci: f64, si: f64, xj: f64, yj: f64, cj: f64, sj: f64) -> f64 {
    let (dx, dy) = (xi - xj, yi - yj);
    let axes = [(ci, si), (-si, ci), (cj, sj), (-sj, cj)];
    let mut g = f64::NEG_INFINITY;
    for (ax, ay) in axes {
        let hi = 0.5 * ((ax * ci + ay * si).abs() + (-ax * si + ay * ci).abs());
        let hj = 0.5 * ((ax * cj + ay * sj).abs() + (-ax * sj + ay * cj).abs());
        g = g.max((dx * ax + dy * ay).abs() - hi - hj);
    }
    if g < 0.0 { g * g } else { 0.0 }
}

fn report(name: &str, ok: bool, detail: String, failures: &mut u32) {
    println!("  {} {name}{}", if ok { "ok  " } else { "FAIL" },
             if detail.is_empty() { String::new() } else { format!("  ({detail})") });
    if !ok {
        *failures += 1;
    }
}
