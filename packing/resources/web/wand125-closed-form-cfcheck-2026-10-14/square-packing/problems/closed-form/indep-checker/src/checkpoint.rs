//! Append-only receipts from a trusted prior run; these are not proof certificates.
use crate::{
    record::{parse_root, Root},
    require, Result,
};
use sha2::{Digest, Sha256};
use std::{
    collections::BTreeMap,
    fs::{File, OpenOptions},
    io::{BufRead, BufReader, Write},
    path::Path,
    time::{Duration, Instant},
};

pub type Counts = BTreeMap<String, u64>;
pub fn counts(root: &Root) -> Counts {
    let mut out = Counts::new();
    for leaf in &root.leaves {
        *out.entry(leaf.kind.clone()).or_default() += 1;
    }
    out
}
#[derive(Clone)]
struct Entry {
    hash: String,
    accepted: Option<(u64, Counts)>,
}
pub struct Checkpoint {
    file: File,
    dirty: usize,
    last_sync: Instant,
    pub input_hash: String,
    accepted: BTreeMap<usize, (String, Counts)>,
}
impl Checkpoint {
    pub fn open(path: &Path, record: &Path, family_hash: &str, resume: bool) -> Result<Self> {
        // Never overwrite a record or family by accident. Existing nonempty logs
        // require explicit resume, and their binding is checked before any append.
        let bytes = if path.exists() {
            std::fs::read(path)?
        } else {
            Vec::new()
        };
        require(
            resume || bytes.is_empty(),
            "nonempty progress file requires --resume",
        )?;
        require(
            !resume || path.exists(),
            "resume progress file does not exist",
        )?;
        let header = format!("CFCHECK_PROGRESS_V1 {family_hash}");
        let complete = bytes.iter().rposition(|b| *b == b'\n').map_or(0, |i| i + 1);
        let text = std::str::from_utf8(&bytes[..complete])
            .map_err(|_| crate::refuse("invalid progress encoding"))?;
        let mut lines = text.lines();
        if !bytes.is_empty() {
            require(
                lines.next() == Some(header.as_str()),
                "progress family or format mismatch",
            )?;
        }
        let mut entries = BTreeMap::<usize, Entry>::new();
        for line in lines {
            // A torn last append is sealed, never trusted, on the next open.
            if line.ends_with(" #TORN") {
                continue;
            }
            let p: Vec<_> = line.splitn(5, ' ').collect();
            require(p.len() >= 4, "malformed progress entry")?;
            let n = p[1]
                .parse::<usize>()
                .map_err(|_| crate::refuse("invalid progress line number"))?;
            require(n > 0 || p[0] == "REFUSE", "invalid progress line number")?;
            let accepted = match p[0] {
                "ACCEPT" => {
                    require(p.len() == 5, "malformed ACCEPT entry")?;
                    let leaves = p[3]
                        .parse()
                        .map_err(|_| crate::refuse("invalid progress leaf count"))?;
                    let kinds: Counts = serde_json::from_str(p[4])
                        .map_err(|_| crate::refuse("invalid progress kind counts"))?;
                    Some((leaves, kinds))
                }
                "REFUSE" | "INCOMPLETE" => None,
                _ => return Err(crate::refuse("unknown progress entry")),
            };
            if let Some(previous) = entries.get(&n) {
                require(previous.hash == p[2], "conflicting progress root hashes")?;
            }
            entries.insert(
                n,
                Entry {
                    hash: p[2].into(),
                    accepted,
                },
            );
        }
        // Validate every listed line, including refusals, before reusing anything.
        let mut accepted = BTreeMap::new();
        let mut reader = BufReader::new(File::open(record)?);
        let mut raw = Vec::new();
        let mut n = 0;
        let mut record_hash = Sha256::new();
        while reader.read_until(b'\n', &mut raw)? != 0 {
            record_hash.update(&raw);
            n += 1;
            if let Some(entry) = entries.remove(&n) {
                require(
                    entry.hash == format!("{:x}", Sha256::digest(&raw)),
                    "progress root hash mismatch: progress file belongs to another record",
                )?;
                if let Some((leaves, kinds)) = entry.accepted {
                    let root = parse_root(&serde_json::from_slice(&raw)?, n)?
                        .ok_or_else(|| crate::refuse("progress entry refers to header"))?;
                    require(
                        leaves == root.leaves.len() as u64 && kinds == counts(&root),
                        "progress counts mismatch",
                    )?;
                    accepted.insert(n, (entry.hash, kinds));
                }
            }
            raw.clear();
        }
        if let Some(entry) = entries.remove(&0) {
            require(
                entry.hash == format!("{:x}", record_hash.finalize()),
                "progress record hash mismatch",
            )?;
        }
        require(entries.is_empty(), "progress entry beyond record end")?;
        let mut file = OpenOptions::new().create(true).append(true).open(path)?;
        if bytes.is_empty() {
            writeln!(file, "{header}")?;
        } else if complete < bytes.len() {
            file.write_all(b" #TORN\n")?;
        }
        file.sync_all()?;
        Ok(Self {
            file,
            dirty: 0,
            last_sync: Instant::now(),
            accepted,
            input_hash: format!("{:x}", Sha256::digest(&bytes)),
        })
    }
    pub fn resumed(&self, line: usize, hash: &str) -> Result<Option<&Counts>> {
        match self.accepted.get(&line) {
            Some((saved, kinds)) => {
                require(saved == hash, "record changed after progress validation")?;
                Ok(Some(kinds))
            }
            None => Ok(None),
        }
    }
    pub fn accept(&mut self, line: usize, hash: &str, kinds: &Counts) -> Result<()> {
        self.append(format!(
            "ACCEPT {line} {hash} {} {}",
            kinds.values().sum::<u64>(),
            serde_json::to_string(kinds).unwrap()
        ))
    }
    pub fn failure(
        &mut self,
        line: usize,
        hash: &str,
        reason: &str,
        incomplete: bool,
    ) -> Result<()> {
        self.append(format!(
            "{} {line} {hash} {}",
            if incomplete { "INCOMPLETE" } else { "REFUSE" },
            serde_json::to_string(reason).unwrap()
        ))
    }
    fn append(&mut self, text: String) -> Result<()> {
        writeln!(self.file, "{text}")?;
        self.dirty += 1;
        self.sync_due()?;
        Ok(())
    }
    pub fn sync_due(&mut self) -> Result<()> {
        if self.dirty >= 16
            || (self.dirty > 0 && self.last_sync.elapsed() >= Duration::from_secs(2))
        {
            self.sync()?;
        }
        Ok(())
    }
    pub fn sync(&mut self) -> Result<()> {
        if self.dirty > 0 {
            self.file.sync_all()?;
            self.dirty = 0;
            self.last_sync = Instant::now();
        }
        Ok(())
    }
}

impl Drop for Checkpoint {
    fn drop(&mut self) {
        // Normal completion uses fallible sync(); retain receipts on error exits too.
        let _ = self.sync();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn receipt_sync_count_timer_and_final_flush() {
        let path = format!("tests/checkpoint_sync_{}", std::process::id());
        let file = OpenOptions::new()
            .create_new(true)
            .write(true)
            .open(&path)
            .unwrap();
        let mut cp = Checkpoint {
            file,
            dirty: 0,
            last_sync: Instant::now(),
            input_hash: String::new(),
            accepted: BTreeMap::new(),
        };
        for _ in 0..15 {
            cp.append("test receipt".into()).unwrap();
        }
        assert_eq!(cp.dirty, 15);
        cp.append("sixteenth receipt".into()).unwrap();
        assert_eq!(cp.dirty, 0);
        cp.append("timer receipt".into()).unwrap();
        cp.last_sync = Instant::now() - Duration::from_secs(2);
        cp.sync_due().unwrap();
        assert_eq!(cp.dirty, 0);
        cp.append("final receipt".into()).unwrap();
        cp.sync().unwrap();
        assert_eq!(cp.dirty, 0);
        drop(cp);
        assert_eq!(std::fs::read_to_string(&path).unwrap().lines().count(), 18);
        std::fs::remove_file(path).unwrap();
    }
}
