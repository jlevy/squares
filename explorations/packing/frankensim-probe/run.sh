#!/usr/bin/env bash
# Run the two FrankenSim probes against a local frankensim checkout.
#
# These are OUR experiment sources; nothing from FrankenSim is vendored here.
# They are dropped into the checkout's examples/ directories, run, and removed.
#
# Usage: ./run.sh /path/to/frankensim
set -euo pipefail
FS="${1:?usage: ./run.sh /path/to/frankensim}"
HERE="$(cd "$(dirname "$0")" && pwd)"
[ -f "$FS/Cargo.toml" ] || { echo "not a frankensim checkout: $FS" >&2; exit 1; }

AD="$FS/crates/fs-ad/Cargo.toml"
AD_BACKUP="$(mktemp)"
cp "$AD" "$AD_BACKUP"

cleanup() {
  cp "$AD_BACKUP" "$AD"; rm -f "$AD_BACKUP"
  rm -f "$FS/crates/fs-ivl/examples/packing_sat.rs" \
        "$FS/crates/fs-rand/examples/schedule_invariance.rs"
  rmdir "$FS/crates/fs-ivl/examples" "$FS/crates/fs-rand/examples" 2>/dev/null || true
}
trap cleanup EXIT

# At the heads recorded in constellation.lock, fs-ad asks for FrankenTorch
# packages named `frankentorch-autograd` / `frankentorch-core`, but the pinned
# checkout names them `ft-autograd` / `ft-core`, so Cargo cannot resolve the
# workspace at all. Both deps are optional and off by default; drop the renames
# for the duration of the run. Reported in the research doc.
if grep -q 'package = "frankentorch-autograd"' "$AD"; then
  echo "[probe] patching fs-ad manifest around the constellation pin drift" >&2
  sed -i.bak 's/package = "frankentorch-autograd", //; s/package = "frankentorch-core", //' "$AD"
  rm -f "$AD.bak"
fi

mkdir -p "$FS/crates/fs-ivl/examples" "$FS/crates/fs-rand/examples"
cp "$HERE/packing_sat.rs" "$FS/crates/fs-ivl/examples/"
cp "$HERE/schedule_invariance.rs" "$FS/crates/fs-rand/examples/"

echo "== fs-ivl: can certified interval arithmetic verify a packing? =="
( cd "$FS" && cargo run -q -p fs-ivl --example packing_sat )
echo
echo "== fs-rand: is a counter-based stream schedule-independent? =="
( cd "$FS" && cargo run -q --release -p fs-rand --example schedule_invariance )
