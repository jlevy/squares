#!/usr/bin/env python3
"""Exactly regenerate this one certificate from the pinned Hosono source."""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from math import isqrt
from pathlib import Path
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
SOURCE_JSON = '64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a'
CANDIDATE_JSON = 'd1df3bc69bb12c0eebcb51d6b3636593079fbb82ae1128938ec5c07c83cc951c'
CANDIDATE_GZIP = 'f59d4c9562d7246f41c8c389a5bc118da9cf268a794e6416d146a195fb03360c'
VERIFIER_SOURCE = 'd97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88'

class PacketError(Exception):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(detail)

def require(condition, code, detail):
    if not condition:
        raise PacketError(code, detail)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def deterministic_gzip(raw):
    data = bytearray(gzip.compress(raw, compresslevel=9, mtime=0))
    data[9] = 255  # Fix the gzip OS byte across Python versions; no file-name header.
    return bytes(data)

def regenerate():
    source = gzip.decompress((ROOT / 'source/hosono-candidate.json.gz').read_bytes())
    require(sha(source) == SOURCE_JSON, 'source_digest', 'Hosono JSON digest mismatch')
    d = json.loads(source, parse_float=str, parse_int=str)
    require(F(d['L']) == F(199,20) and F(d['B']) == F(9977,10000),
            'source_parameters', 'unexpected source side/core')
    lam = F(4986,4975)
    d['n'] = 94
    d['L'] = str(F(d['L']) * lam)
    d['B'] = str(F(d['B']) * lam)
    last = isqrt(2 * 12000**2) - 12000 + 1
    d['proof_net'] = {'step': '1/12000', 'last': last}
    d['rectangles'] = [dict(rectangle=[str(F(x) * lam) for x in r['rectangle']],
                            mass=r['mass']) for r in d['rectangles']]
    d['derived_from'] = 'Hiroaki Hosono (wand125), mixed_n94_L995; exact similarity 4986/4975'
    del d['scaling_source_digest']
    del d['scaling_factor']
    raw = json.dumps(d, sort_keys=True, separators=(',', ':')).encode('utf-8')
    require(sha(raw) == CANDIDATE_JSON, 'regeneration_json_digest', 'canonical JSON mismatch')
    compressed = deterministic_gzip(raw)
    require(sha(compressed) == CANDIDATE_GZIP, 'regeneration_gzip_digest',
            'gzip mismatch: this exact archive requires a matching zlib deflate stream; JSON identity is checked separately')
    return raw, compressed

def source_digest():
    root = ROOT / 'verifier/sqverify_fast'
    names = ['Cargo.toml', 'Cargo.lock', 'build.rs'] + sorted(
        'src/' + p.name for p in (root/'src').glob('*.rs'))
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode()); digest.update(b'\0')
        digest.update((root/name).read_bytes()); digest.update(b'\0')
    return digest.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='new output directory')
    args = parser.parse_args()
    raw, compressed = regenerate()
    args.output.mkdir(parents=True, exist_ok=True)
    outputs = [('n94-L9972.json',raw), ('n94-L9972.json.gz',compressed)]
    require(all(not (args.output/name).exists() for name,_ in outputs),
            'output_exists', 'regeneration outputs must be new')
    for name, data in outputs:
        (args.output/name).write_bytes(data)
    print(json.dumps(dict(status='REGENERATED', json_sha256=sha(raw), gzip_sha256=sha(compressed),
                         python=sys.version.split()[0], zlib=zlib.ZLIB_RUNTIME_VERSION)))

if __name__ == '__main__':
    try:
        main()
    except PacketError as error:
        print(json.dumps(dict(status='ERROR', code=error.code, detail=error.detail)), file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, KeyError, TypeError, EOFError, zlib.error) as error:
        print(json.dumps(dict(status='ERROR', code='input_or_io', detail=str(error))), file=sys.stderr)
        sys.exit(1)
