use crate::{exact::*, geom::*, pyjson, pyrandom::Random, stream::NodeStream, sweep::*, verify::*};
use crate::{json, value::Value};
use rug::Integer;
use std::collections::BTreeMap;
use std::{io::Cursor, path::PathBuf};
fn p(x: i32, y: i32) -> Point {
    (Q::from(x), Q::from(y))
}
fn rect(x: i32, y: i32, w: i32, h: i32) -> Poly {
    vec![p(x, y), p(x + w, y), p(x + w, y + h), p(x, y + h)]
}
fn ratio(n: i32, d: i32) -> Ratio {
    (
        crate::int::Int::from(i128::from(n)),
        crate::int::Int::from(i128::from(d)),
    )
}
fn section(a: i32, b: i32) -> Section {
    (ratio(a, 1), ratio(b, 1))
}
fn data(name: &str) -> PathBuf {
    let crate_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let local = crate_dir.join("tests/data").join(name);
    // Inside jlevy/squares the stalled certificate is not duplicated: the identical
    // files live in the campaign record, which is used when no local copy exists.
    if name == "stall-w7-bins8" && !local.exists() {
        return crate_dir.join(
            "../campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/fixture-w7-bins8",
        );
    }
    local
}
fn read(name: &str) -> Value {
    crate::value::from_slice(&std::fs::read(data(name)).unwrap()).unwrap()
}
#[test]
fn fraction_parsing() {
    for (s, expected) in [
        ("1.5", Q::from((3, 2))),
        ("-2e-3", Q::from((-1, 500))),
        ("1_000.25", Q::from((4001, 4))),
        (" +1 / 2 ", Q::from((1, 2))),
        (".125", Q::from((1, 8))),
        ("2.", Q::from(2)),
        ("12e+3", Q::from(12000)),
        ("-0", Q::new()),
        ("-00012 / 00008", Q::from((-3, 2))),
        ("\u{2003}+12\t/\n8\u{2003}", Q::from((3, 2))),
        (
            "170141183460469231731687303715884105728/2",
            Q::from(Integer::from(1) << 126),
        ),
    ] {
        assert_eq!(fraction_str(s).unwrap(), expected, "{s}");
    }
    for s in [
        "1/0", "1/-2", "1/+2", "1/-0", "- 1/2", "1__2", "_2", "1._2", "1.2.3", "1e", "NaN", "",
        "1 / 2/3",
    ] {
        assert!(fraction_str(s).is_err(), "{s}");
    }
    assert_eq!(
        q(&json!(0.1)).unwrap(),
        Q::from((
            Integer::from(3_602_879_701_896_397_i64),
            Integer::from(36_028_797_018_963_968_i64)
        ))
    );
    assert_eq!(q(&json!(true)).unwrap(), 1);
    assert_eq!(
        repr_point(&(Q::from((1, 2)), Q::from((3, 4)))),
        "(Fraction(1, 2), Fraction(3, 4))"
    );
    assert!(point(&json!([1])).is_err());
    assert!(poly(&json!([null])).is_err());
}
#[test]
fn geometry_helpers() {
    let square = rect(0, 0, 2, 2);
    assert_eq!(cross(&p(0, 0), &p(1, 0), &p(0, 1)), 1);
    assert_eq!(area2(&square), 8);
    assert_eq!(
        hull(&[p(1, 0), p(0, 0), p(2, 0), p(0, 0)]),
        vec![p(0, 0), p(2, 0)]
    );
    assert!(hull(&[]).is_empty());
    assert_eq!(area2(&[p(0, 0)]), 0);
    assert!(inside(&square, &p(1, 1)).unwrap());
    assert!(inside(&square, &p(0, 2)).unwrap());
    assert!(!inside(&square, &p(3, 1)).unwrap());
    assert!(planes_of(&[p(0, 0)]).is_err());
    assert_eq!(planes_of(&square).unwrap().len(), 4);
    let clipped = clip_closed(&square, &Q::from(1), &Q::new(), &Q::from(1));
    assert!(same_set(&clipped, &rect(0, 0, 1, 2)));
    assert_eq!(
        hull(&clip_closed(&square, &Q::from(1), &Q::new(), &Q::new())),
        vec![p(0, 0), p(0, 2)]
    );
    assert!(clip_closed(&[], &Q::new(), &Q::new(), &Q::new()).is_empty());
    assert!(same_set(
        &intersect_convex(&square, &rect(1, 1, 2, 2)).unwrap(),
        &rect(1, 1, 1, 1)
    ));
    assert_eq!(trig(&Q::new()), (Q::from(1), Q::new()));
    assert_eq!(trig(&Q::from(1)), (Q::new(), Q::from(1)));
    assert_eq!(trig(&Q::from((1, 2))), (Q::from((3, 5)), Q::from((4, 5))));
    assert_eq!(
        wall_box(&Q::new(), &Q::from(1), &Q::from(3))[0],
        (Q::from((1, 2)), Q::from((1, 2)))
    );
    assert!(quad_min_positive(
        &Q::from(1),
        &Q::new(),
        &Q::from(1),
        &Q::new(),
        &Q::from(1)
    ));
    assert!(!quad_min_positive(
        &Q::from((1, 4)),
        &Q::from(-1),
        &Q::from(1),
        &Q::new(),
        &Q::from(1)
    ));
    assert!(!quad_min_positive(
        &Q::new(),
        &Q::from(1),
        &Q::new(),
        &Q::new(),
        &Q::from(1)
    ));
    let small = poly(&json!([
        ["-1/10", "-1/10"],
        ["1/10", "-1/10"],
        ["1/10", "1/10"],
        ["-1/10", "1/10"]
    ]))
    .unwrap();
    assert!(core_strict(&small, &Q::new(), &Q::from(1)));
    assert!(!core_strict(
        &[(Q::from((1, 2)), Q::new())],
        &Q::new(),
        &Q::from(1)
    ));
    assert!(core_strict(&[], &Q::new(), &Q::from(1)));
    let cell = poly(&json!([
        ["9/10", "9/10"],
        ["11/10", "9/10"],
        ["11/10", "11/10"],
        ["9/10", "11/10"]
    ]))
    .unwrap();
    assert!(owned(&cell, &p(1, 1), &Q::from(3), &Q::new(), &Q::from(1), 0).unwrap());
    assert!(!owned(&cell, &p(0, 0), &Q::from(3), &Q::new(), &Q::from(1), 0).unwrap());
    assert!(
        owned(
            &rect(-2, -2, 1, 1),
            &p(0, 0),
            &Q::from(3),
            &Q::new(),
            &Q::from(1),
            0
        )
        .unwrap()
    );
    assert!(same_set(
        &minkowski_diff(&rect(0, 0, 1, 1), &rect(0, 0, 1, 1)),
        &rect(-1, -1, 2, 2)
    ));
}
#[test]
fn integer_helpers() {
    let hp = homogeneous(&(Q::from((1, 2)), Q::from((-2, 3))));
    assert_eq!(hp, (3.into(), (-4).into(), 6.into()));
    assert_eq!(normalised((-4).into(), (-6).into()).unwrap(), ratio(2, 3));
    assert!(normalised(1.into(), 0.into()).is_err());
    assert!(ratio_lt(&ratio(-1, 3), &ratio(0, 1)));
    assert_eq!(
        ratio_extremes(&[ratio(2, 3), ratio(-1, 3), ratio(1, 2)]).unwrap(),
        (ratio(-1, 3), ratio(2, 3))
    );
    assert!(ratio_extremes(&[]).is_err());
    for (a, b, expected) in [
        (ratio(0, 1), ratio(1, 1), ratio(1, 2)),
        (ratio(-2, 1), ratio(2, 1), ratio(-1, 1)),
        (ratio(-1, 3), ratio(-1, 4), ratio(-2, 7)),
        (ratio(1, 3), ratio(1, 2), ratio(2, 5)),
        (ratio(5, 2), ratio(8, 3), ratio(13, 5)),
    ] {
        let r = between(&a, &b).unwrap();
        assert!(ratio_lt(&a, &r) && ratio_lt(&r, &b));
        assert_eq!(r, expected);
    }
    assert!(between(&ratio(0, 1), &ratio(0, 1)).is_err());
    let hs: Vec<_> = rect(0, 0, 2, 2).iter().map(homogeneous).collect();
    assert_eq!(
        directions(&hs).unwrap(),
        vec![ratio(0, -1), ratio(1, 0), ratio(0, 1), ratio(-1, 0)]
    );
    assert_eq!(support(&hs, &1.into(), &1.into(), true), ratio(4, 1));
    assert_eq!(support(&hs, &1.into(), &1.into(), false), ratio(0, 1));
    assert_eq!(support(&[], &1.into(), &1.into(), true), ratio(0, 0));
}
#[test]
fn coverage_intervals() {
    assert!(!section_covered(&section(1, 1), vec![]).unwrap());
    assert!(section_covered(&section(1, 1), vec![section(0, 1)]).unwrap());
    assert!(!section_covered(&section(1, 1), vec![section(-1, 0), section(2, 3)]).unwrap());
    assert!(section_covered(&section(0, 4), vec![section(2, 4), section(0, 2)]).unwrap());
    assert!(!section_covered(&section(0, 4), vec![section(0, 1), section(2, 4)]).unwrap());
    assert!(!well_formed(&(ratio(0, 0), ratio(1, 1))));
    assert!(!well_formed(&section(2, 1)));
    assert!(section_covered(&section(0, 1), vec![section(2, 1)]).is_err());
    assert_eq!(
        widen(Some(section(1, 2)), ratio(0, 1), ratio(3, 1)),
        section(0, 3)
    );
    assert_eq!(widen(None, ratio(1, 1), ratio(2, 1)), section(1, 2));
    let huge = crate::int::Int::from(Integer::from(1) << 200);
    let a = (huge.clone(), 1.into());
    let b = (huge.clone() + 1, 1.into());
    let c = (huge + 2, 1.into());
    assert!(section_covered(&(a.clone(), c.clone()), vec![(b.clone(), c), (a, b)]).unwrap());
}
#[test]
fn degenerate_domains() {
    let origin = vec![p(0, 0)];
    assert!(degenerate_covered(&origin, std::slice::from_ref(&origin)).unwrap());
    assert!(!degenerate_covered(&origin, &[]).unwrap());
    assert!(!degenerate_covered(&origin, &[vec![p(1, 0)]]).unwrap());
    assert!(degenerate_covered(&origin, &[rect(-1, -1, 2, 2)]).unwrap());
    let segment = vec![p(0, 0), p(4, 0)];
    assert!(
        degenerate_covered(&segment, &[vec![p(0, 0), p(2, 0)], vec![p(2, 0), p(4, 0)]]).unwrap()
    );
    assert!(!degenerate_covered(&segment, &[vec![p(0, 0)], vec![p(2, 0)], vec![p(4, 0)]]).unwrap());
    assert!(!degenerate_covered(&segment, &[rect(0, 0, 1, 1), rect(2, 0, 2, 1)]).unwrap());
    assert!(degenerate_covered(&[], &[]).is_err());
    assert!(closed_planes(&[]).is_err());
    for region in [&origin, &segment, &rect(0, 0, 2, 2)] {
        for point in region {
            assert!(
                closed_planes(region)
                    .unwrap()
                    .iter()
                    .all(|(a, b, c)| dot(a, b, point) <= *c)
            );
        }
    }
}
#[test]
fn edges_and_events() {
    let a = rect(0, 0, 2, 2);
    let triangle = vec![p(0, 1), p(2, -1), p(2, 3)];
    let polys: Vec<Vec<HPoint>> = [a, triangle]
        .iter()
        .map(|p| p.iter().map(homogeneous).collect())
        .collect();
    let (edges, verts) = compile_edges(&polys).unwrap();
    assert_eq!(edges.len(), 4);
    assert_eq!(verts.len(), 2);
    assert!(edges.iter().all(|e| e.b > 0));
    let events = sweep_events(&polys, &edges, &ratio(0, 1), &ratio(2, 1)).unwrap();
    assert_eq!(events, vec![ratio(0, 1), ratio(1, 1), ratio(2, 1)]);
    assert_eq!(
        covered_by_sweep(&rect(0, 0, 2, 2), &[]).unwrap(),
        (false, Some(Q::new()))
    );
    assert!(
        covered_by_sweep(&rect(0, 0, 2, 2), &[rect(0, 0, 1, 2), rect(1, 0, 1, 2)])
            .unwrap()
            .0
    );
}
fn random_polygon(rng: &mut Random) -> Poly {
    let pts: Poly = (0..8)
        .map(|_| {
            let x = rng.word().cast_signed() % 9;
            let y = rng.word().cast_signed() % 9;
            let d = (rng.word() % 3 + 1).cast_signed();
            (Q::from((x, d)), Q::from((y, d)))
        })
        .collect();
    hull(&pts)
}
/// The hidden lens of the 2026-10-03 review's `hidden-lens` mutation, on a small domain:
/// left and right blocks, a lower block with roof y = 1, and an upper piece whose floor is
/// the V through (1, 1 + 2e), (3/2, 3/4 + 2e), (2, 1 + 2e). With e = 0 the pieces cover the
/// domain exactly (touching along the roof); with e > 0 a sliver between x = 1 and the
/// crossing of the V with the roof is uncovered, though both events have covered sections.
fn lens_pieces(e: &Q) -> Vec<Poly> {
    let one = Q::from(1);
    let floor = |y: Q| y + Q::from(2) * e;
    vec![
        rect(0, 0, 1, 2),
        rect(2, 0, 1, 2),
        rect(1, 0, 1, 1),
        vec![
            (one.clone(), floor(one.clone())),
            (Q::from((3, 2)), floor(Q::from((3, 4)))),
            (Q::from(2), floor(one.clone())),
            p(2, 2),
            p(1, 2),
        ],
    ]
}
#[test]
fn hidden_lens_zero_gap_passes_positive_gap_fails() {
    let domain = rect(0, 0, 3, 2);
    let zero = Q::new();
    assert!(covered_by_sweep(&domain, &lens_pieces(&zero)).unwrap().0);
    assert!(covered_by_area(&domain, &lens_pieces(&zero)).unwrap().0);
    let tiny = Q::from((Integer::from(1), Integer::from(1) << 40));
    for e in [tiny, Q::from((1, 1000))] {
        let (covered, at) = covered_by_sweep(&domain, &lens_pieces(&e)).unwrap();
        assert!(!covered, "gap {e} reported covered");
        let x = at.expect("an uncovered abscissa");
        // The uncovered abscissa lies in the sliver, strictly right of the event x = 1.
        assert!(x > 1 && x < Q::from((3, 2)), "uncovered at {x}");
        assert!(!covered_by_area(&domain, &lens_pieces(&e)).unwrap().0);
    }
}
#[test]
fn sweep_matches_area_random_rationals() {
    let mut rng = Random::new(&7_654_321.into());
    for iteration in 0..150 {
        let domain = random_polygon(&mut rng);
        if domain.len() < 3 {
            continue;
        }
        let mut regions: Vec<_> = (0..4).map(|_| random_polygon(&mut rng)).collect();
        if iteration % 3 == 0 {
            let cut = Q::from((rng.word() % 5).cast_signed() - 2);
            regions = vec![
                hull(&clip_closed(&domain, &Q::from(1), &Q::new(), &cut)),
                hull(&clip_closed(&domain, &Q::from(-1), &Q::new(), &-cut)),
            ];
        }
        let sweep = covered_by_sweep(&domain, &regions).unwrap().0;
        let area = covered_by_area(&domain, &regions).unwrap().0;
        assert_eq!(sweep, area, "iteration {iteration}");
    }
}
#[test]
fn facets_match_vertex_difference_hull() {
    let mut rng = Random::new(&324.into());
    for _ in 0..100 {
        let a = random_polygon(&mut rng);
        let b = random_polygon(&mut rng);
        if a.len() < 3 || b.len() < 3 {
            continue;
        }
        let expected = minkowski_diff(&a, &b);
        let eh: Vec<_> = expected.iter().map(homogeneous).collect();
        let facets = difference_facets(
            &a.iter().map(homogeneous).collect::<Vec<_>>(),
            &b.iter().map(homogeneous).collect::<Vec<_>>(),
        )
        .unwrap();
        assert_eq!(facets.len(), expected.len());
        let expected_dirs: BTreeSet<_> = directions(&eh).unwrap().into_iter().collect();
        assert_eq!(
            facets
                .iter()
                .map(|(a, b, _, _)| (a.clone(), b.clone()))
                .collect::<BTreeSet<_>>(),
            expected_dirs
        );
        for (nx, ny, n, d) in facets {
            let (sn, sd) = support(&eh, &nx, &ny, true);
            assert_eq!(n * sd, sn * d);
        }
    }
}
use std::collections::BTreeSet;
#[test]
fn canonical_table() {
    for (input, wanted) in [
        (
            r#"{"z":true,"a":[null,false,123456789012345678901234567890]}"#,
            r#"{"a":[null,false,123456789012345678901234567890],"z":true}"#,
        ),
        (r#""é中😀""#, r#""\u00e9\u4e2d\ud83d\ude00""#),
        (
            r#""\"\\\n\r\t\b\f\u0000\u001f\u007f""#,
            r#""\"\\\n\r\t\b\f\u0000\u001f\u007f""#,
        ),
        (
            r#"{"😀":1,"\ue000":2,"a":3}"#,
            r#"{"a":3,"\ue000":2,"\ud83d\ude00":1}"#,
        ),
        ("0.1", "0.1"),
        ("1e-05", "1e-05"),
        ("1e16", "1e+16"),
        ("1.5e300", "1.5e+300"),
        ("-0.0", "-0.0"),
        ("-0", "0"),
        ("1.0", "1.0"),
    ] {
        let v: Value = crate::value::from_str(input).unwrap();
        assert_eq!(pyjson::canonical(&v).unwrap(), wanted);
    }
    let v = json!({"z":[1,{"é":true}],"a":{},"b":[]});
    assert_eq!(
        pyjson::pretty(&v).unwrap(),
        "{\n \"z\": [\n  1,\n  {\n   \"\\u00e9\": true\n  }\n ],\n \"a\": {},\n \"b\": []\n}\n"
    );
    assert_eq!(
        pyjson::compact(&json!({"a":1,"b":[true,false]})).unwrap(),
        "{\"a\": 1, \"b\": [true, false]}"
    );
    assert!(pyjson::equal(
        &json!([1,true,{"x":0}]),
        &json!([1.0,1,{"x":false}])
    ));
    assert!(!pyjson::equal(&json!("1"), &json!(1)));
    assert!(!pyjson::equal(
        &json!(9_007_199_254_740_993_u64),
        &json!(9_007_199_254_740_992.0)
    ));
    assert_eq!(pyjson::repr_string("a'b"), "\"a'b\"");
    assert_eq!(pyjson::repr_string("a\n"), "'a\\n'");
}
#[test]
fn python_float_corpus() {
    for case in array(&read("floats.json")).unwrap() {
        let bits = u64::from_str_radix(case[0].as_str().unwrap(), 16).unwrap();
        assert_eq!(
            pyjson::float_repr(f64::from_bits(bits)),
            case[1].as_str().unwrap(),
            "bits={bits:016x}"
        );
    }
}
#[test]
fn python_sampling_table() {
    for case in array(&read("sampling.json")).unwrap() {
        let seed = integer(case[0].as_str().unwrap()).unwrap();
        let mut rng = Random::new(&seed);
        let got = rng
            .sample(index(&case[1]).unwrap(), index(&case[2]).unwrap())
            .unwrap();
        let wanted: Vec<_> = array(&case[3])
            .unwrap()
            .iter()
            .map(|v| index(v).unwrap())
            .collect();
        assert_eq!(got, wanted, "seed {seed}");
    }
    let mut r = Random::new(&12345.into());
    assert_eq!(r.getrandbits(0), 0);
    assert_eq!(r.getrandbits(32), 1_789_368_711_u32);
    assert!(r.sample(1, 2).is_err());
    assert!(r.randbelow(0).is_err());
}
fn node(text: &str) -> crate::Result<NodeStream> {
    NodeStream::from_reader(Box::new(Cursor::new(text.as_bytes().to_vec())))
}
fn node_failure(text: &str) -> String {
    match node(text) {
        Err(e) => e.to_string(),
        Ok(mut s) => loop {
            match s.next_step() {
                Err(e) => break e.to_string(),
                Ok(None) => panic!("accepted {text}"),
                Ok(Some(_)) => {}
            }
        },
    }
}
#[test]
fn streaming_checks_and_hash() {
    let text = r#"{"z":4,"b":1.0,"a":"😀", "steps":[{"b":2,"a":1},null],"y":3}"#;
    let mut s = node(text).unwrap();
    assert!(s.header.get("steps").is_none());
    assert_eq!(s.next_step().unwrap(), Some(json!({"b":2,"a":1})));
    assert!(s.steps().is_err());
    assert_eq!(s.next_step().unwrap(), Some(Value::Null));
    assert_eq!(s.next_step().unwrap(), None);
    let v: Value = crate::value::from_str(text).unwrap();
    assert_eq!(
        s.sha256.unwrap(),
        pyjson::digest(pyjson::canonical(&v).unwrap().as_bytes())
    );
    for (text, message) in [
        ("[]", "the node is not a JSON object"),
        ("{}", "the node has no steps"),
        (r#"{"steps":{}}"#, "the node's steps are not an array"),
        (
            r#"{"a":1,"a":2,"steps":[]}"#,
            "the node repeats its member 'a'",
        ),
        (
            r#"{"steps":[],"a":1}"#,
            "the node's member 'a' follows its steps",
        ),
        (r#"{"steps":[]} 0"#, "data follows the node"),
        (r"{1:2}", "a node member's name is not a string"),
        (r#"{"a" 1}"#, "a node member's name lacks its colon"),
        (
            r#"{"steps":[{} {}]}"#,
            "the node's steps are not comma-separated",
        ),
        (
            r#"{"a":{} "steps":[]}"#,
            "the node's members are not comma-separated",
        ),
    ] {
        assert_eq!(node_failure(text), message);
    }
    assert!(node_failure(r#"{"steps":[{"x":]}"#).starts_with("malformed certificate:"));
    // A tiny BufReader forces splits inside UTF-8 and JSON numbers.
    let text = format!(
        "{{\"a\":\"{}😀\",\"steps\":[12345678901234567890,1e-05]}}",
        "x".repeat(10000)
    );
    let source = std::io::BufReader::with_capacity(1, Cursor::new(text.as_bytes().to_vec()));
    let mut s = NodeStream::from_reader(Box::new(source)).unwrap();
    while s.next_step().unwrap().is_some() {}
    assert_eq!(
        s.sha256.unwrap(),
        pyjson::digest(
            pyjson::canonical(&crate::value::from_str(&text).unwrap())
                .unwrap()
                .as_bytes()
        )
    );
}
#[test]
fn verification_fixtures_all_thread_counts() {
    for (label, cell_file) in [
        ("closed", "cells.json"),
        ("stall", "cells.json"),
        ("dead", "dead-cells.json"),
        ("stall-w7-bins8", "../../cells/cover.json"),
    ] {
        let bytes = std::fs::read(data(cell_file)).unwrap();
        let cells = file_cells(data(cell_file).to_str().unwrap(), &pyjson::digest(&bytes)).unwrap();
        for sample in [None, Some(0), Some(2)] {
            if label == "dead" && sample.is_some() {
                continue;
            }
            for threads in [1, 2, 4] {
                let options = Options {
                    sample: sample.map(Integer::from),
                    threads,
                    ..Options::default()
                };
                let result =
                    verify_objects(data(label).to_str().unwrap(), &cells, &options).unwrap();
                let suffix = sample.map_or_else(|| "None".into(), |s| s.to_string());
                assert!(
                    pyjson::equal(&result, &read(&format!("{label}-{suffix}.json"))),
                    "{label} {suffix} threads {threads}: {result}"
                );
                let receipt = verify(data(label).to_str().unwrap(), &cells, &options).unwrap();
                assert_eq!(
                    receipt["status"],
                    if label.starts_with("stall") {
                        "FAIL"
                    } else {
                        "PASS"
                    }
                );
                let keys: Vec<_> = receipt
                    .as_object()
                    .unwrap()
                    .keys()
                    .map(|k| k.text().unwrap())
                    .collect();
                assert_eq!(
                    keys,
                    vec![
                        "schema",
                        "verifier",
                        "provenance",
                        "directory",
                        "cells_source",
                        "mode",
                        "sample_rows_per_step",
                        "sample_seed",
                        "certificate",
                        "mask",
                        "cells",
                        "bins",
                        "closure",
                        "closed",
                        "counts",
                        "status",
                        "failure",
                        "seconds"
                    ]
                );
            }
        }
    }
}

#[test]
fn python_json_extended_domain() {
    for (raw, wanted) in [
        (
            r"[NaN,Infinity,-Infinity,1e999,-1e999]",
            r"[NaN,Infinity,-Infinity,Infinity,-Infinity]",
        ),
        (
            r#"{"\ud800":"\udfff","\ue000":"x","😀":"\ud800a\udc00"}"#,
            r#"{"\ud800":"\udfff","\ue000":"x","\ud83d\ude00":"\ud800a\udc00"}"#,
        ),
        (
            r#"["\ud800\udc00","𐀀","\ud800\u0041"]"#,
            r#"["\ud800\udc00","\ud800\udc00","\ud800A"]"#,
        ),
    ] {
        let value = crate::value::from_str(raw).unwrap();
        assert_eq!(pyjson::canonical(&value).unwrap(), wanted);
    }
    let nan = crate::value::from_str("NaN").unwrap();
    assert!(!pyjson::equal(&nan, &nan));
    assert!(pyjson::equal(&json!([nan]), &json!([nan])));
    assert!(q(&nan).is_err());
    assert!(pyjson::equal(
        &crate::value::from_str("Infinity").unwrap(),
        &crate::value::from_str("1e999").unwrap()
    ));
    let mut stream = node(r#"{"node_id":"\ud800","steps":[NaN,Infinity],"\ud800":1}"#).unwrap();
    while stream.next_step().unwrap().is_some() {}
    let original =
        crate::value::from_str(r#"{"node_id":"\ud800","steps":[NaN,Infinity],"\ud800":1}"#)
            .unwrap();
    assert_eq!(
        stream.sha256.unwrap(),
        pyjson::digest(pyjson::canonical(&original).unwrap().as_bytes())
    );
    assert_eq!(
        node_failure(r#"{"steps":[],"\u0000":0}"#),
        "the node's member '\\x00' follows its steps"
    );
    assert_eq!(
        node_failure(r#"{"steps":[trueX]}"#),
        "the node's steps are not comma-separated"
    );
    let utf16: Vec<u8> = b"\xff\xfe"
        .iter()
        .copied()
        .chain("{\"a\":1}".encode_utf16().flat_map(u16::to_le_bytes))
        .collect();
    assert_eq!(crate::value::from_slice(&utf16).unwrap(), json!({"a":1}));
    let wtf8 = b"\"\xed\xa0\x80\"";
    assert_eq!(
        pyjson::canonical(&crate::value::from_slice(wtf8).unwrap()).unwrap(),
        r#""\ud800""#
    );
    assert!(crate::value::from_slice(b"\"\xc0\x80\"").is_err());
    assert!(crate::value::from_str("01").is_err());
    assert!(crate::value::from_str("1e").is_err());
    assert_eq!(fraction_str("١٢.٥e-١").unwrap(), Q::from((5, 4)));
    assert_eq!(integer("  -١_٢  ").unwrap(), -12);
    assert!(integer("1 2").is_err());
}

#[test]
#[expect(
    clippy::float_cmp,
    reason = "These fixtures require exact Python binary64 rounding results."
)]
fn repr_and_rounding() {
    for (s, expected) in [
        ("\u{feff}", "'\\ufeff'"),
        ("\u{e000}", "'\\ue000'"),
        ("\u{378}", "'\\u0378'"),
        ("\u{a0}", "'\\xa0'"),
        ("\u{2028}", "'\\u2028'"),
    ] {
        assert_eq!(pyjson::repr_string(s), expected);
    }
    assert_eq!(pyjson::round_float(2.675, 2).unwrap(), 2.67);
    assert_eq!(pyjson::round_float(1.2345, 3).unwrap(), 1.234);
    assert_eq!(pyjson::round_float(2.5, 0).unwrap(), 2.0);
    assert_eq!(pyjson::round_float(3.5, 0).unwrap(), 4.0);
    assert_eq!(pyjson::round_float(-2.5, 0).unwrap(), -2.0);
}

#[test]
fn threaded_failure_is_lowest_sequential_row() {
    let raw = std::fs::read(data("cells.json")).unwrap();
    let cells = file_cells(data("cells.json").to_str().unwrap(), &pyjson::digest(&raw)).unwrap();
    let (seed, _) = crate::stream::load_object(&data("closed/seed-any-name.json.gz")).unwrap();
    let (node, _) = crate::stream::load_object(&data("closed/node-any-name.json.gz")).unwrap();
    let full = (0..6).collect();
    for threads in [1, 2, 4] {
        let mut state = State {
            cells: cells.polygons.clone(),
            cap: cells.cap.clone(),
            bins: 3.into(),
            mask: vec![0, 1],
            mask_values: vec![json!(0), json!(1)],
            groups: BTreeMap::default(),
            rows: BTreeMap::default(),
            stats: BTreeMap::default(),
            memos: Memos::default(),
        };
        check_seed(&mut state, &seed, &node).unwrap();
        let first = &node["steps"][0];
        let (rows, planes, live) =
            check_step(&mut state, first, 0, &node["node_id"], &full, None).unwrap();
        compress(&mut state, first, 0, &planes, live).unwrap();
        state.rows.insert(0, rows);
        let mut step = node["steps"][1].clone();
        let mut rows = array(&step["rows"]).unwrap().clone();
        rows[0].as_object_mut().unwrap().insert(
            "collision_regions".into(),
            json!([
                {"partner":0,"vertices":[["0","0"],["2","0"],["2","2"]]}
            ]),
        );
        rows[1]
            .as_object_mut()
            .unwrap()
            .insert("reference".into(), json!({}));
        step.as_object_mut()
            .unwrap()
            .insert("rows".into(), Value::Array(rows));
        let pool = if threads > 1 {
            Some(
                rayon::ThreadPoolBuilder::new()
                    .num_threads(threads)
                    .build()
                    .unwrap(),
            )
        } else {
            None
        };
        let error = check_step(&mut state, &step, 1, &node["node_id"], &full, pool.as_ref())
            .err()
            .unwrap();
        assert_eq!(
            error.to_string(),
            "step 1 row 0: collision region escapes the required domain"
        );
    }
}

#[test]
fn huge_integer_is_not_infinity() {
    let big = crate::value::from_str(&format!("1{}", "0".repeat(400))).unwrap();
    let inf = crate::value::from_str("Infinity").unwrap();
    assert!(!pyjson::equal(&big, &inf));
}

#[test]
fn homogeneous_hull_matches_rational_hull_with_large_coordinates() {
    fn reference(points: &[Point]) -> Poly {
        let mut pts = points.to_vec();
        pts.sort();
        pts.dedup();
        if pts.len() <= 2 {
            return pts;
        }
        let mut lower: Poly = vec![];
        let mut upper: Poly = vec![];
        for p in &pts {
            while lower.len() >= 2
                && cross(&lower[lower.len() - 2], &lower[lower.len() - 1], p) <= 0
            {
                lower.pop();
            }
            lower.push(p.clone());
        }
        for p in pts.iter().rev() {
            while upper.len() >= 2
                && cross(&upper[upper.len() - 2], &upper[upper.len() - 1], p) <= 0
            {
                upper.pop();
            }
            upper.push(p.clone());
        }
        lower.pop();
        upper.pop();
        lower.extend(upper);
        lower
    }
    let mut rng = Random::new(&7345.into());
    for bits in [0, 60, 127, 200, 512] {
        let scale = Q::from(Integer::from(1) << bits);
        for _ in 0..30 {
            let mut points: Poly = (0..15)
                .map(|_| {
                    (
                        Q::from((rng.word().cast_signed() % 9, 7)) * &scale,
                        Q::from((rng.word().cast_signed() % 9, 11)) / &scale,
                    )
                })
                .collect();
            points.extend([p(0, 0), p(0, 0), p(1, 1), p(2, 2)]);
            assert_eq!(hull(&points), reference(&points));
        }
    }
}

#[test]
fn sweep_event_set_matches_all_pairs_rational_reference() {
    let mut rng = Random::new(&6453.into());
    for bits in [0, 70, 200] {
        let scale = Q::from(Integer::from(1) << bits);
        for _ in 0..30 {
            let mut polys: Vec<Poly> = (0..4)
                .map(|_| {
                    random_polygon(&mut rng)
                        .into_iter()
                        .map(|(x, y)| (x * &scale, y / &scale))
                        .collect()
                })
                .collect();
            polys.push(polys[0].clone()); // duplicate edges must preserve the complete event set
            let left = Q::from(-3) * &scale;
            let right = Q::from(3) * &scale;
            let mut expected = BTreeSet::new();
            let mut lines = vec![];
            for p in &polys {
                for i in 0..p.len() {
                    let a = &p[i];
                    let b = &p[(i + 1) % p.len()];
                    if left <= a.0 && a.0 <= right {
                        expected.insert(a.0.clone());
                    }
                    if a.0 == b.0 {
                        continue;
                    }
                    let slope = Q::from(&b.1 - &a.1) / Q::from(&b.0 - &a.0);
                    let intercept = a.1.clone() - Q::from(&slope * &a.0);
                    lines.push((
                        a.0.clone().min(b.0.clone()),
                        a.0.clone().max(b.0.clone()),
                        slope,
                        intercept,
                    ));
                }
            }
            for (i, a) in lines.iter().enumerate() {
                for b in &lines[..i] {
                    if a.2 == b.2 {
                        continue;
                    }
                    let x = Q::from(&b.3 - &a.3) / Q::from(&a.2 - &b.2);
                    if left <= x && x <= right && a.0 <= x && x <= a.1 && b.0 <= x && x <= b.1 {
                        expected.insert(x);
                    }
                }
            }
            let hp: Vec<Vec<HPoint>> = polys
                .iter()
                .map(|p| p.iter().map(homogeneous).collect())
                .collect();
            let (edges, _) = compile_edges(&hp).unwrap();
            let actual = sweep_events(
                &hp,
                &edges,
                &(left.numer().into(), left.denom().into()),
                &(right.numer().into(), right.denom().into()),
            )
            .unwrap();
            let actual: Vec<Q> = actual
                .into_iter()
                .map(|(n, d)| Q::from((Integer::from(n), Integer::from(d))))
                .collect();
            assert_eq!(actual, expected.into_iter().collect::<Vec<_>>());
        }
    }
}

/// The `owned_hulls_intersect` fixtures: one closure of that kind, the same node declaring
/// the other kind, and the kernel point moved out of the other owner's hull.
#[test]
fn owned_hulls_intersect_fixtures_all_thread_counts() {
    let bytes = std::fs::read(data("cells.json")).unwrap();
    let cells = file_cells(
        data("cells.json").to_str().unwrap(),
        &pyjson::digest(&bytes),
    )
    .unwrap();
    for label in ["ohi", "ohi-wrong-kind", "ohi-point-outside"] {
        let expected = read(&format!("{label}-expected.json"));
        for threads in [1, 2, 4] {
            let options = Options {
                threads,
                ..Options::default()
            };
            let receipt = verify(data(label).to_str().unwrap(), &cells, &options).unwrap();
            let context = format!("{label} threads {threads}: {receipt}");
            assert!(
                pyjson::equal(&receipt["status"], &expected["status"]),
                "{context}"
            );
            match label {
                "ohi" => {
                    assert_eq!(receipt["status"], "PASS", "{context}");
                    assert_eq!(
                        receipt["closure"]["kind"], "owned_hulls_intersect",
                        "{context}"
                    );
                    assert!(
                        pyjson::equal(&receipt["closure"], &expected["closure"]),
                        "{context}"
                    );
                    assert!(
                        pyjson::equal(&receipt["counts"], &expected["counts"]),
                        "{context}"
                    );
                }
                "ohi-wrong-kind" => assert_eq!(
                    receipt["failure"], "step 0: the derived closure is not the declared one",
                    "{context}"
                ),
                _ => assert_eq!(receipt["failure"], "no closure derived", "{context}"),
            }
            assert!(pyjson::equal(
                &receipt["failure"],
                if label == "ohi" {
                    &Value::Null
                } else {
                    &expected["failure"]
                }
            ));
        }
    }
}

#[test]
fn receipt_publication_replaces_complete_json_and_cleans_staging() {
    let directory = tempfile::tempdir().unwrap();
    let output = directory.path().join("nested/receipt-λ.json");
    std::fs::create_dir_all(output.parent().unwrap()).unwrap();
    std::fs::write(&output, b"old receipt\n").unwrap();
    let receipt = json!({"status": "PASS", "failure": null, "mode": "full"});
    write_receipt(&output, &receipt).unwrap();
    assert_eq!(
        std::fs::read_to_string(&output).unwrap(),
        pyjson::pretty(&receipt).unwrap()
    );
    assert_eq!(
        std::fs::read_dir(output.parent().unwrap()).unwrap().count(),
        1
    );
    let new_output = directory.path().join("new/receipt.json");
    write_receipt(&new_output, &receipt).unwrap();
    assert_eq!(
        std::fs::read(&new_output).unwrap(),
        std::fs::read(&output).unwrap()
    );
}

#[test]
fn receipt_publication_write_failure_preserves_old_file() {
    use std::io::Write;
    let directory = tempfile::tempdir().unwrap();
    let output = directory.path().join("receipt.json");
    std::fs::write(&output, b"old receipt\n").unwrap();
    let receipt = json!({"status": "PASS"});
    let result = write_receipt_with(
        &output,
        &receipt,
        |file, bytes| {
            file.write_all(&bytes[..5])?;
            assert_eq!(std::fs::read(&output)?, b"old receipt\n");
            Err(std::io::Error::other("injected partial receipt write"))
        },
        |_, _| panic!("a partial write must never reach publication"),
    );
    assert!(
        result
            .unwrap_err()
            .to_string()
            .contains("injected partial receipt write")
    );
    assert_eq!(std::fs::read(&output).unwrap(), b"old receipt\n");
    assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 1);
}

#[test]
fn receipt_publication_rename_failure_preserves_old_file() {
    use std::io::Write;
    let directory = tempfile::tempdir().unwrap();
    let output = directory.path().join("receipt.json");
    std::fs::write(&output, b"old receipt\n").unwrap();
    let receipt = json!({"status": "PASS"});
    let expected = pyjson::pretty(&receipt).unwrap();
    let result = write_receipt_with(
        &output,
        &receipt,
        |file, bytes| file.write_all(bytes),
        |staged, destination| {
            assert_eq!(staged.parent(), destination.parent());
            assert_eq!(std::fs::read_to_string(&staged).unwrap(), expected);
            assert_eq!(std::fs::read(destination).unwrap(), b"old receipt\n");
            Err(tempfile::PathPersistError {
                error: std::io::Error::other("injected receipt rename"),
                path: staged,
            })
        },
    );
    assert!(
        result
            .unwrap_err()
            .to_string()
            .contains("injected receipt rename")
    );
    assert_eq!(std::fs::read(&output).unwrap(), b"old receipt\n");
    assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 1);
}

#[test]
fn receipt_publication_refuses_directory_collision() {
    let directory = tempfile::tempdir().unwrap();
    let output = directory.path().join("receipt.json");
    std::fs::create_dir(&output).unwrap();
    std::fs::write(output.join("keep"), b"untouched").unwrap();
    assert!(write_receipt(&output, &json!({"status": "PASS"})).is_err());
    assert_eq!(std::fs::read(output.join("keep")).unwrap(), b"untouched");
    assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 1);
}

#[cfg(unix)]
#[test]
fn receipt_publication_replaces_symlink_and_uses_private_permissions() {
    use std::os::unix::fs::{PermissionsExt, symlink};
    let directory = tempfile::tempdir().unwrap();
    let target = directory.path().join("original.json");
    let output = directory.path().join("receipt.json");
    std::fs::write(&target, b"old receipt\n").unwrap();
    symlink(&target, &output).unwrap();
    let receipt = json!({"status": "PASS"});
    write_receipt(&output, &receipt).unwrap();
    assert!(
        !std::fs::symlink_metadata(&output)
            .unwrap()
            .file_type()
            .is_symlink()
    );
    assert_eq!(
        std::fs::read_to_string(&output).unwrap(),
        pyjson::pretty(&receipt).unwrap()
    );
    assert_eq!(std::fs::read(&target).unwrap(), b"old receipt\n");
    assert_eq!(
        std::fs::metadata(&output).unwrap().permissions().mode() & 0o777,
        0o600
    );
    assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 2);
}

#[test]
fn receipt_publication_reports_cleanup_failure_with_original_error() {
    use std::io::Write;
    let directory = tempfile::tempdir().unwrap();
    let output = directory.path().join("receipt.json");
    std::fs::write(&output, b"old receipt\n").unwrap();
    let mut stranded = None;
    let result = write_receipt_with(
        &output,
        &json!({"status": "PASS"}),
        |file, bytes| file.write_all(bytes),
        |staged, _| {
            std::fs::remove_file(&staged).unwrap();
            std::fs::create_dir(&staged).unwrap();
            stranded = Some(staged.to_path_buf());
            Err(tempfile::PathPersistError {
                error: std::io::Error::other("injected receipt rename"),
                path: staged,
            })
        },
    );
    let error = result.unwrap_err().to_string();
    assert!(error.contains("injected receipt rename"));
    assert!(error.contains("staging cleanup failed"));
    assert_eq!(std::fs::read(&output).unwrap(), b"old receipt\n");
    std::fs::remove_dir(stranded.unwrap()).unwrap();
}

#[cfg(windows)]
#[test]
fn receipt_publication_open_destination_refusal_preserves_old_file() {
    use std::os::windows::fs::OpenOptionsExt;
    let directory = tempfile::tempdir().unwrap();
    let output = directory.path().join("receipt.json");
    std::fs::write(&output, b"old receipt\n").unwrap();
    let held = std::fs::OpenOptions::new()
        .read(true)
        .share_mode(0)
        .open(&output)
        .unwrap();
    assert!(write_receipt(&output, &json!({"status": "PASS"})).is_err());
    assert_eq!(std::fs::read_dir(directory.path()).unwrap().count(), 1);
    drop(held);
    assert_eq!(std::fs::read(&output).unwrap(), b"old receipt\n");
}
