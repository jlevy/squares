#!/usr/bin/env python3
"""Generate Lean data modules from the release data files.

Emits atom and orientation-sample data as plain string literals ("x y w" /
"p q" lines) so the Lean side re-parses them with its own poisoned exact
parser. Records the sha256 of each source file in a comment for provenance.
"""
import csv, hashlib, sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
lean = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

atoms_csv = root / 'data/atoms.csv'
rows = list(csv.DictReader(open(atoms_csv)))
assert len(rows) == 560
atom_lines = "\n".join(f"{int(r['X'])} {int(r['Y'])} {int(r['weight_num'])}" for r in rows)
(lean / 'Square17/AtomData.lean').write_text(
    f"-- Generated from data/atoms.csv (sha256 {sha(atoms_csv)}). Do not edit.\n"
    "import Square17.Basic\n"
    "namespace Square17\n\n"
    f"def atomData : String := \"{atom_lines.replace(chr(10), chr(92) + 'n')}\"\n\n"
    "def atoms : Array Atom := parseAtoms atomData\n\n"
    "end Square17\n")

samples_tsv = root / 'data/orientation_samples.tsv'
samples = [line.split() for line in open(samples_tsv) if line.strip()]
assert len(samples) == 148937
subset_idx = sorted(set(range(0, 148937, 1000)) | {1, 148935, 148936})
subset_lines = "\n".join(f"{samples[i][0]} {samples[i][1]}" for i in subset_idx)
(lean / 'Square17/SampleData.lean').write_text(
    f"-- Generated from data/orientation_samples.tsv (sha256 {sha(samples_tsv)}).\n"
    f"-- Subset: indices 0,1000,...,148000 plus 1, 148935, 148936 ({len(subset_idx)} samples).\n"
    "namespace Square17\n\n"
    f"def sampleSubsetCount : Nat := {len(subset_idx)}\n\n"
    f"def sampleSubsetData : String := \"{subset_lines.replace(chr(10), chr(92) + 'n')}\"\n\n"
    "end Square17\n")

full_lines = "\n".join(f"{p} {q}" for p, q in samples)
(lean / 'Square17/SampleDataFull.lean').write_text(
    f"-- Generated from data/orientation_samples.tsv (sha256 {sha(samples_tsv)}). All 148937 samples.\n"
    "namespace Square17\n\n"
    "def sampleFullCount : Nat := 148937\n\n"
    f"def sampleFullData : String := \"{full_lines.replace(chr(10), chr(92) + 'n')}\"\n\n"
    "end Square17\n")

print("wrote AtomData.lean, SampleData.lean, SampleDataFull.lean")
print("atoms.csv sha256:", sha(atoms_csv))
print("orientation_samples.tsv sha256:", sha(samples_tsv))
