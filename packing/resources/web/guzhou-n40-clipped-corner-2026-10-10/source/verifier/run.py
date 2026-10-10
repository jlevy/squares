"""401 个连续中心域的完整复验。
Complete replay of 401 continuous center domains.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from finite import PARAMS, PIN, candidate_bytes, finite_check, read_json, require, sha, validate_nodes

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser(description='完整复验 / Complete replay')
    ap.add_argument('--runtime', type=Path, required=True, help='已准备依赖的目录 / Directory with prepared dependencies')
    ap.add_argument('--workers', type=int, default=4, help='并行数 / Worker count')
    args = ap.parse_args()
    require(__debug__ and not os.environ.get('PYTHONOPTIMIZE'), 'ASSERTIONS_DISABLED')
    require(platform.system() == 'Linux' and 1 <= args.workers <= 16, 'RUNTIME_REQUIREMENTS')
    for name in ('RUSTFLAGS','CARGO_ENCODED_RUSTFLAGS','CARGO_BUILD_RUSTFLAGS','RUSTC_WRAPPER','RUSTC_WORKSPACE_WRAPPER'):
        require(not os.environ.get(name), 'UNREVIEWED_COMPILER_FLAGS')
    runtime = args.runtime.resolve()
    require(runtime != ROOT and ROOT not in runtime.parents, 'RUNTIME_MUST_BE_OUTSIDE_SOURCE')
    require((runtime/'vendor').is_dir() and not (runtime/'target').exists(), 'FRESH_PREPARED_RUNTIME_REQUIRED')
    out = runtime/'replay'
    out.mkdir(parents=True, exist_ok=False)
    source_files = sorted(p for folder in ('verifier','tests','certificate') for p in (ROOT/folder).rglob('*')
                          if p.is_file() and '__pycache__' not in p.parts)
    source_hashes = {p.relative_to(ROOT).as_posix():sha(p) for p in source_files}
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    parameters = read_json(ROOT/'certificate/parameters.json')
    positive, finite = finite_check(ROOT/'certificate/certified_candidate.json', parameters)
    candidate = out/'candidate-401.json'
    candidate.write_bytes(candidate_bytes(positive))
    candidate_digest = sha(candidate)
    env = os.environ.copy()
    env.update(PYTHONDONTWRITEBYTECODE='1', CARGO_HOME=str(runtime/'cargo'),
               CARGO_TARGET_DIR=str(runtime/'target'), CARGO_NET_OFFLINE='true')
    commands = []
    def execute(stage, command, cwd=ROOT):
        begin = time.monotonic()
        print(stage, flush=True)
        with (out/(stage+'.stdout')).open('wb') as stdout, (out/(stage+'.stderr')).open('wb') as stderr:
            process = subprocess.run(command, cwd=cwd, env=env, stdout=stdout, stderr=stderr)
        commands.append({'stage':stage, 'exit_code':process.returncode, 'seconds':time.monotonic()-begin,
                         'stdout_sha256':sha(out/(stage+'.stdout')), 'stderr_sha256':sha(out/(stage+'.stderr'))})
        (out/'stages.json').write_text(json.dumps(commands, indent=2)+'\n')
        if process.returncode:
            print((out/(stage+'.stderr')).read_text(errors='replace')[-12000:], file=sys.stderr)
        require(process.returncode == 0, 'STAGE_FAILED:'+stage)
    crate = ROOT/'verifier/sqverify_fast'
    config = ['--config','source.crates-io.replace-with="vendored-sources"',
              '--config','source.vendored-sources.directory='+json.dumps(str(runtime/'vendor'))]
    execute('python-tests', [sys.executable,'-B','-m','unittest','discover','-s','tests','-p','test_*.py','-v'])
    execute('rust-tests', ['cargo','test','--profile','gate-test','--locked','--offline',*config], crate)
    execute('rust-build', ['cargo','build','--release','--locked','--offline',*config], crate)
    binary = runtime/'target/release/sqverify-fast'
    node_dir = out/'nodes'
    execute('nodes-401', [str(binary),'--candidate',str(candidate),'--n','40','--side','67/10',
                         '--directions','all','--threshold','10001/10000','--threads',str(args.workers),
                         '--receipts',str(node_dir),'--confirm'])
    lines = [json.loads(line) for line in (out/'nodes-401.stdout').read_text().splitlines() if line.strip()]
    summaries = [z for z in lines if z.get('kind') == 'sqverify-fast-summary/v1']
    rows = sorted([z for z in lines if 'r' in z], key=lambda z:z['r'])
    require(len(summaries) == 1, 'SUMMARY_COUNT')
    summary = summaries[0]
    validate_nodes(summary, rows, candidate_digest)
    for row in rows:
        raw = json.loads((node_dir/('r%03d.json'%row['r'])).read_text())
        require(raw['certificate_sha256'] == candidate_digest, 'RAW_INPUT_IDENTITY')
        require({k:v for k,v in raw.items() if k != 'certificate_sha256'} == row, 'RAW_ROW_IDENTITY')
    require(source_hashes == {p.relative_to(ROOT).as_posix():sha(p) for p in source_files}, 'SOURCE_CHANGED')
    canonical = out/'nodes.jsonl'
    canonical.write_text(''.join(json.dumps(z, sort_keys=True, separators=(',',':'))+'\n' for z in rows))
    result = {'schema':'n40-public-verification/v2','status':'CODE_DISTINCT_FULL',
              'claim':'s(40) > 335427/50000','parameters':PARAMS,'finite':finite,
              'continuous_domains':401,'angle_step':'83/80000','threshold':'10001/10000',
              'source_candidate_sha256':PIN,'derived_candidate_sha256':candidate_digest,
              'nodes_sha256':sha(canonical),'binary_sha256':sha(binary),
              'code_and_input_sha256':source_hashes,'commands':commands,
              'rustc':subprocess.check_output(['rustc','--version'],env=env,text=True).strip(),
              'python':sys.version.split()[0], 'platform':'Linux',
              'started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'source_commit':os.environ.get('GITHUB_SHA'), 'node_summary':summary,
              'method_distinct_full':False,'formal_proof':False,'peer_reviewed':False}
    (out/'verification.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status':result['status'],'claim':result['claim'],'continuous_domains':401,
                      'simple_counting_margin':finite['simple_counting_margin'],
                      'result_sha256':sha(out/'verification.json')}, indent=2), flush=True)

if __name__ == '__main__':
    main()
