#!/usr/bin/env python3
"""Negative contract tests: corruption must not become archive success."""
import argparse
import copy
import gzip
import json
from pathlib import Path
import shutil
import tempfile
import sys

import audit
import rescale
from rescale import PacketError, deterministic_gzip, sha

ORIGINAL_ROOT = audit.ROOT

def write_json(path, value):
    path.write_text(json.dumps(value,indent=2)+'\n')

def alter_merged(root, change):
    path = root/'receipts/directions.jsonl.gz'
    lines = gzip.decompress(path.read_bytes()).splitlines(keepends=True)
    change(lines)
    raw = b''.join(lines)
    compressed = deterministic_gzip(raw)
    path.write_bytes(compressed)
    index_path = root/'receipts/INDEX.json'
    index = json.loads(index_path.read_text())
    index['merged_gzip_sha256'],index['merged_jsonl_sha256'] = sha(compressed),sha(raw)
    write_json(index_path,index)

def duplicate(root):
    def change(lines): lines[1] = lines[0]
    alter_merged(root,change)

def alter_row(root, key, value):
    def change(lines):
        row = json.loads(lines[0]); row[key] = value
        lines[0] = (json.dumps(row,separators=(',',':'))+'\n').encode()
    alter_merged(root,change)

def wrong_native_identity(root):
    index_path = root/'receipts/INDEX.json'; index = json.loads(index_path.read_text())
    ev = index['sources'][0]
    path = root/ev['receipt_file']; rows = [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]
    rows[-1]['build']['source_sha256'] = '0'*64
    raw = ''.join(json.dumps(row,separators=(',',':'))+'\n' for row in rows).encode()
    path.write_bytes(deterministic_gzip(raw))
    ev['archive_sha256'],ev['uncompressed_sha256'] = sha(path.read_bytes()),sha(raw)
    write_json(root/ev['summary_file'],rows[-1]);write_json(index_path,index)

def wrong_source_code(root):
    path = root/'verifier/sqverify_fast/src/main.rs'
    path.write_bytes(path.read_bytes()+b'\n')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    cases = [('duplicate_direction',duplicate,'exhaustive_unique'),
             ('out_of_range_direction',lambda root:alter_row(root,'r',4972),'exhaustive_unique'),
             ('nonfinite_bound',lambda root:alter_row(root,'min_certified_lower_bound',float('nan')),'native_bound'),
             ('subthreshold_bound',lambda root:alter_row(root,'min_certified_lower_bound',0.999),'native_bound'),
             ('wrong_native_source_identity',wrong_native_identity,'native_source'),
             ('modified_verifier_source',wrong_source_code,'source_digest')]
    results = []
    with tempfile.TemporaryDirectory(prefix='s94-audit-negative-') as folder:
        pristine = Path(folder)/'pristine'
        shutil.copytree(ORIGINAL_ROOT,pristine,ignore=shutil.ignore_patterns('.git','target','__pycache__'))
        for name,change,expected in cases:
            fixture = Path(folder)/name;shutil.copytree(pristine,fixture)
            change(fixture)
            audit.ROOT = rescale.ROOT = fixture
            try:
                audit.audit(check_manifest=False)
            except PacketError as error:
                if error.code != expected:
                    raise PacketError('negative_test_wrong_error',name+': '+error.code)
                results.append(dict(test=name,status='REJECTED_AS_REQUIRED',code=error.code))
            else:
                raise PacketError('negative_test_false_accept',name)
            finally:
                audit.ROOT = rescale.ROOT = ORIGINAL_ROOT
    result = dict(status='NEGATIVE_TESTS_PASSED',tests=results,
                  note='Corrupt fixture archive hashes were recomputed, so semantic gates, not only stale manifest hashes, cause these refusals.')
    text = json.dumps(result,indent=2)+'\n'
    if args.output is not None:args.output.write_text(text)
    print(text,end='')

if __name__ == '__main__':
    try:
        main()
    except PacketError as error:
        print(json.dumps(dict(status='ERROR',code=error.code,detail=error.detail)),file=sys.stderr)
        sys.exit(1)
