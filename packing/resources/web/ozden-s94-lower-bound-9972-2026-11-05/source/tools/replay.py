#!/usr/bin/env python3
"""Build the pinned unmodified Rust verifier and perform a fresh numerical replay."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

from audit import check_premises, check_row, native_stream
from rescale import ROOT, CANDIDATE_GZIP, VERIFIER_SOURCE, PacketError, require, sha, source_digest
from fractions import Fraction as F

def parse_scope(text):
    if text == 'all':return list(range(4972))
    scope = []
    for part in text.split(','):
        if '-' in part:
            pieces = part.split('-')
            require(len(pieces) == 2,'replay_scope','bad range')
            a,b = map(int,pieces)
            require(a <= b,'replay_scope','reversed range')
            scope.extend(range(a,b+1))
        else:scope.append(int(part))
    require(bool(scope) and len(scope) == len(set(scope)) and all(0 <= r < 4972 for r in scope),
            'replay_scope','scope must be nonempty, unique and within 0..4971')
    return sorted(scope)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directions', required=True, help='all, inclusive a-b, or comma list')
    parser.add_argument('--threads', type=int, required=True)
    parser.add_argument('--timeout-seconds', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True, help='new output directory')
    parser.add_argument('--mutant', action='store_true', help='negative-control replay, requiring explicit directions 0,1198')
    args = parser.parse_args()
    scope = parse_scope(args.directions)
    require(args.threads > 0 and args.timeout_seconds > 0, 'replay_limits','positive threads/timeout required')
    require(not args.output.exists(), 'output_exists','replay output must be new')
    require(source_digest() == VERIFIER_SOURCE, 'source_digest','verifier source modified')
    candidate = ROOT/('controls/mass-99-100.json.gz' if args.mutant else 'certificate/n94-L9972.json.gz')
    input_sha = sha(candidate.read_bytes())
    expected_sha = '2f72d2ddedd70e6be97fa58494b8508eb3020c2e8bbad5b2f429cac134c01532' if args.mutant else CANDIDATE_GZIP
    require(input_sha == expected_sha,'candidate_digest','unexpected replay input')
    if args.mutant:require(scope == [0,1198],'mutant_scope','mutant replay requires 0,1198')
    cargo = shutil.which('cargo')
    require(cargo is not None,'toolchain_unavailable','Install rustup with the pinned Rust 1.98.0 toolchain and cargo; source files must remain unchanged')
    args.output.mkdir(parents=True)
    crate = ROOT/'verifier/sqverify_fast'
    with (args.output/'build.log').open('w') as log:
        build = subprocess.run([cargo,'build','--locked','--release','--manifest-path',str(crate/'Cargo.toml')],
                               cwd=crate,stdout=log,stderr=subprocess.STDOUT,timeout=600)
    require(build.returncode == 0,'build_failed','see output build.log; no source edits or compiler downgrade applied')
    binary = crate/'target/release/sqverify-fast'
    command = [str(binary),'--candidate',str(candidate),'--n','94','--directions',args.directions,
               '--threshold','1','--threads',str(args.threads),'--confirm']
    with (args.output/'native.jsonl').open('w') as stream,(args.output/'stderr.log').open('w') as errorlog:
        process = subprocess.run(command,stdout=stream,stderr=errorlog,timeout=args.timeout_seconds)
    rows,summary = native_stream((args.output/'native.jsonl').read_bytes())
    mass = F(930599901,10000000) if args.mutant else F(9399999,100000)
    check_premises(summary,input_sha,mass)
    observed = [row['r'] for row,_ in rows]
    require(sorted(observed) == scope and len(observed) == len(set(observed)) and summary['directions'] == len(scope),
            'replay_scope','native replay did not decide exactly requested directions')
    if args.mutant:
        require(process.returncode == 1 and summary['status'] == 'REFUSED' and summary['refused_directions'] == [0,1198] and
                all(row['verdict'] != 'verified' for row,_ in rows), 'mutant_replay_failed','mutant did not refuse')
        status = 'FRESH_MUTANT_REPLAY_REFUSED_AS_REQUIRED'
    else:
        for row,_ in rows:check_row(row)
        expected_status = 'VERIFIED' if scope == list(range(4972)) else 'PARTIAL'
        require(process.returncode == 0 and summary['status'] == expected_status and not summary['refused_directions'],
                'replay_refused','native replay did not verify')
        status = 'FRESH_FULL_NET_REPLAY_VERIFIED' if expected_status == 'VERIFIED' else 'FRESH_SAMPLE_REPLAY_VERIFIED'
    result = dict(status=status,returncode=process.returncode,directions=len(scope),scope=scope,
                  input_sha256=input_sha,source_sha256=VERIFIER_SOURCE,native_summary=summary)
    text = json.dumps(result,indent=2)+'\n';(args.output/'verification.json').write_text(text)
    print(text,end='')

if __name__ == '__main__':
    try:
        main()
    except PacketError as error:
        print(json.dumps(dict(status='ERROR',code=error.code,detail=error.detail)),file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(json.dumps(dict(status='ERROR',code='replay_timeout',detail='Replay/build deadline reached; partial logs are not success')),file=sys.stderr)
        sys.exit(1)
    except (OSError,ValueError,KeyError,TypeError) as error:
        print(json.dumps(dict(status='ERROR',code='input_or_io',detail=str(error))),file=sys.stderr)
        sys.exit(1)
