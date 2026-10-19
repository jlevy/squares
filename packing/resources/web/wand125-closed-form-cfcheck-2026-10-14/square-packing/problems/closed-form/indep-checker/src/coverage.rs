use crate::{
    parse_error,
    rat::{int, q, value, Q},
    report::Report,
    require, Result,
};
use num_traits::{One, Zero};
use serde_json::{json, Value};
use std::path::Path;
pub fn rows(v: &Value) -> Result<&Vec<Value>> {
    v["intervals"]
        .as_array()
        .ok_or_else(|| parse_error("missing intervals array"))
}
// Compare a root of the increasing quadratic to a rational without approximating it.
fn root_ge(alpha: &Q, rad: &Q, x: &Q) -> bool {
    let t = x - int(2) * alpha;
    t <= Q::zero() || rad >= &(&t * &t)
}
fn root_gt(alpha: &Q, rad: &Q, x: &Q) -> bool {
    let t = x - int(2) * alpha;
    t < Q::zero() || rad > &(&t * &t)
}
pub fn rounded_bound(n: i64, rs: &[Value]) -> Result<i64> {
    let mut k = 0;
    while (k + 1) * (k + 1) <= n {
        k += 1;
    }
    if k * k == n {
        return Ok(k * 1_000_000);
    }
    let mut best = None;
    for r in rs {
        let d0 = value(&r["d0"])?;
        let d1 = value(&r["d1"])?;
        let a = value(&r["certified_line"]["alpha"])?;
        let b = value(&r["certified_line"]["beta"])?;
        let rad = int(4) * &a * &a + int(n) + int(4) * b - int(4 * k) * &a;
        if rad < Q::zero() || !root_gt(&a, &rad, &(int(k) + d0)) {
            continue;
        }
        let cap = int(k) + d1;
        // Binary-search the integer floor of min(root,cap)*10^6 exactly.
        let mut lo = k * 1_000_000;
        let mut hi = (k + 1) * 1_000_000 + 1;
        while hi - lo > 1 {
            let m = (lo + hi) / 2;
            let x = q(m, 1_000_000);
            if x <= cap && root_ge(&a, &rad, &x) {
                lo = m;
            } else {
                hi = m;
            }
        }
        best = Some(best.map_or(lo, |v: i64| v.max(lo)));
    }
    best.ok_or_else(|| crate::refuse("closed form has no eligible interval"))
}
pub fn check(v: &Value) -> Result<Value> {
    let rs = rows(v)?;
    require(rs.len() == 34, "expected exactly 34 intervals")?;
    let mut end = Q::zero();
    for (i, r) in rs.iter().enumerate() {
        require(
            r["index"].as_u64() == Some((i + 1) as u64),
            "interval indices must be 1..34 in endpoint order",
        )?;
        let d0 = value(&r["d0"])?;
        let d1 = value(&r["d1"])?;
        require(d0 < d1, "non-positive delta interval")?;
        require(d0 == end, "interval gap, overlap, or unsorted endpoints")?;
        require(
            r["closed_right"].as_bool() == Some(true),
            "right endpoint must be closed",
        )?;
        r["open_left"]
            .as_bool()
            .ok_or_else(|| parse_error("missing open_left boolean"))?;
        require(
            value(&r["certified_line"]["alpha"])? <= q(2187, 1250),
            "alpha exceeds 1.7496",
        )?;
        value(&r["certified_line"]["beta"])?;
        end = d1;
    }
    require(end == Q::one(), "last endpoint is not 1")?;
    let mut table = vec![];
    for (n, want) in [
        (50, 7126165),
        (56, 7646996),
        (61, 8000000),
        (65, 8102316),
        (110, 10600000),
    ] {
        let got = rounded_bound(n, rs)?;
        require(got == want, format!("a({n}) disagrees with README table"))?;
        table.push(json!({"N":n,"rounded_down":format!("{}.{:06}",got/1_000_000,got%1_000_000)}));
    }
    Ok(json!({"intervals":34,"a_of_n":table}))
}
pub fn run(path: &Path, report: &mut Report) -> Result<()> {
    let v = report.read_json(path)?;
    report.details = check(&v)?;
    Ok(())
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn published() {
        let v: Value =
            serde_json::from_str(include_str!("../tests/fixtures/intervals.json")).unwrap();
        assert!(check(&v).is_ok());
    }
    #[test]
    fn gap() {
        let mut v: Value =
            serde_json::from_str(include_str!("../tests/fixtures/intervals.json")).unwrap();
        v["intervals"][1]["d0"] = json!("0");
        assert!(check(&v).is_err());
    }
}
