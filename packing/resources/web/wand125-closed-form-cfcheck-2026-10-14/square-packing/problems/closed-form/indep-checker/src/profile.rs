//! Opt-in, thread-local diagnostics; counters never participate in decisions.
use crate::rat::Q;
use std::{
    cell::RefCell,
    collections::{BTreeMap, BTreeSet},
    time::Instant,
};
#[derive(Default, serde::Serialize)]
pub struct Stats {
    pub local_segments: usize,
    pub planes_before: usize,
    pub planes_after: usize,
    pub nonzero_triples: usize,
    pub prove_calls: usize,
    pub sturm_sequences: usize,
    pub max_degree: usize,
    pub max_coefficient_bits: u64,
    pub stages: BTreeMap<String, f64>,
    #[serde(skip)]
    pub guards: BTreeSet<Vec<num_bigint::BigInt>>,
    pub distinct_guards: usize,
}
thread_local! { static STATS: RefCell<Option<Stats>> = const { RefCell::new(None) }; }
pub fn begin() {
    STATS.with(|s| *s.borrow_mut() = Some(Stats::default()));
}
pub fn update(f: impl FnOnce(&mut Stats)) {
    STATS.with(|s| {
        if let Some(s) = s.borrow_mut().as_mut() {
            f(s);
        }
    });
}
pub fn finish() -> Stats {
    STATS.with(|s| {
        let mut v = s.borrow_mut().take().unwrap();
        v.distinct_guards = v.guards.len();
        v
    })
}
pub fn polynomial(c: &[Q]) {
    update(|s| {
        s.max_degree = s.max_degree.max(c.len().saturating_sub(1));
        for q in c {
            s.max_coefficient_bits = s
                .max_coefficient_bits
                .max(q.numer().bits())
                .max(q.denom().bits());
        }
    });
}
pub struct Stage(&'static str, Instant);
pub fn stage(name: &'static str) -> Stage {
    Stage(name, Instant::now())
}
impl Drop for Stage {
    fn drop(&mut self) {
        update(|s| *s.stages.entry(self.0.into()).or_default() += self.1.elapsed().as_secs_f64());
    }
}
