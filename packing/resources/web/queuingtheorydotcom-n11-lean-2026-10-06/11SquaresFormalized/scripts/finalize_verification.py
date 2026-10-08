#!/usr/bin/env python3
"""Validate a completed full replay; --write saves portable evidence and manifest.

Run after the final source/documentation edits and `verify.py --all` succeeds.
Stage intended new files first. This invokes no Lean and reuses no historical
pass claim: it checks current source/configuration/object hashes and every
receipt and axiom query. Historical provenance and focused audits stay intact.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
from check_sources import ROOT, check, code_only, imports
from native_certificates import (load_native_manifest, native_declarations,
                                 validate_native_source)
from verify_support import (STANDARD_AXIOMS, admitted_targets, public_audit_status,
                            audit_axioms, input_digest, priority_order, recorded_arguments)

OUTPUTS = {'verification/wand125-upgrade.json', 'verification/source-check.json', 'MANIFEST.json'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(4 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2) + '\n').encode()


def collect_audit(root, source_check):
    """Verify the complete receipt graph before producing any portable output."""
    state = root / '.verification'
    result = json.loads((state / 'result.json').read_text(encoding='utf-8'))
    paths = (sorted((root / 'ElevenSquare').rglob('*.lean')) +
             sorted((root / 'Sqpack').rglob('*.lean')) +
             [root / 'ElevenSquare.lean', root / 'Sqpack.lean'])
    modules = {'.'.join(p.relative_to(root).with_suffix('').parts): p for p in paths}
    require(result.get('status') in {'PARTIAL_ASSEMBLY_COMPILES', 'OPTIMALITY_PROVED',
                                    'OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES'},
            'No successful full-project verifier result; run scripts/verify.py --all.')
    require(result.get('checked_modules') == len(modules),
            'The verifier result does not cover every current local module.')
    admissions = json.loads((root / 'verification/admissions.json').read_text(encoding='utf-8'))['sites']
    unfinished = admitted_targets(admissions)
    admission_count = len(admissions)
    native_manifest = load_native_manifest(root)
    approved_native = native_declarations(native_manifest)
    native_paths = set(native_manifest.get('files', {}))
    require(native_paths <= {p.relative_to(root).as_posix() for p in paths},
            'Missing inventoried native certificate sources.')
    require(source_check.get('status') == 'SOURCE_ASSEMBLY_PASS'
            and source_check.get('local_modules') == len(modules)
            and source_check.get('explicit_admissions') == admission_count,
            'The source check must accept the full tree and exactly the inventoried admissions.')

    context = {p: sha(root / p) for p in ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']}
    toolchain = (root / 'lean-toolchain').read_text(encoding='utf-8').strip()
    version = toolchain.rsplit(':v', 1)[-1]
    manifest = json.loads((root / 'lake-manifest.json').read_text(encoding='utf-8'))
    mathlib = next(p['rev'] for p in manifest['packages'] if p['name'] == 'mathlib')
    dependencies = {m: [d for d in imports(p) if d in modules] for m, p in modules.items()}
    order = priority_order(dependencies, {m: p.stat().st_size for m, p in modules.items()})
    source_hashes = {}; object_hashes = {}; input_ids = {}; axioms = {}
    compiler = None
    for m in order:
        receipt = json.loads((state / (m + '.json')).read_text(encoding='utf-8'))
        require(receipt.get('status') == 'accepted', 'Unaccepted module: ' + m)
        recorded = receipt.get('inputs', {})
        if compiler is None:
            compiler = recorded.get('compiler', '')
            parsed = re.search(r'\bversion ([^,]+),', compiler)
            require(parsed is not None and parsed[1] == version, 'Compiler/toolchain mismatch.')
        source = modules[m].read_bytes()
        # Revalidate permissions against actual source bytes. The finalizer must
        # not accept a caller-provided source-check summary as a native audit.
        validate_native_source(modules[m].relative_to(root).as_posix(), source, native_manifest)
        source_hashes[m] = hashlib.sha256(source).hexdigest()
        current = {
            'source': source_hashes[m],
            'local_dependency_objects': {d: object_hashes[d] for d in dependencies[m]},
            'compiler': compiler,
            'arguments': recorded_arguments(m, recorded.get('arguments')),
            'build_context': context,
            'local_dependency_inputs': {d: input_ids[d] for d in dependencies[m]},
        }
        require(recorded == current, 'Stale source/configuration/dependency receipt: ' + m)
        target = root / '.lake/build/lib/lean' / (m.replace('.', '/') + '.olean')
        object_hashes[m] = sha(target)
        require(receipt.get('object_sha256') == object_hashes[m], 'Changed compiled object: ' + m)
        input_ids[m] = input_digest(current)
        log = state / (m + '.log')
        require(log.is_file(), 'Missing compiler log: ' + m)
        if b'#print' in source:
            axioms.update(audit_axioms(code_only(source.decode()), log.read_text(encoding='utf-8'),
                                      STANDARD_AXIOMS, unfinished, approved_native))
    status = public_audit_status(axioms, admission_count)
    require(axioms == result.get('axioms'), 'Verifier result does not match the current axiom logs.')
    require(result.get('status') == status['status']
            and result.get('global_optimality_proved') is status['global_optimality_proved'],
            'Verifier proof status does not match the current admission inventory and axiom logs.')
    # Historical kernel-only receipts remain usable. Native results must carry
    # the complete explicit trust declaration, never a historical clean label.
    if status['native_certificate_axioms']:
        require(result.get('trust_model') == status['trust_model'] and
                result.get('native_certificate_axioms') == status['native_certificate_axioms'],
                'Verifier native trust disclosure does not match the current axiom logs.')
    return {
        **status,
        'scope': f'All local ElevenSquare and Sqpack modules; {admission_count} inventoried admissions remain.',
        'checked_modules': len(modules), 'lean_toolchain': toolchain, 'mathlib_revision': mathlib,
        'full_upgrade_verified': True,
        'explicit_native_admissions': admission_count,
        'native_certificate_manifest_sha256': hashlib.sha256(
            json.dumps(native_manifest, sort_keys=True).encode()).hexdigest(),
        'build_context_sha256': context, 'source_sha256': dict(sorted(source_hashes.items())),
        'axioms': dict(sorted(axioms.items())),
    }


def publication(root, audit, source_check):
    """Prepare the full manifest in memory before modifying any evidence file."""
    def git_paths(*args):
        data = subprocess.check_output(['git', 'ls-files', *args, '-z'], cwd=root)
        return {p.decode() for p in data.split(b'\0') if p}
    tracked = git_paths('--cached')
    untracked = git_paths('--others', '--exclude-standard') - OUTPUTS
    require(not untracked, 'Stage intended new files before finalization: ' + ', '.join(sorted(untracked)))
    payloads = {'verification/wand125-upgrade.json': json_bytes(audit),
                'verification/source-check.json': json_bytes(source_check)}
    entries = []
    for rel in sorted((tracked | set(payloads)) - {'MANIFEST.json'}):
        path = root / rel
        require(rel in payloads or path.is_file(), 'Missing tracked file; stage its removal: ' + rel)
        if rel in payloads:
            data = payloads[rel]
            size, digest = len(data), hashlib.sha256(data).hexdigest()
        else:
            size, digest = path.stat().st_size, sha(path)
        entries.append({'path': rel, 'bytes': size, 'sha256': digest})
    payloads['MANIFEST.json'] = json_bytes({'format': 'sha256-source-manifest-v1', 'files': entries})
    return payloads


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Save verified portable evidence and refresh MANIFEST.json.')
    args = parser.parse_args()
    # Missing/incomplete full results fail before the source scan.
    result_path = ROOT / '.verification/result.json'
    require(result_path.is_file(), 'No full-build result exists; complete scripts/verify.py --all first.')
    source_check = check(use_cache=True)
    audit = collect_audit(ROOT, source_check)
    # Preserve the destination runner's audited, machine-local evidence file.
    report = ROOT / '.verification/final-audit.json'
    temporary_report = report.with_name(report.name + f'.{os.getpid()}.tmp')
    try:
        temporary_report.write_bytes(json_bytes(audit))
        temporary_report.replace(report)
    finally:
        temporary_report.unlink(missing_ok=True)
    if args.write:
        payloads = publication(ROOT, audit, source_check)
        for rel, data in payloads.items():
            path = ROOT / rel
            temporary = path.with_name(path.name + f'.{os.getpid()}.tmp')
            try:
                temporary.write_bytes(data)
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
        print('Saved ' + ', '.join(payloads) + '.')
    proof = 'verified' if audit['global_optimality_proved'] else 'unfinished'
    print(f"Validated {audit['checked_modules']} modules; {audit['explicit_native_admissions']} "
          f"admissions remain; global optimality is {proof}.")
    if not args.write:
        print('No portable evidence changed. Use --write to publish the audit and source manifest.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        raise SystemExit('Finalization refused: ' + str(error)) from error
