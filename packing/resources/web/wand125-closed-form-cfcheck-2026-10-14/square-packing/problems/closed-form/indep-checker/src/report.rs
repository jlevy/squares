use crate::{Error, Result};
use serde::Serialize;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::{collections::BTreeMap, fs, path::Path, time::Instant};
#[derive(Serialize)]
pub struct Input {
    pub path: String,
    pub sha256: String,
}
#[derive(Serialize)]
pub struct Refusal {
    pub r#where: String,
    pub reason: String,
}
#[derive(Serialize)]
pub struct Report {
    pub ok: bool,
    pub command: String,
    pub inputs: Vec<Input>,
    pub extra_keys: BTreeMap<String, Vec<String>>,
    pub roots: u64,
    pub leaves: u64,
    pub leaf_kinds: BTreeMap<String, u64>,
    pub checked_leaf_kinds: BTreeMap<String, u64>,
    pub refusals: Vec<Refusal>,
    pub partial: bool,
    pub incomplete: bool,
    pub interruptions: Vec<Refusal>,
    pub resumed_roots: u64,
    pub details: Value,
    pub seconds: f64,
    #[serde(skip)]
    pub code: i32,
    #[serde(skip)]
    pub start: Option<Instant>,
}
impl Report {
    pub fn new(command: &str) -> Self {
        Self {
            ok: true,
            command: command.into(),
            inputs: vec![],
            extra_keys: BTreeMap::new(),
            roots: 0,
            leaves: 0,
            leaf_kinds: BTreeMap::new(),
            checked_leaf_kinds: BTreeMap::new(),
            refusals: vec![],
            partial: false,
            incomplete: false,
            interruptions: vec![],
            resumed_roots: 0,
            details: json!({}),
            seconds: 0.,
            code: 0,
            start: Some(Instant::now()),
        }
    }
    pub fn error(&mut self, loc: impl Into<String>, e: Error) {
        self.ok = false;
        self.code = self.code.max(e.code);
        self.refusals.push(Refusal {
            r#where: loc.into(),
            reason: e.reason,
        });
    }
    pub fn deadline(&mut self, loc: impl Into<String>) {
        self.ok = false;
        self.code = self.code.max(1);
        self.incomplete = true;
        self.interruptions.push(Refusal {
            r#where: loc.into(),
            reason: "incomplete: deadline".into(),
        });
    }
    pub fn add_bytes(&mut self, path: &Path, bytes: &[u8]) {
        self.add_hash(path, format!("{:x}", Sha256::digest(bytes)));
    }
    pub fn add_hash(&mut self, path: &Path, sha256: String) {
        self.inputs.push(Input {
            path: path.to_string_lossy().into_owned(),
            sha256,
        });
    }
    pub fn read_json(&mut self, path: &Path) -> Result<Value> {
        let bytes = fs::read(path)?;
        self.add_bytes(path, &bytes);
        let value: Value = serde_json::from_slice(&bytes)?;
        if let Some(object) = value.as_object() {
            if object.contains_key("F") || object.contains_key("T") || object.contains_key("UA") {
                let base = ["d0", "d1", "UA", "F", "T", "V", "U"];
                let keys = object
                    .keys()
                    .filter(|key| !base.contains(&key.as_str()))
                    .cloned()
                    .collect();
                self.extra_keys
                    .insert(path.to_string_lossy().into_owned(), keys);
            }
        }
        Ok(value)
    }
    pub fn finish(&mut self) {
        let mut identities = BTreeMap::new();
        let mut changed = Vec::new();
        for input in &self.inputs {
            if let Some(previous) = identities.insert(input.path.clone(), input.sha256.clone()) {
                if previous != input.sha256 {
                    changed.push(input.path.clone());
                }
            }
        }
        for path in changed {
            self.error(path, crate::refuse("input bytes changed between reads"));
        }
        self.seconds = self.start.take().unwrap().elapsed().as_secs_f64();
    }
}
