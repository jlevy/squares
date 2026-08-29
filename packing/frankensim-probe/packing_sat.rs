//! EXPERIMENT (added for external research; not part of FrankenSim).
//!
//! Can fs-ivl certify a square packing? Runs the separating-axis test on
//! Walter Trump's 11-unit-square packing from f64 coordinates, once with
//! outward-rounded `Interval` arithmetic and once with the exact `orient2d`
//! predicate.
//!
//! A record packing has pairs that touch exactly, so their true separation
//! is exactly zero. The experiment measures how many pairs each method can
//! actually settle.

use fs_ivl::{Interval, Sign, orient2d};

const SIDE: f64 = 3.877_083_590_022_814;
const SQUARES: [[[f64; 2]; 4]; 11] = [
    [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
    [[2.877_083_590_022_814, 0.0], [3.877_083_590_022_814, 0.0], [3.877_083_590_022_814, 1.0], [2.877_083_590_022_814, 1.0]],
    [[2.032_558_314_349_614_6, 2.877_083_590_022_814], [3.032_558_314_349_614_6, 2.877_083_590_022_814], [3.032_558_314_349_614_6, 3.877_083_590_022_814], [2.032_558_314_349_614_6, 3.877_083_590_022_814]],
    [[0.0, 2.877_083_590_022_814], [1.0, 2.877_083_590_022_814], [1.0, 3.877_083_590_022_814], [0.0, 3.877_083_590_022_814]],
    [[1.0, 2.877_083_590_022_814], [2.0, 2.877_083_590_022_814], [2.0, 3.877_083_590_022_814], [1.0, 3.877_083_590_022_814]],
    [[0.0, 1.877_083_590_022_814_2], [1.0, 1.877_083_590_022_814_2], [1.0, 2.877_083_590_022_814], [0.0, 2.877_083_590_022_814]],
    [[1.212_862_592_269_273, 0.747_950_004_101_898_5], [1.976_862_065_905_759_2, 1.393_166_870_188_931_3], [1.331_645_199_818_726_4, 2.157_166_343_825_417_6], [0.567_645_726_182_240_2, 1.511_949_477_738_384_6]],
    [[1.877_083_590_022_814_2, 0.0], [2.641_083_063_659_300_6, 0.645_216_866_087_032_8], [1.995_866_197_572_267_6, 1.409_216_339_723_519], [1.231_866_723_935_781_4, 0.763_999_473_636_486_2]],
    [[1.900_221_524_117_055, 1.483_916_719_833_883], [2.664_220_997_753_541_4, 2.129_133_585_920_915_7], [2.019_004_131_666_508_6, 2.893_133_059_557_402], [1.255_004_658_030_022_3, 2.247_916_193_470_369]],
    [[2.564_442_521_870_596, 0.735_966_715_731_984_6], [3.328_441_995_507_082_3, 1.381_183_581_819_017_2], [2.683_225_129_420_049_5, 2.145_183_055_455_503_6], [1.919_225_655_783_563_4, 1.499_966_189_368_470_8]],
    [[3.113_084_116_386_328, 1.636_188_239_849_039_5], [3.877_083_590_022_814, 2.281_405_105_936_072_3], [3.231_866_723_935_781_2, 3.045_404_579_572_558_4], [2.467_867_250_299_295, 2.400_187_713_485_525_6]],
];

type Square = [[f64; 2]; 4];

fn project(sq: &Square, ax: (Interval, Interval)) -> (Interval, Interval) {
    let mut lo = Interval::WHOLE;
    let mut hi = Interval::WHOLE;
    for (n, p) in sq.iter().enumerate() {
        let v = ax.0 * Interval::point(p[0]) + ax.1 * Interval::point(p[1]);
        if n == 0 {
            lo = v;
            hi = v;
        } else {
            lo = Interval::new(lo.lo().min(v.lo()), lo.hi().min(v.hi()));
            hi = Interval::new(hi.lo().max(v.lo()), hi.hi().max(v.hi()));
        }
    }
    (lo, hi)
}

fn edge_axes(sq: &Square) -> [(Interval, Interval); 2] {
    let mut out = [(Interval::point(0.0), Interval::point(0.0)); 2];
    for k in 0..2 {
        let (p, q) = (sq[k], sq[k + 1]);
        out[k] = (
            Interval::point(p[1]) - Interval::point(q[1]),
            Interval::point(q[0]) - Interval::point(p[0]),
        );
    }
    out
}

/// Does some axis PROVE a strictly positive gap under interval arithmetic?
fn interval_separation_proven(a: &Square, b: &Square) -> bool {
    let mut axes = Vec::new();
    axes.extend_from_slice(&edge_axes(a));
    axes.extend_from_slice(&edge_axes(b));
    for ax in axes {
        let (alo, ahi) = project(a, ax);
        let (blo, bhi) = project(b, ax);
        if (blo - ahi).lo() > 0.0 || (alo - bhi).lo() > 0.0 {
            return true;
        }
    }
    false
}

/// Exact-sign separating-line test: an edge of one square whose line has
/// the other square entirely on the far closed side.
fn exact_axis_separates(a: &Square, b: &Square) -> bool {
    for (sq, other) in [(a, b), (b, a)] {
        for k in 0..4 {
            let (p, q) = (sq[k], sq[(k + 1) % 4]);
            let other_neg = other.iter().all(|r| orient2d(p, q, *r) != Sign::Positive);
            let other_pos = other.iter().all(|r| orient2d(p, q, *r) != Sign::Negative);
            let own_neg = sq.iter().all(|r| orient2d(p, q, *r) != Sign::Positive);
            let own_pos = sq.iter().all(|r| orient2d(p, q, *r) != Sign::Negative);
            if (other_pos && own_neg) || (other_neg && own_pos) {
                return true;
            }
        }
    }
    false
}

fn main() {
    println!("fs-ivl on Trump's 11-square packing (f64 coordinates)\n");

    let mut iv_proven = 0;
    let mut iv_unproven = Vec::new();
    let mut exact_sep = 0;
    let mut exact_fail = Vec::new();
    for i in 0..11 {
        for j in (i + 1)..11 {
            if interval_separation_proven(&SQUARES[i], &SQUARES[j]) {
                iv_proven += 1;
            } else {
                iv_unproven.push((i, j));
            }
            if exact_axis_separates(&SQUARES[i], &SQUARES[j]) {
                exact_sep += 1;
            } else {
                exact_fail.push((i, j));
            }
        }
    }

    println!("outward-rounded Interval arithmetic");
    println!("  pairs PROVEN strictly separated  : {iv_proven} / 55");
    println!("  pairs it cannot settle           : {} {:?}", iv_unproven.len(), iv_unproven);
    println!();
    println!("exact orient2d (Shewchuk adaptive; exact for f64 inputs)");
    println!("  pairs with a separating edge line: {exact_sep} / 55");
    println!("  pairs without one                : {} {:?}", exact_fail.len(), exact_fail);
    println!();

    let s = Interval::point(SIDE);
    let mut outside = 0;
    for sq in &SQUARES {
        for p in sq {
            for v in [
                Interval::point(p[0]),
                Interval::point(p[1]),
                s - Interval::point(p[0]),
                s - Interval::point(p[1]),
            ] {
                if v.hi() < 0.0 {
                    outside += 1;
                }
            }
        }
    }
    println!("containment: {outside} of 176 coordinate bounds provably violated");
}
