use cfcheck::{
    family::Family,
    leaf,
    rat::{int, q},
    record::Box4,
};
use serde_json::json;
fn interior() -> Box4 {
    [
        int(3),
        q(31, 10),
        int(3),
        q(31, 10),
        q(1, 10),
        q(11, 100),
        int(0),
        q(1, 10),
    ]
}
fn empty_family() -> Family {
    Family::parse(json!({"d0":"0","d1":"1/10","UA":"9/5","F":[],"T":[],"V":[]})).unwrap()
}
#[test]
fn named_interior_tests() {
    let f = empty_family();
    for kind in [
        "CORE",
        "EDGE",
        "CORE1:P",
        "CORE1:x",
        "CORE1:y",
        "CORE1:xy",
        "CORE1:xyh",
        "B3D",
        "B3U:x",
        "B3U:y",
        "B3U:xy",
        "B3U:xyh",
        "B4U",
    ] {
        assert!(leaf::check(&f, &interior(), kind).is_ok(), "{kind}");
    }
}
#[test]
fn no_dispatch_fallback() {
    let f = empty_family();
    assert!(leaf::check(&f, &interior(), "CORE1").is_err());
    assert!(leaf::check(&f, &interior(), "EMPTY").is_err());
    assert!(leaf::check(&f, &interior(), "B3T:x").is_err());
    assert!(leaf::check(&f, &interior(), "B3T:y").is_err());
}
#[test]
fn malformed_families() {
    for row in [
        json!(["0", "0", "1", "0", "0"]),
        json!(["0", "0", "1", "0", "-1"]),
        json!(["0", "0", "0", "0", "1"]),
        json!(["0", "0", "1", "1", "1"]),
    ] {
        let f = json!({"d0":"0","d1":"1/10","UA":"9/5","F":[row],"T":[],"V":[]});
        assert!(Family::parse(f).is_err());
    }
}
#[test]
fn tangent_modes() {
    let f=Family::parse(json!({"d0":"0","d1":"1/10","UA":"9/5","F":[["9/5","0","9/5","10","100"],["0","9/5","10","9/5","100"]],"T":[],"V":[]})).unwrap();
    let mut b = interior();
    b[0] = q(17, 10);
    b[1] = q(18, 10);
    for kind in ["CORE1:Tx", "CORE1:TxHy", "B3T:x"] {
        assert!(leaf::check(&f, &b, kind).is_ok(), "{kind}");
    }
    b.swap(0, 2);
    b.swap(1, 3);
    for kind in ["CORE1:Ty", "CORE1:TyHx", "B3T:y"] {
        assert!(leaf::check(&f, &b, kind).is_ok(), "{kind}");
    }
}

#[test]
fn sum_before_minimum() {
    let f = Family::parse(json!({"d0":"0","d1":"1/10","UA":"9/5",
        "F":[["0","9/5","1","9/5","1"]],"T":[],"V":[["1","9/5","1"]]}))
    .unwrap();
    assert_eq!(leaf::dy(&f, &int(0), &int(2), &int(0), &q(1, 10)), int(1));
}

#[test]
fn crossing_midpoint_with_equal_volume() {
    let root = interior();
    let mut a = root.clone();
    let mut b = root.clone();
    a[1] = q(76, 25);
    b[0] = a[1].clone();
    assert!(!cfcheck::record::tiling(&root, &[a, b]));
}

#[test]
fn strict_empty_and_zero_angle() {
    let f = empty_family();
    let mut b = interior();
    b[0] = int(0);
    b[1] = q(1, 2);
    b[4] = q(-1, 10);
    b[5] = q(1, 10);
    assert!(leaf::check(&f, &b, "EMPTY").is_err());
    assert!(leaf::check(&f, &b, "CORE1:P").is_err());
    b[1] = q(49, 100);
    assert!(leaf::check(&f, &b, "EMPTY").is_ok());
}

#[test]
fn derived_half_plane_tests() {
    let f = empty_family();
    for kind in ["EX:CORE", "EY:CORE", "EX:B3D", "EY:B3D"] {
        assert!(leaf::check(&f, &interior(), kind).is_ok(), "{kind}");
    }
}

#[test]
fn irrational_guard_boundaries() {
    use cfcheck::symbolic::{prove, RF};
    assert!(prove(&int(-1), &int(1), |e| {
        let p = RF::u().mul(&RF::u()).sub(&RF::q(q(1, 2)));
        let v = if e.sign(&p)? < 0 { p.neg() } else { p };
        Ok(vec![v])
    })
    .is_ok());
}

#[test]
fn edge_critical_value_is_not_just_endpoints() {
    use cfcheck::symbolic::{prove_frontier, RF};
    // f(t) = 23/20 - t + t^2: both endpoints exceed 1, but f(1/2)=9/10.
    let fp = RF::q(q(23, 20));
    let fq = fp.clone();
    let gm = RF::q(q(9, 10));
    assert!(prove_frontier(&q(1, 10), &q(1, 5), |e| {
        let a = fp.sub(&gm.scale(&int(2))).add(&fq).scale(&int(2));
        let b = fq.sub(&fp).sub(&a);
        let t = b.neg().div(&a.scale(&int(2)));
        assert!(e.sign(&a)? > 0 && e.sign(&t)? > 0 && e.sign(&RF::i(1).sub(&t))? > 0);
        Ok(vec![fp
            .sub(&b.mul(&b).div(&a.scale(&int(4))))
            .sub(&RF::i(1))])
    })
    .is_err());
}

#[test]
fn cached_clipping_replays_every_guard() {
    use cfcheck::symbolic::{self as sy, Eval, RF};
    cfcheck::symbolic::clear_caches();
    let a = [RF::i(0), RF::i(0)];
    let b = [RF::i(2), RF::i(0)];
    let center = [RF::q(cfcheck::rat::q(3, 4)), RF::q(cfcheck::rat::q(1, 5))];
    let sample = cfcheck::rat::q(1, 7);
    let mut first = Eval::new(sample.clone());
    let v = sy::width(&a, &b, &center, &mut first).unwrap();
    assert!(!first.guards.is_empty());
    let mut second = Eval::new(sample.clone());
    assert_eq!(v, sy::width(&a, &b, &center, &mut second).unwrap());
    assert_eq!(first.guards, second.guards);
    let polygon = cfcheck::geom::rect(
        cfcheck::rat::int(0),
        cfcheck::rat::int(2),
        cfcheck::rat::int(0),
        cfcheck::rat::int(2),
    );
    let mut first = Eval::new(sample.clone());
    let v = sy::square_area(&polygon, &center, &mut first).unwrap();
    let mut second = Eval::new(sample);
    assert_eq!(v, sy::square_area(&polygon, &center, &mut second).unwrap());
    assert_eq!(first.guards, second.guards);
}
