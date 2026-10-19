//! Read-once gzip node streaming and canonical object digests.
use crate::pyjson::{canonical, digest, escape_points, repr_key};
use crate::value::{Key, Map, Value};
use crate::{Result, malformed, require};
use flate2::read::MultiGzDecoder;
use sha2::{Digest, Sha256};
use std::{
    fs::File,
    io::{BufRead, BufReader, Read},
    path::Path,
};
/// Open a buffered concatenated-gzip byte stream for strict UTF-8 parsing.
pub fn gunzip_text(path: &Path) -> Result<Box<dyn BufRead>> {
    Ok(Box::new(BufReader::with_capacity(
        1 << 20,
        MultiGzDecoder::new(File::open(path)?),
    )))
}
/// Read a gzip object and return its Python-canonical SHA-256.
pub fn load_object(path: &Path) -> Result<(Value, String)> {
    let mut raw = Vec::new();
    gunzip_text(path)?.read_to_end(&mut raw)?;
    let v: Value = crate::value::from_slice(&raw)?;
    let sha = digest(canonical(&v)?.as_bytes());
    Ok((v, sha))
}
/// A read-once node iterator whose digest is final only after complete EOF validation.
pub struct NodeStream {
    pending: std::collections::VecDeque<u8>,
    acquired: bool,
    /// Members parsed outside the streamed steps array.
    pub header: Value,
    /// Canonical digest populated only after the stream reaches validated EOF.
    pub sha256: Option<String>,
    source: Box<dyn BufRead>,
    digest: Sha256,
    started: bool,
    finished: bool,
    count: usize,
}
impl NodeStream {
    /// Open a gzip node and parse members preceding the steps array.
    pub fn new(path: &Path) -> Result<Self> {
        Self::from_reader(gunzip_text(path)?)
    }
    /// Parse a buffered node source without buffering its steps array.
    pub fn from_reader(source: Box<dyn BufRead>) -> Result<Self> {
        let mut s = Self {
            pending: std::collections::VecDeque::new(),
            acquired: false,
            header: Value::Object(Map::new()),
            sha256: None,
            source,
            digest: Sha256::new(),
            started: false,
            finished: false,
            count: 0,
        };
        s.digest.update(b"{");
        require(s.char()? == Some(b'{'), "the node is not a JSON object")?;
        let mut separator = if s.peek()? == Some(b'}') { b'}' } else { b',' };
        while separator == b',' {
            let name = s.name()?;
            if name.is("steps") {
                require(s.char()? == Some(b'['), "the node's steps are not an array")?;
                s.hash_members(false)?;
                s.digest.update(b"\"steps\":[");
                return Ok(s);
            }
            let v = s.value()?;
            s.insert(name, v)?;
            separator = s.char()?.unwrap_or(0);
            require(
                b",}".contains(&separator),
                "the node's members are not comma-separated",
            )?;
        }
        Err(crate::Error::Check("the node has no steps".into()))
    }
    fn insert(&mut self, k: Key, v: Value) -> Result<()> {
        self.header
            .as_object_mut()
            .ok_or_else(|| malformed("invalid header"))?
            .insert(k, v);
        Ok(())
    }
    fn hash_members(&mut self, after: bool) -> Result<()> {
        let obj = self
            .header
            .as_object()
            .ok_or_else(|| malformed("invalid header"))?;
        let mut keys: Vec<_> = obj
            .keys()
            .filter(|k| {
                if after {
                    *k > &Key::from("steps")
                } else {
                    *k < &Key::from("steps")
                }
            })
            .collect();
        keys.sort();
        for k in keys {
            if after {
                self.digest.update(b",");
            }
            self.digest.update(escape_points(k.0.iter().copied()));
            self.digest.update(b":");
            self.digest.update(canonical(&obj[k])?);
            if !after {
                self.digest.update(b",");
            }
        }
        Ok(())
    }
    fn peek(&mut self) -> Result<Option<u8>> {
        loop {
            let c = self.raw()?;
            if c.is_some_and(|b| b" \t\r\n".contains(&b)) {
                continue;
            }
            if let Some(c) = c {
                self.pending.push_front(c);
            }
            return Ok(c);
        }
    }
    fn char(&mut self) -> Result<Option<u8>> {
        self.peek()?;
        self.raw()
    }
    fn raw(&mut self) -> Result<Option<u8>> {
        if let Some(c) = self.pending.pop_front() {
            return Ok(Some(c));
        }
        let c = self.source.fill_buf()?.first().copied();
        if c.is_some() {
            self.source.consume(1);
        }
        Ok(c)
    }
    fn name(&mut self) -> Result<Key> {
        let value = self.value()?;
        require(value.is_string(), "a node member's name is not a string")?;
        let name = value.key().ok_or_else(|| malformed("invalid name"))?;
        require(
            self.header
                .as_object()
                .and_then(|o| o.get_key(&name))
                .is_none(),
            format!("the node repeats its member {}", repr_key(&name)),
        )?;
        require(
            self.char()? == Some(b':'),
            "a node member's name lacks its colon",
        )?;
        Ok(name)
    }
    fn value(&mut self) -> Result<Value> {
        let first = self
            .char()?
            .ok_or_else(|| malformed("unexpected end of JSON"))?;
        let mut raw = vec![first];
        if first == b'"' || first == b'{' || first == b'[' {
            let mut depth = usize::from(first != b'"');
            let mut in_string = first == b'"';
            let mut escaped = false;
            loop {
                let c = self
                    .raw()?
                    .ok_or_else(|| malformed("unterminated JSON value"))?;
                raw.push(c);
                if in_string {
                    if escaped {
                        escaped = false;
                    } else if c == b'\\' {
                        escaped = true;
                    } else if c == b'"' {
                        in_string = false;
                        if depth == 0 {
                            break;
                        }
                    }
                } else if c == b'"' {
                    in_string = true;
                } else if c == b'{' || c == b'[' {
                    depth = depth
                        .checked_add(1)
                        .ok_or_else(|| malformed("JSON nesting overflow"))?;
                } else if c == b'}' || c == b']' {
                    depth = depth
                        .checked_sub(1)
                        .ok_or_else(|| malformed("unbalanced JSON"))?;
                    if depth == 0 {
                        break;
                    }
                }
            }
        } else {
            while let Some(c) = self.raw()? {
                if b" \t\n\r,:]}".contains(&c) {
                    self.pending.push_front(c);
                    break;
                }
                raw.push(c);
            }
            let (value, used) = crate::value::prefix_utf8(&raw)?;
            for &c in raw[used..].iter().rev() {
                self.pending.push_front(c);
            }
            return Ok(value);
        }
        // gunzip_text in Python uses strict UTF-8, unlike json.loads(bytes).
        let text = std::str::from_utf8(&raw).map_err(|_| malformed("invalid UTF-8"))?;
        crate::value::from_str(text)
    }

    /// Read one step, or finalize trailing members and require EOF before returning None.
    pub fn next_step(&mut self) -> Result<Option<Value>> {
        if self.finished {
            return Ok(None);
        }
        let separator = if self.started {
            let c = self.char()?.unwrap_or(0);
            require(
                b",]".contains(&c),
                "the node's steps are not comma-separated",
            )?;
            c
        } else {
            self.started = true;
            if self.peek()? == Some(b']') {
                self.char()?.unwrap_or(0)
            } else {
                b','
            }
        };
        if separator == b',' {
            let step = self.value()?;
            if self.count > 0 {
                self.digest.update(b",");
            }
            self.digest.update(canonical(&step)?);
            self.count += 1;
            return Ok(Some(step));
        }
        self.digest.update(b"]");
        loop {
            let c = self.char()?;
            if c != Some(b',') {
                require(
                    c == Some(b'}'),
                    "the node's members are not comma-separated",
                )?;
                break;
            }
            let name = self.name()?;
            require(
                name > Key::from("steps"),
                format!("the node's member {} follows its steps", repr_key(&name)),
            )?;
            let v = self.value()?;
            self.insert(name, v)?;
        }
        require(self.peek()?.is_none(), "data follows the node")?;
        self.hash_members(true)?;
        self.digest.update(b"}");
        self.sha256 = Some(format!("{:x}", self.digest.clone().finalize()));
        self.finished = true;
        Ok(None)
    }
    // Explicit generator acquisition, for callers needing Python's read-once check.
    /// Acquire the steps generator once, before any step has been read.
    pub fn steps(&mut self) -> Result<()> {
        require(
            !self.acquired && !self.started,
            "the node's steps are read once",
        )?;
        self.acquired = true;
        Ok(())
    }
}
