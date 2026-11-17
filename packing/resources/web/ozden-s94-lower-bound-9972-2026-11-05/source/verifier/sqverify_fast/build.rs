//! Embed the digest of the sources, manifest and lockfile, so every receipt
//! names the code that produced it.

use std::path::Path;

use sha2::{Digest, Sha256};

fn main() {
    let mut files = vec![
        "Cargo.toml".to_string(),
        "Cargo.lock".to_string(),
        "build.rs".to_string(),
    ];
    let mut sources: Vec<String> = std::fs::read_dir("src")
        .expect("src directory")
        .filter_map(Result::ok)
        .map(|entry| format!("src/{}", entry.file_name().to_string_lossy()))
        .filter(|name| Path::new(name).extension().is_some_and(|ext| ext == "rs"))
        .collect();
    sources.sort();
    files.extend(sources);
    let mut hasher = Sha256::new();
    for file in &files {
        println!("cargo:rerun-if-changed={file}");
        hasher.update(file.as_bytes());
        hasher.update([0]);
        hasher.update(std::fs::read(Path::new(file)).expect("readable source"));
        hasher.update([0]);
    }
    let digest = hasher
        .finalize()
        .iter()
        .fold(String::new(), |mut text, byte| {
            use std::fmt::Write;
            let _ = write!(text, "{byte:02x}");
            text
        });
    println!("cargo:rustc-env=SQVERIFY_FAST_SOURCE_SHA256={digest}");
    println!(
        "cargo:rustc-env=SQVERIFY_FAST_TARGET={}",
        std::env::var("TARGET").unwrap_or_default()
    );
    let rustc = std::env::var("RUSTC").unwrap_or_else(|_| "rustc".into());
    let version = std::process::Command::new(rustc)
        .arg("--version")
        .output()
        .map(|out| String::from_utf8_lossy(&out.stdout).trim().to_string())
        .unwrap_or_default();
    println!("cargo:rustc-env=SQVERIFY_FAST_RUSTC={version}");
}
