//! Window w₀ families. Use a separate test binary because w₀ is process-wide.
use rug::Rational as Q;
use seam4d_core::{load_family_text, w0};

const V1: &str = r#"[["0","1","1"]]"#;

fn fam(extra: &str, vkey: &str) -> String {
    format!(r#"{{"d0":"0","d1":"1/10","UA":"14/5","F":[],"T":[],"{vkey}":{V1}{extra}}}"#)
}

#[test]
fn w0_three_family() {
    // Reject W0 alone, VW alone, V together with VW, explicit W0 = 2, and noninteger W0.
    assert!(load_family_text(&fam(r#","W0":"3""#, "V")).is_err());
    assert!(load_family_text(&fam("", "VW")).is_err());
    assert!(load_family_text(&format!(r#"{{"d0":"0","d1":"1/10","UA":"14/5","F":[],"T":[],"V":[],"VW":{V1},"W0":"3"}}"#)).is_err());
    assert!(load_family_text(&fam(r#","W0":"2""#, "VW")).is_err());
    assert!(load_family_text(&fam(r#","W0":"7/2""#, "VW")).is_err());
    assert_eq!(w0(), 2, "rejected families must not set w0");
    let f = load_family_text(&fam(r#","W0":"3""#, "VW")).expect("W0 = 3 family");
    assert_eq!(w0(), 3);
    // V segment [0, w₀ + δ] × {1}, density 1, δ ∈ [0, 1/10]; axis-aligned (u ≈ 0) square centered at x ∈ [3.39, 3.41], y = 1.
    // The right endpoint 3 + δ ≥ 3 exceeds the square's left edge x − 1/2 ≤ 2.91, giving positive mass; w₀ = 2 gives endpoint ≤ 2.1 and zero mass.
    let b = f.bound_fast(Q::from((339, 100)), Q::from((341, 100)), Q::from((99, 100)), Q::from((101, 100)),
                         Q::from(0), Q::from((1, 1000)), Q::from(0), Q::from((1, 10)));
    let b = b.expect("box has admissible poses");
    assert!(b > 0, "V endpoint must be w0 + delta = 3 + delta, got bound {b}");
    assert!(b <= Q::from((11, 100)), "V mass bounded by overlap length, got {b}");
    // Reject a family with a different w₀ in the same process (the default format uses w₀ = 2).
    let old = r#"{"d0":"0","d1":"1/10","UA":"9/5","F":[],"T":[],"V":[]}"#;
    assert!(load_family_text(old).is_err());
}
