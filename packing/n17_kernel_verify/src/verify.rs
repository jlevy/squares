//! Certificate admission, replay, closure checks, and receipts.
use crate::exact::{
    Plane, Point, Poly, Q, array, at, dot, get, index, int_value, integer, is_int, iterable,
    numeric, object, planes, point, poly, pylen, q, repr_point,
};
use crate::geom::{
    area2, clip_closed, core_strict, hull, intersect_convex, minkowski_diff, owned, planes_of,
    same_set, wall_box,
};
use crate::sweep::{
    Direction, Facet, HPoint, Ratio, covered_by_sweep, degenerate_covered, difference_facets,
    homogeneous, support,
};
use crate::{Result, malformed, require};
use crate::{json, value::Value};
use crate::{
    pyjson,
    pyrandom::Random,
    stream::{NodeStream, load_object},
};
use rayon::prelude::*;
use rug::Integer;
use std::{
    collections::{BTreeMap, BTreeSet},
    io::Write,
    path::Path,
    time::Instant,
};

#[derive(Clone)]
/// Ordered certificate cells and the provenance of their supplied geometry.
pub struct Cells {
    /// Cell names in the source order.
    pub names: Vec<Value>,
    /// Cell polygons aligned with names.
    pub polygons: Vec<Poly>,
    /// Exact declared wall side cap.
    pub cap: Q,
    /// Receipt metadata identifying the source of cell geometry.
    pub source: Value,
}
impl Cells {
    fn from_data(data: &Value, source: Value) -> Result<Self> {
        let names: Vec<Value> = iterable(get(data, "order")?)?
            .into_iter()
            .map(std::borrow::Cow::into_owned)
            .collect();
        let obj = get(data, "cells")?;
        let polygons = names
            .iter()
            .map(|n| {
                let key = n
                    .key()
                    .ok_or_else(|| malformed("cell name is not a string"))?;
                poly(
                    object(obj)?
                        .get_key(&key)
                        .ok_or_else(|| malformed("missing cell"))?,
                )
            })
            .collect::<Result<_>>()?;
        Ok(Self {
            names,
            polygons,
            cap: q(get(data, "U")?)?,
            source,
        })
    }
}
/// Load declared cell geometry only after its byte digest matches the supplied SHA-256.
pub fn file_cells(path: &str, sha256: &str) -> Result<Cells> {
    let raw = std::fs::read(path)?;
    let digest = pyjson::digest(&raw);
    require(
        digest == sha256,
        format!("cells file digest {digest} is not the stated one"),
    )?;
    let data: Value = crate::value::from_slice(&raw)?;
    Cells::from_data(&data, json!({"kind":"file","path":path,"sha256":digest}))
}
/// Load the build-time embedded cover, failing when no cover was supplied.
pub fn cover_cells() -> Result<Cells> {
    let raw = include_bytes!(concat!(env!("OUT_DIR"), "/cover.json"));
    if raw.is_empty() {
        return Err(malformed(
            "embedded cells/cover.json was not supplied at build time; use --cells and --cells-sha256",
        ));
    }
    let data: Value = crate::value::from_slice(raw)?;
    Cells::from_data(&data, json!({"kind":"cover","design":get(&data,"design")?}))
}
#[derive(Clone)]
/// An admitted cover row with homogeneous geometry and cached domain support minima.
pub struct CoverRow {
    /// Original declared domain retained for equality checks.
    pub domain_given: Value,
    /// Original declared core retained for equality checks.
    pub core_given: Value,
    /// Admitted homogeneous domain hull.
    pub domain: Vec<HPoint>,
    /// Admitted homogeneous core hull.
    pub core: Vec<HPoint>,
    /// Support minima cached by exact normal direction.
    pub minima: BTreeMap<Direction, Ratio>,
}
impl CoverRow {
    /// Return and memoize the exact minimum support for a domain normal.
    #[must_use]
    pub fn minimum(&mut self, nx: &crate::int::Int, ny: &crate::int::Int) -> Ratio {
        self.minima
            .entry((nx.clone(), ny.clone()))
            .or_insert_with(|| support(&self.domain, nx, ny, false))
            .clone()
    }
}
#[derive(Clone)]
/// An accepted interval row carrying its outer hull, residuals, and optional cover.
pub struct Row {
    /// Exact half-angle parameter bounds.
    pub interval: Point,
    /// Original row reference used by predecessor resolution.
    pub reference: Value,
    /// Admitted outer convex hull.
    pub outer: Poly,
    /// Remaining polygon regions after admitted exclusions.
    pub residual: Vec<Poly>,
    /// Optional admitted cover payload.
    pub cover: Option<CoverRow>,
}
impl Row {
    fn new(interval: Point, reference: Value, outer: Poly, residual: Vec<Poly>) -> Self {
        Self {
            interval,
            reference,
            outer,
            residual,
            cover: None,
        }
    }
}
type CorePair = (Vec<HPoint>, Vec<HPoint>);
type HullPair = (Poly, Poly);
/// Exact integer counters emitted into verification receipts.
pub type Stats = BTreeMap<String, Integer>;
fn tick(stats: &mut Stats, key: &str, n: usize) {
    *stats.entry(key.into()).or_default() += n;
}
#[derive(Default)]
/// Geometry caches keyed by the complete exact operands.
pub struct Memos {
    /// Facets cached by the complete partner/core pair.
    pub facets: BTreeMap<CorePair, Vec<Facet>>,
    /// Forbidden hulls cached by the complete group/core pair.
    pub forbidden: BTreeMap<HullPair, Poly>,
}
impl Memos {
    /// Memoize partner-minus-core support facets by exact homogeneous hull pairs.
    pub fn difference(&mut self, partner: &[HPoint], core: &[HPoint]) -> Result<&[Facet]> {
        let key = (partner.to_vec(), core.to_vec());
        let entry = self.facets.entry(key);
        Ok(match entry {
            std::collections::btree_map::Entry::Occupied(e) => e.into_mut(),
            std::collections::btree_map::Entry::Vacant(e) => {
                e.insert(difference_facets(partner, core)?)
            }
        })
    }
    /// Memoize the group-minus-core hull by exact point sets.
    #[must_use]
    pub fn forbidden_region(&mut self, group: &[Point], core: &[Point]) -> Poly {
        self.forbidden
            .entry((group.to_vec(), core.to_vec()))
            .or_insert_with(|| minkowski_diff(group, core))
            .clone()
    }
}
/// Per-object replay state; owners, rows, and caches remain local to that object.
pub struct State {
    /// Ordered exact cell polygons.
    pub cells: Vec<Poly>,
    /// Exact declared wall side cap.
    pub cap: Q,
    /// Exact number of declared angle bins.
    pub bins: Integer,
    /// Owner indices in declared order.
    pub mask: Vec<usize>,
    /// Original owner values aligned with mask.
    pub mask_values: Vec<Value>,
    /// Replayed group hulls indexed by owner.
    pub groups: BTreeMap<usize, Poly>,
    /// Accepted interval rows indexed by owner.
    pub rows: BTreeMap<usize, Vec<Row>>,
    /// Exact verification counters.
    pub stats: Stats,
    /// Per-object geometry caches.
    pub memos: Memos,
}
impl State {
    fn new(cells: &Cells, bins: Integer, mask: Vec<usize>, mask_values: Vec<Value>) -> Self {
        Self {
            cells: cells.polygons.clone(),
            cap: cells.cap.clone(),
            bins,
            mask,
            mask_values,
            groups: BTreeMap::new(),
            rows: BTreeMap::new(),
            stats: BTreeMap::new(),
            memos: Memos::default(),
        }
    }
    /// Add n to a named exact replay counter.
    pub fn tick(&mut self, key: &str, n: usize) {
        tick(&mut self.stats, key, n);
    }
    fn owner_name(&self, o: usize) -> Result<String> {
        let i = self
            .mask
            .iter()
            .position(|&k| k == o)
            .ok_or_else(|| malformed("unknown owner"))?;
        pyjson::pystr(&self.mask_values[i])
    }
}
fn group(s: &State, o: usize) -> Result<&Poly> {
    s.groups.get(&o).ok_or_else(|| malformed("unknown group"))
}
fn rows(s: &State, o: usize) -> Result<&Vec<Row>> {
    s.rows
        .get(&o)
        .ok_or_else(|| malformed("unknown owner rows"))
}
fn empty(v: &Value) -> bool {
    matches!(v,Value::Array(a) if a.is_empty())
}
fn eq(a: &Value, b: &Value) -> bool {
    pyjson::equal(a, b)
}
fn polies(v: &Value, convex: bool) -> Result<Vec<Poly>> {
    iterable(v)?
        .iter()
        .map(|v| {
            let p = poly(v)?;
            Ok(if convex { hull(&p) } else { p })
        })
        .collect()
}
/// Validate seed/node framing and return the declared owner mask.
#[expect(
    clippy::similar_names,
    reason = "The certificate seed and its seen-cell set have distinct roles."
)]
pub fn check_frame(seed: &Value, node: &Value, cells: &Cells) -> Result<Vec<usize>> {
    require(
        eq(get(seed, "schema")?, &json!("generic_wall_seed_v1")),
        "seed schema",
    )?;
    require(
        eq(get(node, "schema")?, &json!("exact_generic_owned_hull_v1")),
        "node schema",
    )?;
    for doc in [seed, node] {
        require(
            q(get(doc, "U")?)? == cells.cap,
            "the cap is not the cells' cap",
        )?;
        require(
            q(get(doc, "B")?)? == 1,
            "field and physical coordinates differ",
        )?;
    }
    let mask = get(seed, "mask")?;
    require(
        eq(get(node, "mask")?, mask),
        "the node's mask is not the seed's",
    )?;
    let valid = if let Some(a) = mask.as_array() {
        if a.iter()
            .any(|v| matches!(v, Value::Array(_) | Value::Object(_)))
        {
            return Err(malformed("unhashable mask member"));
        }
        let mut seen = BTreeSet::new();
        let mut good = a.len() >= 2;
        for k in a {
            if !is_int(k) {
                good = false;
                break;
            }
            let n = int_value(k)?;
            if n < 0 || n >= cells.names.len() || !seen.insert(n) {
                good = false;
                break;
            }
        }
        good
    } else {
        false
    };
    require(valid, "the mask is not a set of cell indices")?;
    require(
        get(node, "parent")?.is_null()
            && empty(get(node, "constraints")?)
            && get(node, "guard_source")?.is_null(),
        "the node is not a root node",
    )?;
    let world = get(seed, "world")?;
    require(
        pylen(world)? == cells.names.len(),
        "the seed's world has the wrong size",
    )?;
    for (k, p) in cells.polygons.iter().enumerate() {
        require(
            same_set(&poly(at(world, k)?)?, p),
            format!("world cell {k} differs"),
        )?;
    }
    array(mask)?.iter().map(index).collect()
}
/// Admit seed groups and rows after checking their geometry and ownership.
pub fn check_seed(state: &mut State, seed: &Value, node: &Value) -> Result<()> {
    for o in state.mask.clone() {
        let name = state.owner_name(o)?;
        let points = poly(get(get(seed, "groups")?, &name)?)?;
        for pt in &points {
            require(
                owned(&state.cells[o], pt, &state.cap, &Q::new(), &Q::from(1), 0)?,
                format!("seed point {} of {name} not owned", repr_point(pt)),
            )?;
        }
        state.groups.insert(o, hull(&points));
        let seed_rows_value = get(get(seed, "cells")?, &name)?;
        let seed_rows_count = pylen(seed_rows_value)?;
        require(
            state.bins == seed_rows_count,
            format!("seed owner {name} has the wrong number of rows"),
        )?;
        let seed_rows = iterable(seed_rows_value)?;
        let mut accepted = vec![];
        for (i, r) in seed_rows.iter().enumerate() {
            let interval = point(get(r, "interval")?)?;
            let (lo, hi) = &interval;
            require(
                *lo == Q::from((Integer::from(i), state.bins.clone()))
                    && *hi == Q::from((Integer::from(i + 1), state.bins.clone())),
                format!("seed row {name}/{i} interval"),
            )?;
            let domain = intersect_convex(&state.cells[o], &wall_box(lo, hi, &state.cap))?;
            require(
                same_set(&poly(get(r, "outer_domain")?)?, &domain),
                format!("seed row {name}/{i} domain"),
            )?;
            let residual = polies(get(r, "residual_polygons")?, false)?;
            require(
                (residual.is_empty() && domain.is_empty())
                    || (residual.len() == 1 && same_set(&residual[0], &domain)),
                format!("seed row {name}/{i} residual"),
            )?;
            let reference = get(r, "reference")?;
            require(
                eq(reference, &json!({"kind":"wall_seed","owner":o,"row":i})),
                format!("seed row {name}/{i} reference"),
            )?;
            accepted.push(Row::new(
                interval,
                reference.clone(),
                hull(&domain),
                residual.iter().map(|p| hull(p)).collect(),
            ));
        }
        state.rows.insert(o, accepted);
        state.tick("seed_points", points.len());
        state.tick("seed_rows", seed_rows_count);
    }
    for &o in &state.mask {
        let name = state.owner_name(o)?;
        let initial = get(node, "initial")?;
        require(
            same_set(
                &poly(get(get(initial, "groups")?, &name)?)?,
                group(state, o)?,
            ),
            format!("initial group {name}"),
        )?;
        require(
            eq(
                get(get(initial, "cell_references")?, &name)?,
                &Value::Array(
                    rows(state, o)?
                        .iter()
                        .map(|r| r.reference.clone())
                        .collect(),
                ),
            ),
            format!("initial references {name}"),
        )?;
    }
    Ok(())
}
/// Validate declared cover geometry before caching its homogeneous form.
pub fn admit_cover(row: &Row, item: &Value, si: usize, pj: usize) -> Result<CoverRow> {
    let vertices: Poly = row.residual.iter().flatten().cloned().collect();
    let domain = hull(&vertices);
    let given = poly(get(item, "domain")?)?;
    let rownum = pyjson::pystr(get(&row.reference, "row")?)?;
    require(
        same_set(&given, &domain),
        format!("step {si} partner {pj} row {rownum} domain"),
    )?;
    let core = hull(&poly(get(item, "core")?)?);
    require(
        core.len() >= 3 && area2(&core) > 0,
        format!("step {si}: partner {pj} core"),
    )?;
    require(
        core_strict(&core, &row.interval.0, &row.interval.1),
        format!("step {si} partner {pj} core not strict"),
    )?;
    Ok(CoverRow {
        domain_given: get(item, "domain")?.clone(),
        core_given: get(item, "core")?.clone(),
        domain: domain.iter().map(homogeneous).collect(),
        core: core.iter().map(homogeneous).collect(),
        minima: BTreeMap::new(),
    })
}
/// Check referenced partner covers and exact residual coverage.
pub fn check_partners(
    state: &mut State,
    step: &Value,
    si: usize,
) -> Result<BTreeMap<usize, Vec<CoverRow>>> {
    let owner = index(get(step, "owner")?)?;
    let mut partners = BTreeMap::new();
    for (key, items) in object(get(step, "prior_partner_pose_covers")?)? {
        let n = integer(&key.text()?)?;
        let pj = n.to_usize();
        require(
            pj.is_some_and(|p| state.mask.contains(&p) && p != owner),
            format!("step {si}: partner {n}"),
        )?;
        let pj = pj.ok_or_else(|| malformed("partner index"))?;
        let accepted = state
            .rows
            .get_mut(&pj)
            .ok_or_else(|| malformed("unknown partner"))?;
        require(
            pylen(items)? == accepted.len(),
            format!("step {si}: partner {pj} cover length"),
        )?;
        let items = iterable(items)?;
        let mut live = vec![];
        for (item, r) in items.iter().zip(accepted) {
            require(
                eq(get(item, "reference")?, &r.reference),
                format!("step {si}: partner {pj} reference"),
            )?;
            require(
                point(get(item, "interval")?)? == r.interval,
                format!("step {si}: partner {pj} interval"),
            )?;
            if !r.residual.iter().any(|p| !p.is_empty()) {
                require(
                    empty(get(item, "domain")?) && empty(get(item, "core")?),
                    format!("step {si}: dead row"),
                )?;
                continue;
            }
            let cached = if let Some(c) = &r.cover {
                eq(&c.domain_given, get(item, "domain")?) && eq(&c.core_given, get(item, "core")?)
            } else {
                false
            };
            if !cached {
                r.cover = Some(admit_cover(r, item, si, pj)?);
            }
            live.push(
                r.cover
                    .clone()
                    .ok_or_else(|| malformed("missing admitted cover"))?,
            );
        }
        require(!live.is_empty(), format!("step {si}: empty partner cover"))?;
        state.tick("partner_rows", live.len());
        partners.insert(pj, live);
    }
    Ok(partners)
}
/// Validate collision half-planes against replayed partner geometry.
pub fn check_collisions(
    memos: &mut Memos,
    stats: &mut Stats,
    row: &Value,
    where_: &str,
    core: &[Point],
    required: &[Point],
    partners: &mut BTreeMap<usize, Vec<CoverRow>>,
) -> Result<Vec<Poly>> {
    let mut regions = vec![];
    let core_h: Vec<_> = core.iter().map(homogeneous).collect();
    let mut required_planes = None;
    for item in &iterable(get(row, "collision_regions")?)? {
        let pv = get(item, "partner")?;
        let pj = match pv {
            Value::Number(_) | Value::Bool(_) => q(pv).ok().and_then(|n| {
                if n.is_integer() {
                    n.numer().to_usize()
                } else {
                    None
                }
            }),
            Value::Array(_) | Value::Object(_) => {
                return Err(malformed("unhashable collision partner"));
            }
            _ => None,
        };
        if let Value::SurrogateString(points) = pv {
            let mut message: Vec<u32> = format!("{where_}: collision partner ")
                .chars()
                .map(u32::from)
                .collect();
            message.extend(points);
            return Err(crate::Error::UnicodeCheck(message));
        }
        let pname = pyjson::pystr(pv)?;
        require(
            pj.is_some_and(|p| partners.contains_key(&p)),
            format!("{where_}: collision partner {pname}"),
        )?;
        let pj = pj.ok_or_else(|| malformed("partner index"))?;
        let region = hull(&poly(get(item, "vertices")?)?);
        require(
            region.len() >= 3 && area2(&region) > 0,
            format!("{where_}: degenerate region"),
        )?;
        if required_planes.is_none() {
            required_planes = Some(planes_of(required)?);
        }
        let planes = required_planes
            .as_ref()
            .ok_or_else(|| malformed("missing planes"))?;
        require(
            region
                .iter()
                .all(|v| planes.iter().all(|(a, b, c)| dot(a, b, v) <= *c)),
            format!("{where_}: collision region escapes the required domain"),
        )?;
        let region_h: Vec<_> = region.iter().map(homogeneous).collect();
        for cover in partners
            .get_mut(&pj)
            .ok_or_else(|| malformed("unknown collision partner"))?
        {
            let facets = memos.difference(&cover.core, &core_h)?;
            require(
                facets.len() >= 3,
                format!("{where_}: degenerate difference"),
            )?;
            for (nx, ny, hn, hd) in facets {
                let (mn, md) = cover.minimum(nx, ny);
                let bound_n = hn * &md + mn * hd;
                let bound_d = hd * &md;
                tick(stats, "collision_facet_checks", region.len());
                for (x, y, z) in &region_h {
                    if crate::int::Int::cmp_products(&(nx * x + ny * y), &bound_d, &bound_n, z)
                        .is_gt()
                    {
                        return Err(crate::Error::Check(format!(
                            "{where_} partner {pname}: region escapes the collision set"
                        )));
                    }
                }
            }
        }
        regions.push(region);
        tick(stats, "collision_regions", 1);
    }
    Ok(regions)
}
struct CoverCheck<'a> {
    owner: usize,
    where_: &'a str,
    core: &'a [Point],
    required: &'a [Point],
    collisions: Vec<Poly>,
    residual: &'a [Poly],
}
#[expect(
    clippy::similar_names,
    reason = "Replay state and separately accumulated stats have distinct roles."
)]
fn check_cover(
    state: &State,
    memos: &mut Memos,
    stats: &mut Stats,
    check: CoverCheck<'_>,
) -> Result<()> {
    let CoverCheck {
        owner,
        where_,
        core,
        required,
        collisions,
        residual,
    } = check;
    let mut every = vec![];
    for &oj in &state.mask {
        let g = group(state, oj)?;
        if oj != owner && !g.is_empty() {
            every.push(memos.forbidden_region(g, core));
        }
    }
    every.extend(collisions);
    every.extend_from_slice(residual);
    if area2(required) > 0 {
        let (ok, probe) = covered_by_sweep(&hull(required), &every)?;
        require(
            ok,
            format!(
                "{where_}: required domain NOT covered (uncovered at x={})",
                probe.map_or_else(|| "None".into(), |q| q.to_string())
            ),
        )?;
    } else {
        require(
            degenerate_covered(required, &every)?,
            format!("{where_}: degenerate row uncovered"),
        )?;
        tick(stats, "degenerate_cover_checks", 1);
    }
    tick(stats, "cover_checks", 1);
    Ok(())
}
/// Canonicalize a predecessor reference for exact matching.
pub fn reference_key(v: &Value) -> Result<String> {
    pyjson::canonical(v)
}
/// Resolve predecessor rows from accepted references for the current step.
pub fn predecessors(accepted: &[Row], rs: &Value, si: usize) -> Result<Vec<Row>> {
    require(
        rs.as_array().is_some_and(|a| !a.is_empty()),
        format!("step {si}: no rows"),
    )?;
    let mut by_reference = BTreeMap::new();
    for r in accepted {
        by_reference.insert(reference_key(&r.reference)?, r);
    }
    require(
        by_reference.len() == accepted.len(),
        format!("step {si}: duplicate accepted reference"),
    )?;
    let mut cursor = Q::new();
    let mut found = vec![];
    for (ri, row) in array(rs)?.iter().enumerate() {
        let where_ = format!("step {si} row {ri}");
        let (lo, hi) = point(get(row, "interval")?)?;
        require(
            lo == cursor,
            format!(
                "{where_}: interval {}",
                if lo > cursor { "gap" } else { "overlap" }
            ),
        )?;
        require(
            lo < hi && hi <= 1,
            format!("{where_}: interval is empty or ends past 1"),
        )?;
        cursor.clone_from(&hi);
        let prior = by_reference.get(&reference_key(get(row, "prior_reference")?)?);
        require(
            prior.is_some(),
            format!("{where_}: prior reference is not an accepted row"),
        )?;
        let prior = prior.ok_or_else(|| malformed("missing predecessor"))?;
        require(
            prior.interval.0 <= lo && hi <= prior.interval.1,
            format!("{where_}: interval escapes its predecessor"),
        )?;
        found.push((*prior).clone());
    }
    require(
        cursor == 1,
        format!("step {si}: the rows do not reach the end of the interval"),
    )?;
    Ok(found)
}
struct Prepared {
    row: Row,
    core: Poly,
    required: Poly,
    planes: Vec<Plane>,
    live: bool,
}
#[expect(
    clippy::many_single_char_names,
    reason = "Coordinate and polynomial symbols match the exact geometric formulas."
)]
fn prepare_row(
    state: &State,
    row: &Value,
    prior: &Row,
    si: usize,
    ri: usize,
    owner: usize,
    node_id: &Value,
) -> Result<Prepared> {
    let where_ = format!("step {si} row {ri}");
    let interval = point(get(row, "interval")?)?;
    let (lo, hi) = &interval;
    let reference = get(row, "reference")?;
    require(
        eq(
            reference,
            &json!({"kind":"phase3","node":node_id,"step":si,"row":ri}),
        ),
        format!("{where_}: reference"),
    )?;
    require(
        row.get("self_hull_cuts").is_none_or(empty),
        format!("{where_}: self-hull cuts"),
    )?;
    let required = if prior.outer.is_empty() {
        vec![]
    } else {
        intersect_convex(&prior.outer, &wall_box(lo, hi, &state.cap))?
    };
    let residual = polies(get(row, "residual_polygons")?, true)?;
    let vertices: Vec<&Point> = residual.iter().flatten().collect();
    if required.is_empty() {
        require(
            residual.is_empty()
                && empty(get(row, "collision_regions")?)
                && empty(get(row, "common_core_halfplanes")?)
                && empty(get(row, "outer_bounds")?)
                && empty(get(row, "outer_domain")?),
            format!("{where_}: a dead row carries data"),
        )?;
        return Ok(Prepared {
            row: Row::new(interval, reference.clone(), vec![], vec![]),
            core: vec![],
            required,
            planes: vec![],
            live: false,
        });
    }
    let core = hull(&poly(get(row, "core_vertices")?)?);
    require(
        core.len() >= 3 && area2(&core) > 0,
        format!("{where_}: degenerate core"),
    )?;
    require(
        core_strict(&core, lo, hi),
        format!("{where_}: core not strict"),
    )?;
    let mut common = vec![];
    if !vertices.is_empty() {
        for k in 0..core.len() {
            let p = &core[k];
            let q = &core[(k + 1) % core.len()];
            let a = q.1.clone() - &p.1;
            let b = p.0.clone() - &q.0;
            let least = vertices
                .iter()
                .map(|v| dot(&a, &b, v))
                .min()
                .ok_or_else(|| malformed("missing residual vertex"))?;
            let c = dot(&a, &b, p) + least;
            common.push((a, b, c));
        }
    }
    let published = planes(get(row, "common_core_halfplanes")?)?;
    require(
        published.iter().collect::<BTreeSet<_>>() == common.iter().collect(),
        format!("{where_}: common-core planes"),
    )?;
    let bounds = planes(get(row, "outer_bounds")?)?;
    let live = !vertices.is_empty();
    let outer = if live {
        require(bounds.len() == 8, format!("{where_}: outer bounds"))?;
        for (a, b, c) in &bounds {
            require(
                vertices.iter().all(|v| dot(a, b, v) <= *c),
                format!("{where_}: bound"),
            )?;
        }
        let mut outer = state
            .cells
            .get(owner)
            .ok_or_else(|| malformed("owner cell index"))?
            .clone();
        for (a, b, c) in bounds {
            outer = clip_closed(&outer, &a, &b, &c);
        }
        outer = hull(&outer);
        require(
            same_set(&poly(get(row, "outer_domain")?)?, &outer),
            format!("{where_}: outer domain"),
        )?;
        outer
    } else {
        require(
            bounds.is_empty() && empty(get(row, "outer_domain")?),
            format!("{where_}: dead bounds"),
        )?;
        vec![]
    };
    Ok(Prepared {
        row: Row::new(interval, reference.clone(), outer, residual),
        core,
        required,
        planes: common,
        live,
    })
}
#[derive(Clone, Copy)]
struct FullRow<'a> {
    raw: &'a Value,
    prepared: &'a Prepared,
    si: usize,
    ri: usize,
    owner: usize,
}
#[expect(
    clippy::similar_names,
    reason = "Replay state and separately accumulated stats have distinct roles."
)]
fn full_row(
    state: &State,
    memos: &mut Memos,
    stats: &mut Stats,
    partners: &mut BTreeMap<usize, Vec<CoverRow>>,
    job: FullRow<'_>,
) -> Result<()> {
    let FullRow {
        raw,
        prepared: p,
        si,
        ri,
        owner,
    } = job;
    tick(stats, "rows_full", 1);
    let where_ = format!("step {si} row {ri}");
    let collisions = check_collisions(memos, stats, raw, &where_, &p.core, &p.required, partners)?;
    check_cover(
        state,
        memos,
        stats,
        CoverCheck {
            owner,
            where_: &where_,
            core: &p.core,
            required: &p.required,
            collisions,
            residual: &p.row.residual,
        },
    )
}
/// Replay one step and return its admitted rows and supporting geometry.
#[expect(
    clippy::similar_names,
    reason = "Replay state and separately accumulated stats have distinct roles."
)]
pub fn check_step(
    state: &mut State,
    step: &Value,
    si: usize,
    node_id: &Value,
    full: &BTreeSet<usize>,
    pool: Option<&rayon::ThreadPool>,
) -> Result<(Vec<Row>, Vec<Plane>, bool)> {
    let owner = index(get(step, "owner")?)?;
    let mut partners = check_partners(state, step, si)?;
    let rs = get(step, "rows")?;
    let cited = predecessors(rows(state, owner)?, rs, si)?;
    let raw = array(rs)?;
    let mut prepared = vec![];
    let mut pending = None;
    let mut memos = std::mem::take(&mut state.memos);
    let mut stats = std::mem::take(&mut state.stats);
    for (ri, (row, prior)) in raw.iter().zip(&cited).enumerate() {
        match prepare_row(state, row, prior, si, ri, owner, node_id) {
            Ok(p) => {
                if pool.is_none() && full.contains(&ri) && !p.required.is_empty() {
                    full_row(
                        state,
                        &mut memos,
                        &mut stats,
                        &mut partners,
                        FullRow {
                            raw: row,
                            prepared: &p,
                            si,
                            ri,
                            owner,
                        },
                    )?;
                }
                prepared.push(p);
            }
            Err(e) => {
                pending = Some(e);
                break;
            }
        }
    }
    if let Some(pool) = pool {
        let jobs: Vec<_> = prepared
            .iter()
            .enumerate()
            .filter(|(ri, p)| full.contains(ri) && !p.required.is_empty())
            .collect();
        let results: Vec<Result<Stats>> = pool.install(|| {
            jobs.par_iter()
                .map(|&(ri, p)| {
                    let mut cache = Memos::default();
                    let mut counters = Stats::new();
                    let mut covers = partners.clone();
                    full_row(
                        state,
                        &mut cache,
                        &mut counters,
                        &mut covers,
                        FullRow {
                            raw: &raw[ri],
                            prepared: p,
                            si,
                            ri,
                            owner,
                        },
                    )?;
                    Ok(counters)
                })
                .collect()
        });
        for result in results {
            for (k, v) in result? {
                *stats.entry(k).or_default() += v;
            }
        }
    }
    if let Some(e) = pending {
        return Err(e);
    }
    if pool.is_none() {
        for (pj, covers) in partners {
            let mut live = covers.into_iter();
            for row in state
                .rows
                .get_mut(&pj)
                .ok_or_else(|| malformed("unknown partner"))?
            {
                if row.residual.iter().any(|p| !p.is_empty()) {
                    row.cover = live.next();
                }
            }
        }
    }
    state.memos = memos;
    state.stats = stats;
    let mut new_rows = vec![];
    let mut all_planes = vec![];
    let mut any_live = false;
    for p in prepared {
        new_rows.push(p.row);
        all_planes.extend(p.planes);
        any_live |= p.live;
    }
    Ok((new_rows, all_planes, any_live))
}
/// Apply an admitted step to owner state and validate row compression.
pub fn compress(
    state: &mut State,
    step: &Value,
    si: usize,
    planes: &[Plane],
    any_live: bool,
) -> Result<()> {
    let owner = index(get(step, "owner")?)?;
    let kernel = poly(get(step, "common_owned_kernel")?)?;
    for pt in &kernel {
        require(
            pt.0 >= 0 && pt.0 <= state.cap && pt.1 >= 0 && pt.1 <= state.cap,
            format!("step {si}: kernel"),
        )?;
        require(
            planes.iter().all(|(a, b, c)| dot(a, b, pt) <= *c),
            format!("step {si}: kernel point fails a plane"),
        )?;
    }
    if !(any_live && (!group(state, owner)?.is_empty() || !kernel.is_empty())) {
        require(
            step.get("inner_grid_compression").is_none(),
            format!("step {si}: unexpected compression"),
        )?;
        return Ok(());
    }
    let mut original = group(state, owner)?.clone();
    original.extend(kernel);
    let original = hull(&original);
    require(
        same_set(&poly(get(step, "compression_source_hull")?)?, &original),
        format!("step {si}: source"),
    )?;
    let record = get(step, "inner_grid_compression")?;
    let points = poly(get(record, "vertices")?)?;
    let witness_value = get(record, "witnesses")?;
    require(
        points.len() == pylen(witness_value)? && pylen(witness_value)? > 0,
        format!("step {si}: witnesses"),
    )?;
    let witnesses = iterable(witness_value)?;
    for (pt, witness) in points.iter().zip(&witnesses) {
        let indices = iterable(get(witness, "indices")?)?;
        let weights = iterable(get(witness, "weights")?)?
            .iter()
            .map(|v| q(v))
            .collect::<Result<Vec<_>>>()?;
        let mut valid = (1..=3).contains(&indices.len());
        if valid {
            for k in &indices {
                let n = numeric(k)?;
                if n < 0 || n >= original.len() {
                    valid = false;
                    break;
                }
            }
        }
        require(
            valid
                && weights.iter().all(|x| x >= &Q::new())
                && weights.iter().cloned().sum::<Q>() == 1,
            format!("step {si}: witness weights"),
        )?;
        if indices.len() != weights.len() {
            return Err(malformed("witness zip length mismatch"));
        }
        let mut combined = (Q::new(), Q::new());
        for (k, x) in indices.iter().zip(weights) {
            let p = original
                .get(index(k)?)
                .ok_or_else(|| malformed("witness index out of range"))?;
            combined.0 += x.clone() * &p.0;
            combined.1 += x * &p.1;
        }
        require(
            combined == *pt && *pt == point(get(witness, "point")?)?,
            format!("step {si}: witness point"),
        )?;
        require(
            (pt.0.clone() * 1_048_576i32).is_integer()
                && (pt.1.clone() * 1_048_576i32).is_integer(),
            format!("step {si}: off the grid"),
        )?;
    }
    let next = if record.get("mode").is_some_and(|m| eq(m, &json!("replace"))) {
        hull(&points)
    } else {
        let mut p = group(state, owner)?.clone();
        p.extend(points);
        hull(&p)
    };
    state.groups.insert(owner, next);
    require(
        group(state, owner)?.len() <= 16,
        format!("step {si}: owned hull too large"),
    )
}
/// Derive an optional owner closure from replayed empty residuals.
pub fn derive_closure(state: &State, owner: usize, si: usize) -> Result<Option<Value>> {
    if !rows(state, owner)?.iter().any(|r| !r.residual.is_empty()) {
        return Ok(Some(
            json!({"kind":"all_parent_poses_forbidden","owner":owner,"step":si}),
        ));
    }
    let mut mask = state.mask.clone();
    mask.sort_unstable();
    for oj in mask {
        if oj != owner && !group(state, oj)?.is_empty() && !group(state, owner)?.is_empty() {
            let common = if group(state, oj)?.len() >= 3 {
                intersect_convex(group(state, owner)?, group(state, oj)?)?
            } else {
                vec![]
            };
            if !common.is_empty() {
                let mut owners = vec![owner, oj];
                owners.sort_unstable();
                return Ok(Some(
                    json!({"kind":"owned_hulls_intersect","owners":owners,"step":si}),
                ));
            }
        }
    }
    Ok(None)
}
/// Validate declared final state against replayed rows and closure.
pub fn check_final(state: &State, node: &Value, stall: bool) -> Result<()> {
    let final_ = get(node, "final_state")?;
    for &o in &state.mask {
        let name = state.owner_name(o)?;
        require(
            same_set(
                &poly(get(get(final_, "groups")?, &name)?)?,
                group(state, o)?,
            ),
            format!("final group {name}"),
        )?;
        let recorded = get(get(final_, "cells")?, &name)?;
        let rs = rows(state, o)?;
        require(pylen(recorded)? == rs.len(), format!("final rows {name}"))?;
        let recorded = iterable(recorded)?;
        for (recorded, r) in recorded.iter().zip(rs) {
            require(
                eq(get(recorded, "reference")?, &r.reference),
                format!("final reference {name}"),
            )?;
            require(
                if r.outer.is_empty() {
                    empty(get(recorded, "outer_domain")?)
                } else {
                    same_set(&poly(get(recorded, "outer_domain")?)?, &r.outer)
                },
                format!("final outer domain {name}"),
            )?;
            let residual = get(recorded, "residual_polygons")?;
            let mut matches = pylen(residual)? == r.residual.len();
            if matches {
                let residual = iterable(residual)?;
                for (a, b) in residual.iter().zip(&r.residual) {
                    if !same_set(&poly(a)?, b) {
                        matches = false;
                        break;
                    }
                }
            }
            require(matches, format!("final residual {name}"))?;
        }
    }
    require(
        get(node, "closed")?.as_bool() == Some(!stall)
            && get(node, "terminal")?.as_bool() == Some(!stall),
        "closed flags",
    )?;
    require(
        get(node, "mask_exclusion_proved")?.as_bool() == Some(false)
            && get(node, "global_optimality_proved")?.as_bool() == Some(false),
        "the node claims more than a closure",
    )
}
/// Retire stale group caches and cap retained facet entries.
pub fn bound_memos(state: &mut State, owner: usize, before: &[Point]) -> Result<()> {
    if group(state, owner)? != before {
        state.memos.forbidden.retain(|(g, _), _| g != before);
    }
    if state.memos.facets.len() > (1 << 15) {
        state.memos.facets.clear();
    }
    Ok(())
}
#[derive(Clone)]
/// Verification controls; sampled runs are diagnostic and do not certify full closure.
pub struct Options {
    /// Optional diagnostic sample count; None replays every object.
    pub sample: Option<Integer>,
    /// Python-compatible deterministic sampling seed.
    pub sample_seed: Integer,
    /// Whether to emit progress diagnostics during replay.
    pub progress: bool,
    /// Positive worker count; receipt objects retain their selected order.
    pub threads: usize,
}
impl Default for Options {
    fn default() -> Self {
        Self {
            sample: None,
            sample_seed: Integer::from(12345),
            progress: false,
            threads: 1,
        }
    }
}
fn int_json(n: &Integer) -> Result<Value> {
    crate::value::from_str(&n.to_string())
}
/// Verify selected object pairs and construct deterministic per-object receipt entries.
pub fn verify_objects(directory: &str, cells: &Cells, opt: &Options) -> Result<Value> {
    let mut seeds = vec![];
    let mut nodes = vec![];
    // pathlib.glob on a missing/non-directory path returns no matches.
    match std::fs::read_dir(directory) {
        Ok(entries) => {
            for entry in entries {
                let path = entry?.path();
                if let Some(n) = path.file_name().and_then(|s| s.to_str()) {
                    if n.starts_with("seed-") && n.ends_with(".json.gz") {
                        seeds.push(path.clone());
                    }
                    if n.starts_with("node-") && n.ends_with(".json.gz") {
                        nodes.push(path);
                    }
                }
            }
        }
        Err(e)
            if e.kind() == std::io::ErrorKind::NotFound
                || e.kind() == std::io::ErrorKind::NotADirectory => {}
        Err(e) => return Err(e.into()),
    }
    seeds.sort();
    nodes.sort();
    require(
        seeds.len() == 1 && nodes.len() == 1,
        "the directory must hold one seed and one node",
    )?;
    let (seed, seed_sha) = load_object(&seeds[0])?;
    let mut stream = NodeStream::new(&nodes[0])?;
    let node = &stream.header;
    require(
        eq(get(get(node, "source")?, "sha256")?, &json!(seed_sha)),
        "the node's source is not the seed",
    )?;
    let mask = check_frame(&seed, node, cells)?;
    let bins = get(&seed, "bins")?;
    require(is_int(bins) && int_value(bins)? > 0, "bins")?;
    let mut state = State::new(
        cells,
        int_value(bins)?,
        mask,
        array(get(&seed, "mask")?)?.clone(),
    );
    let clock = Instant::now();
    check_seed(&mut state, &seed, node)?;
    let contradiction = get(node, "contradiction")?.clone();
    let stall = contradiction.is_null();
    let closure_step = if stall {
        json!(-1)
    } else {
        get(&contradiction, "step")?.clone()
    };
    let node_id = get(node, "node_id")?.clone();
    let mut rng = Random::new(&opt.sample_seed);
    let mut derived = None;
    let mut si = 0;
    let pool = if opt.threads > 1 {
        Some(
            rayon::ThreadPoolBuilder::new()
                .num_threads(opt.threads)
                .build()
                .map_err(|e| malformed(e.to_string()))?,
        )
    } else {
        None
    };
    stream.steps()?;
    while let Some(step) = stream.next_step()? {
        let owner_value = get(&step, "owner")?;
        require(
            eq(get(&step, "index")?, &json!(si))
                && state.mask_values.iter().any(|o| eq(o, owner_value))
                && get(&step, "complete")?.as_bool() == Some(true),
            format!("step {si}: header"),
        )?;
        require(
            eq(get(&step, "allowed_half_angle")?, &json!(["0", "1"])),
            format!("step {si}: allowed half-angle"),
        )?;
        let owner = index(owner_value)?;
        for &o in &state.mask {
            let name = state.owner_name(o)?;
            require(
                same_set(
                    &poly(get(get(&step, "prior_owned_hulls")?, &name)?)?,
                    group(&state, o)?,
                ),
                format!("step {si}: prior hull {name}"),
            )?;
        }
        let count = pylen(get(&step, "rows")?)?;
        let full: BTreeSet<_> = if opt.sample.is_none() || eq(&json!(si), &closure_step) {
            (0..count).collect()
        } else {
            let sample = opt
                .sample
                .as_ref()
                .ok_or_else(|| malformed("missing sample"))?;
            if sample < &Integer::from(0) {
                return Err(malformed("sample larger than population or negative"));
            }
            let k = sample
                .clone()
                .min(Integer::from(count))
                .to_usize()
                .ok_or_else(|| malformed("sample size"))?;
            rng.sample(count, k)?.into_iter().collect()
        };
        let before = group(&state, owner)?.clone();
        let (new_rows, planes, any_live) =
            check_step(&mut state, &step, si, &node_id, &full, pool.as_ref())?;
        compress(&mut state, &step, si, &planes, any_live)?;
        state.rows.insert(owner, new_rows);
        bound_memos(&mut state, owner, &before)?;
        state.tick("steps", 1);
        derived = derive_closure(&state, owner, si)?;
        if opt.progress {
            let live = rows(&state, owner)?
                .iter()
                .filter(|r| !r.residual.is_empty())
                .count();
            let progress = json!({"step":si,"owner":owner_value,"live_rows":live,"rows_checked_in_full":full.len(),"closure":derived.is_some(),"seconds":pyjson::round_float(clock.elapsed().as_secs_f64(),1)?});
            println!("{}", pyjson::compact(&progress)?);
            std::io::stdout().flush()?;
        }
        if let Some(d) = &derived {
            let mut matches = eq(&json!(si), &closure_step);
            if matches {
                matches = eq(get(d, "kind")?, get(&contradiction, "kind")?)
                    && eq(
                        d.get("owner").unwrap_or(&Value::Null),
                        contradiction.get("owner").unwrap_or(&Value::Null),
                    );
            }
            require(
                matches,
                format!("step {si}: the derived closure is not the declared one"),
            )?;
            require(stream.next_step()?.is_none(), "steps after the closure")?;
            break;
        }
        si += 1;
    }
    if derived.is_none() {
        require(stall, "no closure derived")?;
    }
    require(stream.sha256.is_some(), "the node was not read to its end")?;
    check_final(&state, &stream.header, stall)?;
    let mut counts = crate::value::Map::new();
    for (k, v) in &state.stats {
        counts.insert(k.clone().into(), int_json(v)?);
    }
    Ok(
        json!({"certificate":{"seed_sha256":seed_sha,"node_sha256":stream.sha256},"mask":state.mask_values,"cells":state.mask.iter().map(|&k|cells.names[k].clone()).collect::<Vec<_>>(),"bins":bins,"closure":contradiction,"closed":!stall,"counts":counts}),
    )
}
/// Construct a versioned receipt, preserving verification failure as a FAIL result.
pub fn verify(directory: &str, cells: &Cells, opt: &Options) -> Result<Value> {
    let clock = Instant::now();
    let mut receipt = json!({"schema":"n17-certificate-verification/v1","verifier":"kernel","provenance":{"implementation":"rust","crate":"n17-kernel-verifier","version":env!("CARGO_PKG_VERSION"),"source_sha256":env!("SOURCE_SHA256")},"directory":directory,"cells_source":cells.source,"mode":if opt.sample.is_none(){"full"}else{"sample"},"sample_rows_per_step":opt.sample.as_ref().map(int_json).transpose()?,"sample_seed":if opt.sample.is_some(){int_json(&opt.sample_seed)?}else{Value::Null}});
    let obj = receipt
        .as_object_mut()
        .ok_or_else(|| malformed("receipt object"))?;
    match verify_objects(directory, cells, opt) {
        Err(e) => {
            obj.insert("status".into(), json!("FAIL"));
            obj.insert("failure".into(), e.receipt_value());
        }
        Ok(result) => {
            let closed = get(&result, "closed")?.as_bool() == Some(true);
            for (k, v) in object(&result)? {
                obj.insert(k.clone(), v.clone());
            }
            obj.insert("status".into(), json!(if closed { "PASS" } else { "FAIL" }));
            obj.insert(
                "failure".into(),
                if closed {
                    Value::Null
                } else {
                    json!("the node is a stall, not a closure")
                },
            );
        }
    }
    obj.insert(
        "seconds".into(),
        json!(pyjson::round_float(clock.elapsed().as_secs_f64(), 3)?),
    );
    Ok(receipt)
}
/// Atomically replace the receipt after writing its complete Python-compatible JSON.
///
/// Staging is in the destination directory. This promises atomic visibility, not
/// crash durability or preservation of destination metadata; a symlink is replaced.
pub fn write_receipt(path: &Path, receipt: &Value) -> Result<()> {
    write_receipt_with(
        path,
        receipt,
        std::io::Write::write_all,
        |staged, destination| staged.persist(destination),
    )
}

// Injection seams exercise partial writes and the rename boundary through the same
// staging and cleanup path used by the CLI, without process-global fault switches.
pub(crate) fn write_receipt_with(
    path: &Path,
    receipt: &Value,
    write: impl FnOnce(&mut std::fs::File, &[u8]) -> std::io::Result<()>,
    publish: impl FnOnce(
        tempfile::TempPath,
        &Path,
    ) -> std::result::Result<(), tempfile::PathPersistError>,
) -> Result<()> {
    use std::io::Write;
    let bytes = pyjson::pretty(receipt)?;
    let directory = path
        .parent()
        .filter(|parent| !parent.as_os_str().is_empty())
        .unwrap_or_else(|| Path::new("."));
    std::fs::create_dir_all(directory)?;
    let mut staged = tempfile::NamedTempFile::new_in(directory)?;
    if let Err(error) =
        write(staged.as_file_mut(), bytes.as_bytes()).and_then(|()| staged.as_file_mut().flush())
    {
        return receipt_publication_error(path, &error, staged.into_temp_path());
    }
    // Close the staged file before replacing, including on Windows.
    match publish(staged.into_temp_path(), path) {
        Ok(()) => Ok(()),
        Err(error) => receipt_publication_error(path, &error.error, error.path),
    }
}

fn receipt_publication_error(
    path: &Path,
    error: &std::io::Error,
    staged: tempfile::TempPath,
) -> Result<()> {
    let context = format!("cannot publish receipt {}: {error}", path.display());
    let staging_path = staged.display().to_string();
    match staged.close() {
        Ok(()) => Err(malformed(context)),
        Err(cleanup) => Err(malformed(format!(
            "{context}; staging cleanup failed at {staging_path}: {cleanup}"
        ))),
    }
}
