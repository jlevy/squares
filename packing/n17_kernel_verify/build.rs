//! Embed the optional default cover and record the verifier source digest.
use sha2::{Digest, Sha256};
use std::{env, fs, path::PathBuf};
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let root = PathBuf::from(env::var("CARGO_MANIFEST_DIR")?);
    println!("cargo:rerun-if-changed={}", root.join("src").display());
    let mut files = vec![
        root.join("Cargo.toml"),
        root.join("Cargo.lock"),
        root.join("build.rs"),
    ];
    for f in fs::read_dir(root.join("src"))? {
        let p = f?.path();
        if p.extension().is_some_and(|x| x == "rs") {
            files.push(p);
        }
    }
    files.sort();
    let mut hash = Sha256::new();
    for p in files {
        println!("cargo:rerun-if-changed={}", p.display());
        hash.update(fs::read(p)?);
    }
    println!("cargo:rustc-env=SOURCE_SHA256={:x}", hash.finalize());
    let candidates = [
        root.join("cells/cover.json"),
        root.join("../cells/cover.json"),
    ];
    let mut data = Vec::new();
    for p in &candidates {
        println!("cargo:rerun-if-changed={}", p.display());
        if data.is_empty() && p.is_file() {
            data = fs::read(p)?;
        }
    }
    fs::write(PathBuf::from(env::var("OUT_DIR")?).join("cover.json"), data)?;
    Ok(())
}
