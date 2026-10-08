#!/usr/bin/env python3
"""Serial Lean replay and axiom audit of the partially formalized repository."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
sys.dont_write_bytecode = True
# Redirected Windows streams otherwise use a legacy code page. Lean diagnostics
# and declaration names are UTF-8, including when a failed check is printed.
for stream in (sys.stdout, sys.stderr):
    stream.reconfigure(encoding='utf-8')
import time
from check_sources import ROOT, check, code_only, imports
from native_certificates import load_native_manifest, native_declarations
from verify_support import (STANDARD_AXIOMS, admitted_targets, public_audit_status,
                            priority_order, input_digest, reusable_fingerprint, audit_axioms,
                            positive_jobs, lean_arguments, native_trust_status)

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--setup', action='store_true', help='Restore pinned generated sources, toolchain, and dependency cache.')
ap.add_argument('--all', action='store_true', help='Check every included local source module.')
ap.add_argument('--keep-going', action='store_true', help='Continue independent modules after a failure; never accepts an incomplete build.')
ap.add_argument('--fresh', action='store_true', help='Ignore this checkout\'s matching accepted receipts.')
ap.add_argument('--jobs', type=positive_jobs, default=1,
                help='Worker threads within each new Lean process (default: 1); matching receipts retain their recorded count. Modules still compile serially.')
ap.add_argument('--plan', action='store_true', help='Print dependency order without installing or compiling.')
ap.add_argument('--module', action='append', default=[], help='Check only this module and its dependencies (repeatable).')
args = ap.parse_args()
if args.setup and not args.plan:
    from materialize_wand125 import materialize, materialize_bundled_baseline
    materialize()
    materialize_bundled_baseline()
print(json.dumps(check(use_cache=not args.fresh)), flush=True)
native_manifest = load_native_manifest(ROOT)
approved_native = native_declarations(native_manifest)
admissions = json.loads((ROOT / 'verification/admissions.json').read_text(encoding='utf-8'))['sites']
try:
    unfinished = admitted_targets(admissions)
except ValueError as error:
    raise SystemExit(str(error)) from error
files = sorted((ROOT / 'ElevenSquare').rglob('*.lean')) + sorted((ROOT / 'Sqpack').rglob('*.lean')) + [ROOT / 'ElevenSquare.lean', ROOT / 'Sqpack.lean']
modules = {'.'.join(p.relative_to(ROOT).with_suffix('').parts): p for p in files}
order = []; done = set()
def visit(m):
    if m in done or m not in modules: return
    for dep in imports(modules[m]): visit(dep)
    done.add(m); order.append(m)
if args.all:
    for m in sorted(modules):
        if m != 'ElevenSquare.Verification': visit(m)
if args.module:
    for m in args.module:
        if m not in modules: raise SystemExit('Unknown local module: ' + m)
        visit(m)
else:
    visit('ElevenSquare.Verification')
selected = set(order)
dependencies = {m: [d for d in imports(modules[m]) if d in selected] for m in selected}
order = priority_order(dependencies, {m: modules[m].stat().st_size for m in selected})
if args.plan:
    print('Serial local module checks:', len(order))
    print('\n'.join(order))
    raise SystemExit(0)

state = ROOT / '.verification'
state.mkdir(exist_ok=True)
child = None
signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))
def run(command, **kwargs):
    global child
    child = subprocess.Popen(command, cwd=ROOT, **kwargs)
    try:
        code = child.wait()
    except BaseException:
        child.terminate()
        try: child.wait(timeout=3)
        except subprocess.TimeoutExpired:
            child.kill(); child.wait()
        raise
    finally:
        child = None
    if code: raise SystemExit(code)

bin_dir = Path(os.environ.get('ELAN_HOME', Path.home() / '.elan')) / 'bin'
env = os.environ.copy()
if bin_dir.is_dir(): env['PATH'] = str(bin_dir) + os.pathsep + env.get('PATH', '')
elan = shutil.which('elan', path=env['PATH'])
lake = shutil.which('lake', path=env['PATH'])
if not elan or not lake:
    raise SystemExit('Install elan and make its bin directory available, then retry.')
if args.setup:
    run([elan, 'toolchain', 'install', (ROOT / 'lean-toolchain').read_text(encoding='utf-8').strip()], env=env)
    run([lake, 'exe', 'cache', 'get'], env=env)
# Read only the scoped Lean executable/path, not the full user environment.
runtime = json.loads(subprocess.check_output(
    [lake, 'env', sys.executable, '-c',
     "import os,shutil,json; print(json.dumps({'lean':shutil.which('lean'), 'path':os.environ.get('LEAN_PATH','')}))"],
    cwd=ROOT, env=env, text=True, encoding='utf-8'))
lean_env = env.copy(); lean_env['LEAN_PATH'] = runtime['path']
version = subprocess.check_output([runtime['lean'], '--version'], cwd=ROOT, env=lean_env,
                                  text=True, encoding='utf-8').strip()
if '4.34.1' not in version:
    raise SystemExit('Unexpected Lean version; use the pinned lean-toolchain.')

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(4 << 20), b''): h.update(b)
    return h.hexdigest()

def object_path(m): return ROOT / '.lake/build/lib/lean' / (m.replace('.', '/') + '.olean')

config_paths = [ROOT / p for p in ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']]
build_context = {p.name: sha(p) for p in config_paths}
config_modified_at = max(p.stat().st_mtime_ns for p in config_paths)
historical = json.loads((ROOT / 'verification/wand125-integration.json').read_text(encoding='utf-8'))
manifest = json.loads((ROOT / 'lake-manifest.json').read_text(encoding='utf-8'))
legacy_baseline = (
    historical.get('lean_toolchain') == (ROOT / 'lean-toolchain').read_text(encoding='utf-8').strip()
    and historical.get('mathlib_revision') == next(
        (p.get('rev') for p in manifest['packages'] if p['name'] == 'mathlib'), None))
input_ids = {}; checked_times = {}
accepted = 0
failed = []; blocked = {}
for index, m in enumerate(order):
    src = modules[m]; rel = str(src.relative_to(ROOT)); target = object_path(m)
    target.parent.mkdir(parents=True, exist_ok=True)
    receipt = state / (m + '.json'); log = state / (m + '.log')
    local_deps = [d for d in imports(src) if d in modules]
    unavailable = [d for d in local_deps if d in failed or d in blocked]
    if unavailable:
        blocked[m] = unavailable
        print(f'[{index+1}/{len(order)}] blocked {m}', flush=True)
        continue
    deps = {d: sha(object_path(d)) for d in local_deps}
    fingerprint = {'source': sha(src), 'local_dependency_objects': deps, 'compiler': version,
                   'arguments': lean_arguments(m, args.jobs),
                   'build_context': build_context,
                   'local_dependency_inputs': {d: input_ids[d] for d in local_deps}}
    old = json.loads(receipt.read_text(encoding='utf-8')) if receipt.is_file() else {}
    old_checked_at = old.get('checked_at_ns', receipt.stat().st_mtime_ns if receipt.is_file() else 0)
    dependency_checked_at = max([config_modified_at] + [checked_times[d] for d in local_deps])
    old_files_modified_at = max([dependency_checked_at] +
        [p.stat().st_mtime_ns for p in [target, log] if p.is_file()])
    cached_fingerprint = reusable_fingerprint(
        m, old.get('inputs'), fingerprint, legacy_baseline=legacy_baseline,
        checked_at=old_checked_at, newest_input=old_files_modified_at)
    if (not args.fresh and target.is_file() and old.get('status') == 'accepted'
            and cached_fingerprint is not None
            and old.get('object_sha256') == sha(target)
            and log.is_file()):
        if old.get('inputs') != cached_fingerprint:
            old.update(inputs=cached_fingerprint, checked_at_ns=old_checked_at)
            receipt.write_text(json.dumps(old, indent=2)+'\n', encoding='utf-8')
        input_ids[m] = input_digest(cached_fingerprint)
        checked_times[m] = max(old_checked_at, dependency_checked_at)
        print(f'[{index+1}/{len(order)}] cached {m}', flush=True)
        accepted += 1; continue
    tmp = target.with_name(target.name + '.checking')
    started = time.monotonic()
    print(f'[{index+1}/{len(order)}] checking {m}', flush=True)
    try:
        # Lean writes UTF-8 bytes directly; never transcode its evidence logs.
        with log.open('wb') as stream:
            run([runtime['lean'], '--root=.', *fingerprint['arguments'],
                 '-o', str(tmp.relative_to(ROOT)), rel], env=lean_env,
                stdout=stream, stderr=subprocess.STDOUT)
        os.replace(tmp, target)
    except BaseException as error:
        if tmp.exists(): tmp.unlink()
        receipt.write_text(json.dumps({'module':m, 'status':'failed_or_interrupted', 'inputs':fingerprint}, indent=2)+'\n', encoding='utf-8')
        print(log.read_text(encoding='utf-8')[-4000:], file=sys.stderr, flush=True)
        if args.keep_going and isinstance(error, SystemExit):
            failed.append(m)
            print(f'[{index+1}/{len(order)}] failed {m}', flush=True)
            continue
        raise
    checked_at = time.time_ns()
    receipt.write_text(json.dumps({'module':m, 'status':'accepted', 'inputs':fingerprint,
                                  'checked_at_ns': checked_at,
                                  'object_sha256':sha(target), 'elapsed_seconds':round(time.monotonic()-started, 2)}, indent=2)+'\n', encoding='utf-8')
    input_ids[m] = input_digest(fingerprint)
    checked_times[m] = max(checked_at, dependency_checked_at)
    accepted += 1
    print(f'[{index+1}/{len(order)}] accepted {m}', flush=True)

if failed or blocked:
    result = {'status': 'INCOMPLETE_BUILD', 'checked_modules': accepted,
              'failed_modules': failed, 'blocked_modules': blocked}
    (state / 'incomplete-result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(f'Incomplete build: {len(failed)} failed, {len(blocked)} blocked, {accepted} accepted.', flush=True)
    raise SystemExit(1)

def audit(module):
    source = modules[module].read_text(encoding='utf-8')
    if '#print' not in source:
        return {}
    try:
        return audit_axioms(code_only(source),
                            (state / (module + '.log')).read_text(encoding='utf-8'),
                            STANDARD_AXIOMS, unfinished, approved_native)
    except ValueError as error:
        raise SystemExit(module + ': ' + str(error)) from error

axioms = {}
for m in order:
    axioms.update(audit(m))

if args.module:
    selected_native = sorted(rel for rel in native_manifest['files']
                             if '.'.join(Path(rel).with_suffix('').parts) in selected)
    result = {'status': 'SELECTED_MODULES_COMPILE', 'checked_modules': accepted,
              'targets': args.module, 'axioms': axioms,
              'native_certificate_sources': selected_native,
              **native_trust_status(axioms, has_native_sources=bool(selected_native))}
    (state / 'selected-result.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
    raise SystemExit(0)

try:
    status = public_audit_status(axioms, len(admissions))
except ValueError as error:
    raise SystemExit(str(error)) from error
result = dict(status, checked_modules=accepted,
              axioms={n: sorted(values) for n, values in axioms.items()})
(state / 'result.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
print(json.dumps(result,indent=2))
if result['global_optimality_proved']:
    if result['trust_model'] == 'lean_kernel_and_native_compiler':
        print('Global optimality verified with compiled numerical certificates; '
              'the recorded native evaluations additionally trust the Lean compiler. No admissions remain.')
    else:
        print('Global optimality verified with no inventoried admissions and clean public axiom audits.')
else:
    print('Partial assembly accepted. See MISSING.md for the remaining proof obligations.')
