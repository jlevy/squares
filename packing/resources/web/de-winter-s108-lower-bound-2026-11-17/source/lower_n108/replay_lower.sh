#!/bin/sh
# Rust 1.98 or later and Cargo. The first build downloads the pinned crates.
set -eu
cd "$(dirname "$0")"
cargo build --locked --release --manifest-path sqverify_fast/Cargo.toml
sqverify_fast/target/release/sqverify-fast --candidate evidence/n108_measure.json.gz \
    --n 108 --directions all --threads "${THREADS:-4}" > lower_replay.jsonl
python3 check_lower.py lower_replay.jsonl
