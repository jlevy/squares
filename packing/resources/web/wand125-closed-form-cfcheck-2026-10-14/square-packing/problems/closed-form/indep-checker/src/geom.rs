use crate::rat::{int, q, Q};
use num_traits::Zero;
pub type Point = [Q; 2];
pub type Polygon = Vec<Point>;
pub type Plane = (Point, Q);
pub fn dot(a: &Point, b: &Point) -> Q {
    &a[0] * &b[0] + &a[1] * &b[1]
}
pub fn sub(a: &Point, b: &Point) -> Point {
    [&a[0] - &b[0], &a[1] - &b[1]]
}
pub fn cross(a: &Point, b: &Point) -> Q {
    &a[0] * &b[1] - &a[1] * &b[0]
}
pub fn rect(x0: Q, x1: Q, y0: Q, y1: Q) -> Polygon {
    vec![
        [x0.clone(), y0.clone()],
        [x1.clone(), y0],
        [x1, y1.clone()],
        [x0, y1],
    ]
}
pub fn clip(p: &[Point], n: &Point, b: &Q) -> Polygon {
    let mut out = vec![];
    if p.is_empty() {
        return out;
    }
    for i in 0..p.len() {
        let a = &p[i];
        let c = &p[(i + 1) % p.len()];
        let fa = dot(n, a) - b;
        let fc = dot(n, c) - b;
        if fa <= Q::zero() {
            out.push(a.clone());
        }
        if fa.is_positive() && fc.is_negative() || fa.is_negative() && fc.is_positive() {
            let t = &fa / (&fa - &fc);
            out.push([&a[0] + &t * (&c[0] - &a[0]), &a[1] + &t * (&c[1] - &a[1])]);
        }
    }
    out.dedup();
    if out.len() > 1 && out.first() == out.last() {
        out.pop();
    }
    out
}
pub fn area(p: &[Point]) -> Q {
    if p.len() < 3 {
        return Q::zero();
    }
    (0..p.len())
        .map(|i| cross(&p[i], &p[(i + 1) % p.len()]))
        .sum::<Q>()
        / int(2)
}
pub fn planes(p: &[Point]) -> Vec<Plane> {
    (0..p.len())
        .map(|i| {
            let a = &p[i];
            let b = &p[(i + 1) % p.len()];
            let n = [&b[1] - &a[1], &a[0] - &b[0]];
            let d = dot(&n, a);
            (n, d)
        })
        .collect()
}
pub fn intersection(a: &[Point], b: &[Point]) -> Polygon {
    if b.len() < 3 {
        return vec![];
    }
    let mut out = a.to_vec();
    for (n, d) in planes(b) {
        out = clip(&out, &n, &d);
    }
    out
}
pub fn segment_width(a: &Point, b: &Point, ps: &[Plane]) -> Option<Q> {
    let mut lo = Q::zero();
    let mut hi = int(1);
    let delta = sub(b, a);
    for (n, d) in ps {
        let num = d - dot(n, a);
        let den = dot(n, &delta);
        if den.is_positive() {
            hi = hi.min(num / den);
        } else if den.is_negative() {
            lo = lo.max(num / den);
        } else if num.is_negative() {
            return None;
        }
    }
    Some(hi - lo)
}
pub fn segment_mass(a: &Point, b: &Point, m: &Q, p: &[Point]) -> Q {
    if p.len() < 3 {
        return Q::zero();
    }
    segment_width(a, b, &planes(p))
        .unwrap_or_else(Q::zero)
        .max(Q::zero())
        * m
}
pub fn hull(mut p: Polygon) -> Polygon {
    p.sort();
    p.dedup();
    if p.len() < 3 {
        return p;
    }
    let mut out: Polygon = vec![];
    for a in &p {
        while out.len() >= 2 {
            let l = out.len();
            if cross(&sub(&out[l - 1], &out[l - 2]), &sub(a, &out[l - 1])) > Q::zero() {
                break;
            }
            out.pop();
        }
        out.push(a.clone());
    }
    let lower = out.len();
    for a in p.iter().rev().skip(1) {
        while out.len() > lower {
            let l = out.len();
            if cross(&sub(&out[l - 1], &out[l - 2]), &sub(a, &out[l - 1])) > Q::zero() {
                break;
            }
            out.pop();
        }
        out.push(a.clone());
    }
    out.pop();
    out
}
pub fn normals(u: &Q) -> [Point; 4] {
    let den = int(1) + u * u;
    let c = (int(1) - u * u) / &den;
    let s = int(2) * u / den;
    [
        [c.clone(), s.clone()],
        [-s.clone(), c.clone()],
        [-c.clone(), -s.clone()],
        [s, -c],
    ]
}
pub fn vertices(u: &Q) -> [Point; 4] {
    let ns = normals(u);
    std::array::from_fn(|i| {
        [
            (&ns[i][0] + &ns[(i + 1) % 4][0]) / int(2),
            (&ns[i][1] + &ns[(i + 1) % 4][1]) / int(2),
        ]
    })
}
pub fn w_min(u0: &Q, u1: &Q) -> Q {
    if u0 <= &Q::zero() && u1 >= &Q::zero() {
        int(1)
    } else {
        [u0, u1]
            .iter()
            .map(|u| {
                let n = normals(u);
                n[0][0].abs() + n[0][1].abs()
            })
            .min()
            .unwrap()
    }
}
pub fn hmax(u0: &Q, u1: &Q) -> Q {
    let m = u0.abs().max(u1.abs());
    if m <= q(2, 5) {
        (int(1) - &m * &m + int(2) * &m) / (int(2) * (int(1) + &m * &m))
    } else {
        q(7072, 10000)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn clipping() {
        let p = rect(int(0), int(2), int(0), int(2));
        let c = clip(&p, &[int(1), int(0)], &int(1));
        assert_eq!(area(&c), int(2));
        assert_eq!(
            segment_mass(&[int(-1), int(1)], &[int(3), int(1)], &int(4), &c),
            int(1)
        );
        assert_eq!(
            segment_mass(&[int(0), int(0)], &[int(1), int(0)], &int(3), &c),
            int(3)
        );
    }
    #[test]
    fn widths() {
        assert_eq!(w_min(&q(-1, 4), &q(1, 4)), int(1));
        assert_eq!(hmax(&int(0), &q(1, 2)), q(7072, 10000));
        assert_eq!(hmax(&int(0), &q(1, 4)), q(23, 34));
    }
}
