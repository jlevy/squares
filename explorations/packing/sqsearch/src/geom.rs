//! The geometry, and nothing else.
//!
//! A packing is `n` unit squares, square `k` having centre `(x[k], y[k])` and
//! angle `t[k]`, inside the axis-aligned container `[0, s]^2`. Validity is
//! disjoint interiors, so touching is allowed and a valid packing typically has
//! many pairs at exactly zero separation.
//!
//! Everything here is `f64` and therefore *approximate*: it screens candidates
//! and can never certify one. Certification is `sqpack`'s exact separating-axis
//! check over the packing's own algebraic number field, which is the only thing
//! that can decide the zero-gap contacts. Nothing in this crate may claim a
//! record.

/// Half-extent of a unit square along its own edge normals is exactly 1/2.
const HALF: f64 = 0.5;

/// A candidate packing. `cos`/`sin` are carried alongside `t` because caching
/// them is worth ~40% of the kernel (measured), and because a move that only
/// translates a square does not need to recompute them at all.
#[derive(Clone, Debug)]
pub struct Config {
    pub n: usize,
    pub x: Vec<f64>,
    pub y: Vec<f64>,
    pub t: Vec<f64>,
    pub cos: Vec<f64>,
    pub sin: Vec<f64>,
}

impl Config {
    pub fn new(n: usize) -> Self {
        Config {
            n,
            x: vec![0.0; n],
            y: vec![0.0; n],
            t: vec![0.0; n],
            cos: vec![1.0; n],
            sin: vec![0.0; n],
        }
    }

    #[inline(always)]
    pub fn set_angle(&mut self, k: usize, t: f64) {
        self.t[k] = t;
        self.cos[k] = t.cos();
        self.sin[k] = t.sin();
    }

    /// The `ceil(sqrt(n))` grid: the trivial packing, always valid, and the
    /// standing best for many `n`. Used as the feasible starting point.
    pub fn grid(n: usize) -> (Self, f64) {
        let m = (n as f64).sqrt().ceil() as usize;
        let mut c = Config::new(n);
        for k in 0..n {
            c.x[k] = (k % m) as f64 + 0.5;
            c.y[k] = (k / m) as f64 + 0.5;
            c.set_angle(k, 0.0);
        }
        (c, m as f64)
    }
}

/// Squared containment violation of one square in `[0, s]^2`.
#[inline(always)]
pub fn contain_penalty(x: f64, y: f64, cos: f64, sin: f64, s: f64) -> f64 {
    let e = HALF * (cos.abs() + sin.abs());
    let mut total = 0.0;
    let q = e - x;
    if q > 0.0 {
        total += q * q;
    }
    let q = x - (s - e);
    if q > 0.0 {
        total += q * q;
    }
    let q = e - y;
    if q > 0.0 {
        total += q * q;
    }
    let q = y - (s - e);
    if q > 0.0 {
        total += q * q;
    }
    total
}

/// Squared penetration depth of two unit squares, by the separating-axis test.
///
/// Four axes must be tested — both edge normals of both squares — but for two
/// *unit* squares the sum of half-extents is the same on all four:
/// `1/2 + 1/2(|cos D| + |sin D|)` with `D` the angle difference. Computing it
/// once instead of per axis is worth ~40% of the pair cost, and this crate's
/// tests check the simplification against the naive four-axis form.
#[inline(always)]
pub fn pair_penalty(xi: f64, yi: f64, ci: f64, si: f64, xj: f64, yj: f64, cj: f64, sj: f64) -> f64 {
    let dx = xi - xj;
    let dy = yi - yj;
    let h = HALF + HALF * ((ci * cj + si * sj).abs() + (si * cj - ci * sj).abs());
    let mut g = (dx * ci + dy * si).abs() - h;
    let g2 = (dy * ci - dx * si).abs() - h;
    if g2 > g {
        g = g2;
    }
    let g2 = (dx * cj + dy * sj).abs() - h;
    if g2 > g {
        g = g2;
    }
    let g2 = (dy * cj - dx * sj).abs() - h;
    if g2 > g {
        g = g2;
    }
    if g < 0.0 {
        g * g
    } else {
        0.0
    }
}

/// Penetration depth of two unit squares: 0 when disjoint, positive when they
/// overlap. Linear rather than squared, because a linear penalty has an *exact*
/// finite-lambda constrained optimum, while a squared one has vanishing gradient
/// as the overlap closes and never quite reaches zero.
#[inline(always)]
pub fn pair_depth(xi: f64, yi: f64, ci: f64, si: f64, xj: f64, yj: f64, cj: f64, sj: f64) -> f64 {
    let dx = xi - xj;
    let dy = yi - yj;
    let h = HALF + HALF * ((ci * cj + si * sj).abs() + (si * cj - ci * sj).abs());
    let mut g = (dx * ci + dy * si).abs() - h;
    let g2 = (dy * ci - dx * si).abs() - h;
    if g2 > g {
        g = g2;
    }
    let g2 = (dx * cj + dy * sj).abs() - h;
    if g2 > g {
        g = g2;
    }
    let g2 = (dy * cj - dx * sj).abs() - h;
    if g2 > g {
        g = g2;
    }
    if g < 0.0 {
        -g
    } else {
        0.0
    }
}

/// Side of the smallest axis-aligned square containing every square of `c`.
///
/// The container may be taken axis-aligned without loss of generality — the
/// squares carry all the rotation — so this is computable from the configuration
/// alone. That is what removes the container from the variables and lets the
/// search minimise the side directly instead of guessing one and testing it.
pub fn required_side(c: &Config) -> f64 {
    let (mut lox, mut hix, mut loy, mut hiy) = (f64::MAX, f64::MIN, f64::MAX, f64::MIN);
    for k in 0..c.n {
        let e = HALF * (c.cos[k].abs() + c.sin[k].abs());
        lox = lox.min(c.x[k] - e);
        hix = hix.max(c.x[k] + e);
        loy = loy.min(c.y[k] - e);
        hiy = hiy.max(c.y[k] + e);
    }
    (hix - lox).max(hiy - loy)
}

/// Total overlap depth over all pairs. Zero exactly when the packing is valid.
pub fn total_overlap(c: &Config) -> f64 {
    let mut pair_tests = 0;
    total_overlap_metered(c, &mut pair_tests)
}

/// Total overlap together with an exact count of evaluated unordered pairs.
pub fn total_overlap_metered(c: &Config, pair_tests: &mut u64) -> f64 {
    let mut total = 0.0;
    for i in 0..c.n {
        for j in (i + 1)..c.n {
            *pair_tests = pair_tests
                .checked_add(1)
                .expect("pair-test counter overflow");
            total += pair_depth(
                c.x[i], c.y[i], c.cos[i], c.sin[i], c.x[j], c.y[j], c.cos[j], c.sin[j],
            );
        }
    }
    total
}

/// Local overlap together with an exact count of evaluated unordered pairs.
#[inline]
pub fn local_overlap_metered(
    c: &Config,
    k: usize,
    x: f64,
    y: f64,
    cos: f64,
    sin: f64,
    pair_tests: &mut u64,
) -> f64 {
    let mut total = 0.0;
    for j in 0..c.n {
        if j != k {
            *pair_tests = pair_tests
                .checked_add(1)
                .expect("pair-test counter overflow");
            total += pair_depth(x, y, cos, sin, c.x[j], c.y[j], c.cos[j], c.sin[j]);
        }
    }
    total
}

/// Total penalty. Zero exactly when the packing is valid at side `s`.
pub fn penalty(c: &Config, s: f64) -> f64 {
    let mut total = 0.0;
    for i in 0..c.n {
        total += contain_penalty(c.x[i], c.y[i], c.cos[i], c.sin[i], s);
        for j in (i + 1)..c.n {
            total += pair_penalty(
                c.x[i], c.y[i], c.cos[i], c.sin[i], c.x[j], c.y[j], c.cos[j], c.sin[j],
            );
        }
    }
    total
}
