use crate::{
    family::Family,
    parse_error,
    rat::{array, int, midpoint, value, Q},
    refuse,
    report::Report,
    require, Result,
};
use num_traits::Zero;
use rayon::prelude::*;
use serde_json::Value;
use sha2::{Digest, Sha256};
use std::{
    collections::{BTreeMap, BTreeSet},
    fs::File,
    io::{BufRead, BufReader},
    path::Path,
    time::{Duration, Instant},
};
pub type Box4 = [Q; 8];
pub const KINDS: [&str; 24] = [
    "EMPTY",
    "CORE",
    "B3D",
    "EDGE",
    "EX:CORE",
    "EX:B3D",
    "EY:CORE",
    "EY:B3D",
    "B3U:x",
    "B3U:y",
    "B3U:xy",
    "B3U:xyh",
    "B3T:x",
    "B3T:y",
    "CORE1:P",
    "CORE1:x",
    "CORE1:y",
    "CORE1:xy",
    "CORE1:xyh",
    "CORE1:Tx",
    "CORE1:Ty",
    "CORE1:TxHy",
    "CORE1:TyHx",
    "B4U",
];
#[derive(Clone)]
pub struct Leaf {
    pub bounds: Box4,
    pub kind: String,
}
pub struct Root {
    pub bounds: Box4,
    pub leaves: Vec<Leaf>,
    pub line: usize,
}
pub fn parse_box(v: &Value) -> Result<Box4> {
    let v = array(v, 8)?;
    let b: Box4 = v.try_into().unwrap();
    validate_box(&b)?;
    Ok(b)
}
pub fn validate_box(b: &Box4) -> Result<()> {
    for i in [0, 2, 4, 6] {
        require(b[i] < b[i + 1], "non-positive box width")?;
    }
    require(
        b[4] > -int(1) && b[5] < int(1),
        "u outside specified |u|<1 range",
    )
}
pub fn parse_root(v: &Value, line: usize) -> Result<Option<Root>> {
    require(v.is_object(), "record line must be an object")?;
    if v.get("header").is_some() {
        return Ok(None);
    }
    for key in ["uncert", "f3d"] {
        let a = v[key]
            .as_array()
            .ok_or_else(|| parse_error(format!("missing {key} array")))?;
        require(a.is_empty(), format!("{key} must be empty"))?;
    }
    let bounds = parse_box(&v["root"])?;
    require(
        !(bounds[4] < Q::zero() && bounds[5] > Q::zero()),
        "root crosses u=0",
    )?;
    let mut leaves = vec![];
    for row in v["leaves"]
        .as_array()
        .ok_or_else(|| parse_error("missing leaves array"))?
    {
        let a = row
            .as_array()
            .ok_or_else(|| parse_error("leaf must be array"))?;
        if a.len() != 2 {
            return Err(parse_error("leaf must have exactly two entries"));
        }
        let bounds = parse_box(&a[0])?;
        let kind = a[1]
            .as_str()
            .ok_or_else(|| parse_error("kind must be string"))?
            .to_owned();
        require(
            KINDS.contains(&kind.as_str()),
            format!("unknown kind {kind}"),
        )?;
        leaves.push(Leaf { bounds, kind });
    }
    Ok(Some(Root {
        bounds,
        leaves,
        line,
    }))
}
pub fn tiling(root: &Box4, leaves: &[Box4]) -> bool {
    if leaves.is_empty() {
        return false;
    }
    for b in leaves {
        for i in [0, 2, 4, 6] {
            if b[i] < root[i] || b[i + 1] > root[i + 1] || b[i] >= b[i + 1] {
                return false;
            }
        }
    }
    let mut stack = vec![(root.clone(), (0..leaves.len()).collect::<Vec<_>>())];
    while let Some((b, indices)) = stack.pop() {
        if indices.len() == 1 {
            if leaves[indices[0]] != b {
                return false;
            }
            continue;
        }
        let mut split = None;
        for axis in [4, 6, 0, 2] {
            let m = midpoint(&b[axis], &b[axis + 1]);
            let mut left = vec![];
            let mut right = vec![];
            let mut crossing = false;
            for &idx in &indices {
                let l = &leaves[idx];
                if l[axis + 1] <= m {
                    left.push(idx);
                } else if l[axis] >= m {
                    right.push(idx);
                } else {
                    crossing = true;
                    break;
                }
            }
            if !crossing && !left.is_empty() && !right.is_empty() {
                let (mut lo, mut hi) = (b.clone(), b.clone());
                lo[axis + 1] = m.clone();
                hi[axis] = m;
                split = Some(((lo, left), (hi, right)));
                break;
            }
        }
        if let Some((a, b)) = split {
            stack.push(b);
            stack.push(a);
        } else {
            return false;
        }
    }
    true
}
#[derive(Default)]
pub struct Domain {
    roots: BTreeSet<Box4>,
    axes: [BTreeSet<(Q, Q)>; 4],
    pub duplicate: bool,
}
impl Domain {
    pub fn insert(&mut self, b: &Box4) {
        if !self.roots.insert(b.clone()) {
            self.duplicate = true;
        }
        for i in 0..4 {
            self.axes[i].insert((b[2 * i].clone(), b[2 * i + 1].clone()));
        }
    }
    pub fn check(&self, bounds: &[Q; 4], d0: &Q, d1: &Q) -> Result<()> {
        require(!self.duplicate, "duplicate root")?;
        require(!self.roots.is_empty(), "empty record")?;
        let mut count = 1usize;
        for i in 0..4 {
            let ax = &self.axes[i];
            count = count
                .checked_mul(ax.len())
                .ok_or_else(|| refuse("root product overflow"))?;
            let mut end = None;
            for (lo, hi) in ax {
                require(lo < hi, "root axis has non-positive width")?;
                if let Some(e) = end {
                    require(e == lo, "root axis gap or interior overlap")?;
                }
                end = Some(hi);
            }
            let (lo, hi) = (&ax.first().unwrap().0, &ax.last().unwrap().1);
            match i {
                0 => require(
                    lo == &bounds[0] && hi == &bounds[1],
                    "x root bounds mismatch",
                )?,
                1 => require(
                    lo == &bounds[2] && hi == &bounds[3],
                    "y root bounds mismatch",
                )?,
                2 => {
                    require(
                        lo < &Q::zero() && hi > &Q::zero() && lo > &-int(1) && hi < &int(1),
                        "invalid angular endpoints",
                    )?;
                    require(
                        -lo + hi - lo * hi >= int(1),
                        "angular coverage is less than 90 degrees",
                    )?;
                }
                3 => require(lo == d0 && hi == d1, "delta root bounds mismatch")?,
                _ => unreachable!(),
            };
        }
        require(
            count == self.roots.len(),
            "root set is not the full Cartesian product",
        )
    }
}
pub fn run(
    family_path: &Path,
    record: &Path,
    bounds: [Q; 4],
    threads: usize,
    chunk_leaves: usize,
    max_roots: Option<usize>,
    progress: bool,
    only_kinds: Option<&BTreeSet<String>>,
    max_per_kind: Option<usize>,
    progress_file: Option<&Path>,
    resume: bool,
    report: &mut Report,
) -> Result<()> {
    require(chunk_leaves > 0, "chunk leaf count must be positive")?;
    let family = Family::parse(report.read_json(family_path)?)?;
    let mut checkpoint = progress_file
        .map(|path| {
            crate::checkpoint::Checkpoint::open(
                path,
                record,
                &report.inputs.last().unwrap().sha256,
                resume,
            )
        })
        .transpose()?;
    if let (Some(path), Some(cp)) = (progress_file, &checkpoint) {
        report.add_hash(path, cp.input_hash.clone());
    }
    let file = File::open(record)?;
    let pool = rayon::ThreadPoolBuilder::new()
        .num_threads(threads)
        .build()
        .map_err(|e| parse_error(e.to_string()))?;
    let family = std::sync::Arc::new(family);
    let mut display = ProgressDisplay::new(progress);
    let mut timing: BTreeMap<String, (u64, f64)> = BTreeMap::new();
    let mut checked_roots = 0;
    let mut selected: BTreeMap<String, usize> = BTreeMap::new();
    let mut halted = false;
    let mut root_count = 0;
    let mut accepted_roots = 0;
    let mut domain = Domain::default();
    let capacity = threads.saturating_mul(4).max(1);
    let window = threads.saturating_mul(8).max(1);
    let mut pending = std::collections::VecDeque::new();
    let mut committed_roots = 0;
    let mut committed_leaves = 0;
    let record_hash = std::thread::scope(|scope| -> Result<String> {
        // Reserve one channel slot for the producer's currently parsed row.
        let (send, receive) = std::sync::mpsc::sync_channel(capacity - 1);
        scope.spawn(move || {
            let result = produce(file, &send);
            let _ = send.send(Parsed::End(result));
        });
        // Dropping the receiver on error releases a blocked producer before scope joins.
        let receive = receive;
        loop {
            while !pending.is_empty() {
                let wait = pending.len() >= window;
                if !commit_front(
                    &mut pending,
                    wait,
                    &mut timing,
                    &mut checkpoint,
                    report,
                    &mut accepted_roots,
                    &mut committed_roots,
                    &mut committed_leaves,
                )? {
                    break;
                }
                halted |= !report.ok;
                display.tick(committed_roots, committed_leaves, pending.len());
            }
            if let Some(cp) = &mut checkpoint {
                cp.sync_due()?;
            }
            display.tick(committed_roots, committed_leaves, pending.len());
            if pending.len() >= window {
                continue;
            }
            let parsed = match receive.recv_timeout(Duration::from_millis(200)) {
                Ok(v) => v,
                Err(std::sync::mpsc::RecvTimeoutError::Timeout) => continue,
                Err(_) => return Err(refuse("record producer disconnected")),
            };
            let (root, hash, tiled) = match parsed {
                Parsed::End(result) => {
                    while !pending.is_empty() {
                        commit_front(
                            &mut pending,
                            true,
                            &mut timing,
                            &mut checkpoint,
                            report,
                            &mut accepted_roots,
                            &mut committed_roots,
                            &mut committed_leaves,
                        )?;
                        if let Some(cp) = &mut checkpoint {
                            cp.sync_due()?;
                        }
                        display.tick(committed_roots, committed_leaves, pending.len());
                    }
                    return result;
                }
                Parsed::Row {
                    line,
                    hash,
                    root: Err(e),
                    ..
                } => {
                    // Structural failures also commit behind earlier root receipts.
                    while !pending.is_empty() {
                        commit_front(
                            &mut pending,
                            true,
                            &mut timing,
                            &mut checkpoint,
                            report,
                            &mut accepted_roots,
                            &mut committed_roots,
                            &mut committed_leaves,
                        )?;
                        if let Some(cp) = &mut checkpoint {
                            cp.sync_due()?;
                        }
                        display.tick(committed_roots, committed_leaves, pending.len());
                    }
                    if let Some(cp) = &mut checkpoint {
                        cp.failure(line, &hash, &e.reason, false)?;
                    }
                    report.error(format!("line {line}"), e);
                    continue;
                }
                Parsed::Row { root: Ok(None), .. } => continue,
                Parsed::Row {
                    hash,
                    root: Ok(Some(root)),
                    tiled,
                    ..
                } => (root, hash, tiled),
            };
            domain.insert(&root.bounds);
            report.roots += 1;
            root_count += 1;
            for l in &root.leaves {
                report.leaves += 1;
                *report.leaf_kinds.entry(l.kind.clone()).or_default() += 1;
            }
            let resumed = checkpoint
                .as_ref()
                .map(|cp| cp.resumed(root.line, &hash))
                .transpose()?
                .flatten()
                .cloned();
            let kinds = crate::checkpoint::counts(&root);
            let leaf_count = root.leaves.len();
            let eligible = resumed.is_none()
                && max_roots.is_none_or(|n| root_count <= n)
                && !crate::budget::expired()
                && !halted;
            let selected_leaves = if eligible {
                checked_roots += 1;
                root.leaves
                    .into_iter()
                    .enumerate()
                    .filter(|(_, l)| {
                        if only_kinds.is_some_and(|ks| !ks.contains(&l.kind)) {
                            return false;
                        }
                        let n = selected.entry(l.kind.clone()).or_default();
                        if max_per_kind.is_some_and(|cap| *n >= cap) {
                            return false;
                        }
                        *n += 1;
                        true
                    })
                    .collect::<Vec<_>>()
            } else {
                Vec::new()
            };
            let work = Work {
                bounds: root.bounds,
                line: root.line,
                complete: tiled && selected_leaves.len() == leaf_count,
                leaves: selected_leaves,
                hash,
                kinds,
            };
            let (sender, receiver) = std::sync::mpsc::sync_channel(1);
            let work = std::sync::Arc::new(work);
            pending.push_back(Pending {
                work: work.clone(),
                receiver,
                tiled,
                resumed,
            });
            if work.leaves.is_empty() {
                let _ = sender.send(Outcome::default());
            } else {
                let family = family.clone();
                pool.spawn(move || {
                    let _ = sender.send(replay_root(&family, &work, chunk_leaves));
                });
            }
        }
    })?;
    if crate::budget::expired() {
        if !report.incomplete {
            report.deadline("budget");
        }
    }
    report.add_hash(record, record_hash.clone());
    if let Err(e) = domain.check(&bounds, &family.d0, &family.d1) {
        if let Some(cp) = &mut checkpoint {
            cp.failure(0, &record_hash, &e.reason, false)?;
        }
        report.error("domain", e);
    }
    if let Some(cp) = &mut checkpoint {
        cp.sync()?;
    }
    report.partial = max_roots.is_some()
        || accepted_roots < report.roots
        || only_kinds.is_some()
        || max_per_kind.is_some();
    report.details = serde_json::json!({"checked_roots":checked_roots,"accepted_roots":accepted_roots,"resumed_roots":report.resumed_roots,"leaf_timing":timing.into_iter().map(|(k,(n,t))|(k,serde_json::json!({"leaves":n,"seconds":t,"seconds_per_leaf":t/n as f64}))).collect::<BTreeMap<_,_>>()});
    Ok(())
}
struct ProgressDisplay {
    enabled: bool,
    start: Instant,
    last: Instant,
    roots: u64,
}
impl ProgressDisplay {
    fn new(enabled: bool) -> Self {
        Self {
            enabled,
            start: Instant::now(),
            last: Instant::now(),
            roots: 0,
        }
    }
    fn tick(&mut self, roots: u64, leaves: u64, in_flight: usize) {
        if self.enabled
            && (self.last.elapsed() >= Duration::from_secs(30) || roots - self.roots >= 200)
        {
            eprintln!(
                "roots={roots} leaves={leaves} elapsed={:.1}s in_flight={in_flight}",
                self.start.elapsed().as_secs_f64()
            );
            self.last = Instant::now();
            self.roots = roots;
        }
    }
}
struct Work {
    bounds: Box4,
    line: usize,
    leaves: Vec<(usize, Leaf)>,
    hash: String,
    kinds: crate::checkpoint::Counts,
    complete: bool,
}
/// The producer owns raw bytes, hashing, JSON parsing and tiling; only root boxes
/// survive the bounded pipeline in the global domain check.
enum Parsed {
    Row {
        line: usize,
        hash: String,
        root: Result<Option<Root>>,
        tiled: bool,
    },
    End(Result<String>),
}
fn produce(file: File, sender: &std::sync::mpsc::SyncSender<Parsed>) -> Result<String> {
    let mut reader = BufReader::new(file);
    let mut hasher = Sha256::new();
    let mut raw = Vec::new();
    let mut line = 0;
    loop {
        raw.clear();
        if reader.read_until(b'\n', &mut raw)? == 0 {
            break;
        }
        line += 1;
        hasher.update(&raw);
        let hash = format!("{:x}", Sha256::digest(&raw));
        let root = serde_json::from_slice(&raw)
            .map_err(crate::Error::from)
            .and_then(|v| parse_root(&v, line));
        let tiled = root.as_ref().ok().and_then(Option::as_ref).is_none_or(|r| {
            tiling(
                &r.bounds,
                &r.leaves
                    .iter()
                    .map(|l| l.bounds.clone())
                    .collect::<Vec<_>>(),
            )
        });
        if sender
            .send(Parsed::Row {
                line,
                hash,
                root,
                tiled,
            })
            .is_err()
        {
            break;
        }
    }
    Ok(format!("{:x}", hasher.finalize()))
}
type LeafAnswer = (usize, String, Result<()>, f64);
#[derive(Default)]
struct Outcome {
    leaves: Vec<LeafAnswer>,
    interrupted: bool,
    internal: Option<crate::Error>,
}
fn chunk_indices(count: usize) -> impl IndexedParallelIterator<Item = usize> {
    // Otherwise Rayon may fold adjacent chunk indices sequentially in one
    // task, recreating the consecutive-heavy-leaf tail at a different level.
    (0..count).into_par_iter().with_max_len(1)
}
fn replay_root(family: &Family, work: &Work, chunk_leaves: usize) -> Outcome {
    let mut outcome = Outcome::default();
    let run = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
        let local = std::sync::Arc::new(crate::stage_b::local_family(family, &work.bounds));
        // Each chunk has at most chunk_leaves entries. Consecutive selected
        // leaves go to distinct chunks until the stride wraps around.
        let stride = work.leaves.len().div_ceil(chunk_leaves);
        let chunks: Vec<_> = chunk_indices(stride)
            .map(|chunk| {
                let local = local.clone();
                let mut out = Outcome::default();
                for (index, l) in work.leaves.iter().skip(chunk).step_by(stride) {
                    if crate::budget::expired() {
                        out.interrupted = true;
                        break;
                    }
                    let start = Instant::now();
                    let f = if l.kind == "CORE"
                        || l.kind.starts_with("CORE1:")
                        || l.kind.starts_with("B3")
                        || l.kind == "B4U"
                    {
                        &local
                    } else {
                        family
                    };
                    let answer = match std::panic::catch_unwind(|| {
                        crate::leaf::check(f, &l.bounds, &l.kind)
                    }) {
                        Ok(v) => v,
                        Err(payload) => match crate::budget::panic_error(payload) {
                            Some(e) => Err(e),
                            None => {
                                out.interrupted = true;
                                break;
                            }
                        },
                    };
                    let failed = answer.is_err();
                    out.leaves.push((
                        *index,
                        l.kind.clone(),
                        answer,
                        start.elapsed().as_secs_f64(),
                    ));
                    if failed {
                        break;
                    }
                }
                out
            })
            .collect();
        let mut answers: Vec<_> = chunks.into_iter().flat_map(|c| c.leaves).collect();
        answers.sort_unstable_by_key(|a| a.0);
        let mut answers = answers.into_iter();
        // Chunk order is no longer record order. Keep only the completed
        // selected prefix, through its first refusal. A missing answer before
        // that refusal means a deadline, never an accepted partial root.
        for (index, _) in &work.leaves {
            match answers.next() {
                Some(answer) if answer.0 == *index => {
                    let failed = answer.2.is_err();
                    outcome.leaves.push(answer);
                    if failed {
                        break;
                    }
                }
                _ => {
                    outcome.interrupted = true;
                    break;
                }
            }
        }
    }));
    if let Err(payload) = run {
        match crate::budget::panic_error(payload) {
            Some(e) => outcome.internal = Some(e),
            None => outcome.interrupted = true,
        }
    }
    outcome
}
struct Pending {
    work: std::sync::Arc<Work>,
    receiver: std::sync::mpsc::Receiver<Outcome>,
    tiled: bool,
    resumed: Option<crate::checkpoint::Counts>,
}
/// Admission, not result delivery, is bounded. Each admitted root has its own
/// one-slot mailbox, so the earliest root can always deliver even if all later
/// roots finished first. Releasing one slot immediately admits another root.
fn commit_front(
    pending: &mut std::collections::VecDeque<Pending>,
    wait: bool,
    timing: &mut BTreeMap<String, (u64, f64)>,
    checkpoint: &mut Option<crate::checkpoint::Checkpoint>,
    report: &mut Report,
    accepted: &mut u64,
    committed: &mut u64,
    leaves: &mut u64,
) -> Result<bool> {
    let Some(front) = pending.front() else {
        return Ok(false);
    };
    let result = if wait {
        match front.receiver.recv_timeout(Duration::from_millis(200)) {
            Ok(v) => Some(v),
            Err(std::sync::mpsc::RecvTimeoutError::Timeout) => None,
            Err(_) => return Err(refuse("worker results missing")),
        }
    } else {
        match front.receiver.try_recv() {
            Ok(v) => Some(v),
            Err(std::sync::mpsc::TryRecvError::Empty) => None,
            Err(_) => return Err(refuse("worker results missing")),
        }
    };
    let Some(root) = result else {
        return Ok(false);
    };
    let front = pending.pop_front().unwrap();
    let work = front.work;
    *committed += 1;
    *leaves += work.kinds.values().sum::<u64>();
    if !front.tiled {
        let reason = "leaves do not reconstruct the midpoint bisection tree";
        if let Some(cp) = checkpoint {
            cp.failure(work.line, &work.hash, reason, false)?;
        }
        report.error(format!("line {}", work.line), refuse(reason));
    }
    if let Some(kinds) = front.resumed {
        report.resumed_roots += 1;
        *accepted += 1;
        for (k, n) in kinds {
            *report.checked_leaf_kinds.entry(k).or_default() += n;
        }
        return Ok(true);
    }
    let complete = work.complete
        && root.leaves.len() == work.leaves.len()
        && root.leaves.iter().all(|l| l.2.is_ok())
        && !root.interrupted
        && root.internal.is_none();
    if complete {
        if let Some(cp) = checkpoint {
            cp.accept(work.line, &work.hash, &work.kinds)?;
        }
        *accepted += 1;
    }
    if root.interrupted {
        report.deadline(format!("line {}", work.line));
        if let Some(cp) = checkpoint {
            cp.failure(work.line, &work.hash, "incomplete: deadline", true)?;
        }
    }
    if let Some(e) = root.internal {
        if let Some(cp) = checkpoint {
            cp.failure(work.line, &work.hash, &e.reason, false)?;
        }
        report.error(format!("line {}", work.line), e);
    }
    for (index, kind, answer, seconds) in root.leaves {
        let t = timing.entry(kind.clone()).or_default();
        t.0 += 1;
        t.1 += seconds;
        *report.checked_leaf_kinds.entry(kind.clone()).or_default() += 1;
        if let Err(e) = answer {
            if let Some(cp) = checkpoint {
                cp.failure(work.line, &work.hash, &e.reason, false)?;
            }
            report.error(
                format!("line {}, leaf {} ({kind})", work.line, index + 1),
                e,
            );
        }
    }
    Ok(true)
}
pub fn angular_range(path: &Path, report: &mut Report) -> Result<()> {
    let mut hasher = Sha256::new();
    let mut reader = BufReader::new(File::open(path)?);
    let mut line = Vec::new();
    let mut us = BTreeSet::new();
    loop {
        line.clear();
        if reader.read_until(b'\n', &mut line)? == 0 {
            break;
        }
        hasher.update(&line);
        let v: Value = serde_json::from_slice(&line)?;
        if v.get("header").is_some() {
            continue;
        }
        let b = v["root"]
            .as_array()
            .ok_or_else(|| parse_error("root missing"))?;
        require(b.len() == 8, "root must have eight coordinates")?;
        let a = value(&b[4])?;
        let z = value(&b[5])?;
        require(
            a < z && !(a < Q::zero() && z > Q::zero()),
            "invalid root angular interval",
        )?;
        us.insert((a, z));
    }
    report.add_hash(path, format!("{:x}", hasher.finalize()));
    require(!us.is_empty(), "empty angular partition")?;
    let mut prev = None;
    for (a, b) in &us {
        if let Some(p) = prev {
            require(p == a, "angular gap or overlap")?;
        }
        prev = Some(b);
    }
    let a = -&us.first().unwrap().0;
    let b = &us.last().unwrap().1;
    require(
        a > Q::zero() && a < int(1) && b > &Q::zero() && b < &int(1) && &a + b + &a * b >= int(1),
        "angular coverage is less than 90 degrees",
    )
}
#[cfg(test)]
mod tests {
    use super::*;
    fn b() -> Box4 {
        [
            int(0),
            int(1),
            int(0),
            int(1),
            int(0),
            crate::rat::q(1, 2),
            int(0),
            int(1),
        ]
    }
    #[test]
    fn chunked_root_preserves_first_failure() {
        let family = Family::parse(serde_json::json!({
            "d0":"0", "d1":"1", "UA":"9/5", "F":[], "T":[], "V":[]
        }))
        .unwrap();
        let mut bounds = b();
        bounds[1] = crate::rat::q(1, 10);
        bounds[3] = crate::rat::q(1, 10);
        let mut work = Work {
            bounds: bounds.clone(),
            line: 1,
            hash: String::new(),
            kinds: BTreeMap::new(),
            complete: true,
            leaves: (0..200)
                .map(|i| {
                    (
                        i,
                        Leaf {
                            bounds: bounds.clone(),
                            kind: if i == 65 || i == 128 { "CORE" } else { "EMPTY" }.into(),
                        },
                    )
                })
                .collect(),
        };
        for threads in [1, 2] {
            let pool = rayon::ThreadPoolBuilder::new()
                .num_threads(threads)
                .build()
                .unwrap();
            for size in [1, 4, 64, 200, usize::MAX] {
                let result = pool.install(|| replay_root(&family, &work, size));
                assert!(!result.interrupted && result.internal.is_none());
                assert_eq!(result.leaves.len(), 66);
                assert_eq!(result.leaves.last().unwrap().0, 65);
                assert!(result.leaves.last().unwrap().2.is_err());
                assert!(result.leaves.iter().enumerate().all(|(i, l)| i == l.0));
            }
        }
        for (_, leaf) in &mut work.leaves {
            leaf.kind = "EMPTY".into();
        }
        let pool = rayon::ThreadPoolBuilder::new()
            .num_threads(2)
            .build()
            .unwrap();
        for size in [1, 4, 64, 200, usize::MAX] {
            let result = pool.install(|| replay_root(&family, &work, size));
            assert_eq!(result.leaves.len(), 200);
            assert!(result.leaves.iter().all(|l| l.2.is_ok()));
            assert!(result.leaves.iter().enumerate().all(|(i, l)| i == l.0));
        }
        // Adjacent expensive chunks must remain independently stealable.
        // Without the task-size bound, the first two may share one serial fold.
        let ready = (std::sync::Mutex::new(0usize), std::sync::Condvar::new());
        pool.install(|| {
            chunk_indices(1024).for_each(|c| {
                if c < 2 {
                    let mut count = ready.0.lock().unwrap();
                    *count += 1;
                    ready.1.notify_all();
                    let (count, _) = ready
                        .1
                        .wait_timeout_while(count, Duration::from_secs(2), |n| *n < 2)
                        .unwrap();
                    assert_eq!(
                        *count, 2,
                        "adjacent chunks were not independently scheduled"
                    );
                }
            });
        });
        // Selection may leave gaps in original record indices.
        work.leaves.retain(|(i, _)| i % 3 == 0);
        let result = pool.install(|| replay_root(&family, &work, 4));
        assert_eq!(result.leaves.len(), work.leaves.len());
        assert!(result.leaves.iter().enumerate().all(|(i, l)| 3 * i == l.0));
    }

    #[test]
    fn ordered_mailboxes_do_not_block_earliest_delivery() {
        let mut pending = std::collections::VecDeque::new();
        let mut senders = Vec::new();
        for line in 1..=16 {
            let (sender, receiver) = std::sync::mpsc::sync_channel(1);
            senders.push(sender);
            pending.push_back(Pending {
                receiver,
                tiled: true,
                resumed: None,
                work: std::sync::Arc::new(Work {
                    bounds: b(),
                    line,
                    leaves: vec![],
                    hash: String::new(),
                    kinds: BTreeMap::new(),
                    complete: true,
                }),
            });
        }
        for sender in senders.iter().skip(1) {
            sender.send(Outcome::default()).unwrap();
        }
        let (mut timing, mut cp, mut report) = (BTreeMap::new(), None, Report::new("test"));
        let (mut accepted, mut committed, mut leaves) = (0, 0, 0);
        assert!(!commit_front(
            &mut pending,
            false,
            &mut timing,
            &mut cp,
            &mut report,
            &mut accepted,
            &mut committed,
            &mut leaves
        )
        .unwrap());
        assert_eq!(pending.len(), 16);
        senders[0].send(Outcome::default()).unwrap();
        assert!(commit_front(
            &mut pending,
            false,
            &mut timing,
            &mut cp,
            &mut report,
            &mut accepted,
            &mut committed,
            &mut leaves
        )
        .unwrap());
        assert_eq!(pending.len(), 15); // One admission slot is available immediately.
        assert_eq!(committed, 1);
        while !pending.is_empty() {
            assert!(commit_front(
                &mut pending,
                false,
                &mut timing,
                &mut cp,
                &mut report,
                &mut accepted,
                &mut committed,
                &mut leaves
            )
            .unwrap());
        }
        assert_eq!(accepted, 16);
    }

    #[test]
    fn tree() {
        let r = b();
        let (mut l, mut h) = (r.clone(), r.clone());
        l[1] = crate::rat::q(1, 2);
        h[0] = l[1].clone();
        assert!(tiling(&r, &[l.clone(), h.clone()]));
        assert!(!tiling(&r, &[l.clone()]));
        assert!(!tiling(&r, &[l.clone(), h.clone(), h.clone()]));
        h[0] = crate::rat::q(2, 5);
        assert!(!tiling(&r, &[l.clone(), h]));
        l[0] = int(-1);
        assert!(!tiling(&r, &[l]));
    }
}
