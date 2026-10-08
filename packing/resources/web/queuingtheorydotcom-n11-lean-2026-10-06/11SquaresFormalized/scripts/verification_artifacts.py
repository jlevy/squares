#!/usr/bin/env python3
"""Package allowlisted verification outputs and restore same-branch checkpoints."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

from verify_support import STANDARD_AXIOMS, native_axiom_owner, public_audit_status

ROOT = Path(__file__).resolve().parents[1]
MODULE = r'(?:ElevenSquare|Sqpack)(?:\.[A-Za-z0-9_]+)*'
RECEIPT = re.compile(MODULE + r'\.json\Z')
MEMBER = re.compile(
    r'(?:\.verification/' + MODULE + r'\.(?:json|log)|'
    r'\.lake/build/lib/lean/(?:ElevenSquare|Sqpack)(?:/[A-Za-z0-9_]+)*\.olean)\Z')
PROVED_STATUSES = {'OPTIMALITY_PROVED', 'OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES'}


def validated_success(result, audit):
    """Preserve finalized proof trust; a success label alone is insufficient."""
    admissions = audit.get('explicit_native_admissions')
    if type(admissions) is not int or admissions != 0:
        raise ValueError('Full proof acceptance requires zero admissions.')
    axioms = audit.get('axioms')
    if not isinstance(axioms, dict) or any(
            not isinstance(values, list) or any(not isinstance(a, str) or
                (a not in STANDARD_AXIOMS and native_axiom_owner(a) is None)
                for a in values) for values in axioms.values()):
        raise ValueError('Invalid final theorem axiom report.')
    expected = public_audit_status(axioms, admissions)
    count = audit.get('checked_modules')
    if type(count) is not int or count <= 0 or audit.get('full_upgrade_verified') is not True:
        raise ValueError('Invalid finalized module count or verification status.')
    for evidence in (result, audit):
        if (evidence.get('status') != expected['status'] or
                evidence.get('global_optimality_proved') is not True or
                evidence.get('checked_modules') != count or evidence.get('axioms') != axioms):
            raise ValueError('Final proof evidence does not agree.')
        # Kernel-only historical results may predate explicit trust metadata.
        for key in ('trust_model', 'native_certificate_axioms'):
            if (expected['native_certificate_axioms'] or key in evidence) and evidence.get(key) != expected[key]:
                raise ValueError('Final proof trust metadata does not agree.')
    return dict(expected, checked_modules=count, explicit_native_admissions=0)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(4 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def regular(root, path):
    return path.is_file() and not any(p.is_symlink() for p in [path, *path.parents]) and path.is_relative_to(root)


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def portable_member(member):
    member.uid = member.gid = 0
    member.uname = member.gname = ''
    return member


def package(root):
    root = root.resolve()
    state = root / '.verification'
    output = state / 'artifacts'
    output.mkdir(parents=True, exist_ok=True)
    evidence = output / 'evidence'
    evidence.mkdir(exist_ok=True)
    for name in ['result.json', 'final-audit.json']:
        (evidence / name).unlink(missing_ok=True)
    summary_path = state / 'runner-summary.json'
    summary = json.loads(summary_path.read_text()) if summary_path.is_file() else {'status': 'NOT_VERIFIED'}
    write_json(evidence / 'summary.json', summary)
    write_json(evidence / 'provenance.json', {
        'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip(),
        'run_id': os.environ.get('GITHUB_RUN_ID'),
        'run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
        'configuration_sha256': {name: sha(root / name) for name in
                                 ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']},
    })
    # A verifier result alone precedes finalization and is not final acceptance.
    if summary.get('status') in PROVED_STATUSES:
        finalized = {}
        for name in ['result.json', 'final-audit.json']:
            source = state / name
            if not regular(root, source):
                raise ValueError('Successful run is missing ' + name)
            finalized[name] = json.loads(source.read_text())
        expected = validated_success(finalized['result.json'], finalized['final-audit.json'])
        if any(summary.get(key) != value for key, value in expected.items()):
            raise ValueError('Runner summary does not match finalized proof trust.')
        for name in finalized:
            source = state / name
            shutil.copyfile(source, evidence / name)
    for name in ['lean-toolchain', 'lake-manifest.json', 'lakefile.lean']:
        shutil.copyfile(root / name, evidence / name)
    checkpoint = []
    rows = []
    for receipt in sorted(state.glob('*.json')):
        if not RECEIPT.fullmatch(receipt.name) or not regular(root, receipt):
            continue
        module = receipt.stem
        try:
            info = json.loads(receipt.read_text())
            if not isinstance(info, dict) or not isinstance(info.get('inputs', {}), dict):
                raise ValueError('Invalid receipt shape')
        except (ValueError, OSError):
            rows.append((module, 'unreadable_receipt', '', ''))
            continue
        rows.append((module, info.get('status'), info.get('elapsed_seconds', ''),
                     ' '.join(info.get('inputs', {}).get('arguments', []))))
        if info.get('status') != 'accepted' or info.get('module') != module:
            continue
        obj = root / '.lake/build/lib/lean' / (module.replace('.', '/') + '.olean')
        log = state / (module + '.log')
        if regular(root, obj) and regular(root, log) and sha(obj) == info.get('object_sha256'):
            checkpoint.extend([receipt, log, obj])
    with (evidence / 'module-timings.csv').open('w', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['module', 'status', 'recorded_compile_seconds', 'lean_arguments'])
        writer.writerows(rows)
    (evidence / 'README.txt').write_text(
        'summary.json is the current run status. OPTIMALITY_PROVED means the kernel-only audit passed;\n'
        'OPTIMALITY_PROVED_WITH_NATIVE_CERTIFICATES additionally trusts the Lean compiler for the listed numerical checks.\n'
        'final-audit.json contains source/configuration hashes and theorem axiom dependencies on success.\n'
        'module-timings.csv includes reused receipts; their times can come from earlier runs.\n'
        'Checkpoints accelerate verification; they are not independently a proof acceptance report.\n')
    # Explicit files only: never archive dependencies, Git metadata, credentials, or home directories.
    # Publish only a complete checkpoint. A packaging failure or cancellation
    # must not expose a partial tar or replace an earlier completed checkpoint.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output, prefix='.checkpoint-',
                                         suffix='.tar.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            with tarfile.open(fileobj=stream, mode='w') as archive:
                for path in checkpoint:
                    archive.add(path, arcname=path.relative_to(root).as_posix(),
                                recursive=False, filter=portable_member)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, output / 'checkpoint.tar')
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    diagnostic_paths = [p for p in state.glob('*') if
                        re.fullmatch(MODULE + r'\.(?:log|json)', p.name) or p.name in {
                            'runner-summary.json', 'result.json', 'incomplete-result.json',
                            'selected-result.json', 'final-audit.json'}]
    diagnostic_paths += [p for p in (state / 'runs').glob('*/*') if p.name in {
        'bootstrap.log', 'replay.log', 'finalize.log', 'plan.log', 'summary.json'}]
    with tarfile.open(output / 'diagnostics.tar', 'w') as archive:
        for path in sorted(diagnostic_paths):
            if regular(root, path):
                archive.add(path, arcname=path.relative_to(root).as_posix(), recursive=False, filter=portable_member)
    count = len(checkpoint) // 3
    print(f'Packaged evidence, diagnostics, and {count} accepted module checkpoints.')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as stream:
            stream.write(f'\nArtifact preparation: {count} accepted modules in the checkpoint. '
                         'See the run Artifacts section for uploads.\n')


def extract_checkpoint(root, archive_path):
    root = root.resolve()
    with tarfile.open(archive_path, 'r:*') as archive:
        members = archive.getmembers()
        seen = set()
        # Validate the entire archive before writing anything.
        for member in members:
            if not member.isfile() or not MEMBER.fullmatch(member.name) or member.name in seen:
                raise ValueError('Invalid checkpoint archive member')
            seen.add(member.name)
            target = root / member.name
            if any(p.is_symlink() for p in [target, *target.parents]):
                raise ValueError('Checkpoint target contains a symlink')
        for member in members:
            target = root / member.name
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.extractfile(member) as source, target.open('wb') as destination:
                shutil.copyfileobj(source, destination)
            # Preserve timestamps for older receipt compatibility.
            os.utime(target, (member.mtime, member.mtime))
    print(f'Restored {len(members)} checkpoint files; verifier will validate receipts before reuse.')


def gh_json(endpoint):
    return json.loads(subprocess.check_output(['gh', 'api', endpoint], text=True))


def restore(root, run_id):
    repository = os.environ['GITHUB_REPOSITORY']
    branch = os.environ['GITHUB_REF_NAME']
    current = os.environ['GITHUB_RUN_ID']
    if run_id != 'auto' and not re.fullmatch(r'[1-9][0-9]*', run_id):
        raise ValueError('resume_run must be auto or a positive run ID')
    if run_id == 'auto':
        artifacts = gh_json(f'repos/{repository}/actions/artifacts?name=proof-checkpoint&per_page=100')['artifacts']
        candidates = [a['workflow_run']['id'] for a in artifacts if not a['expired']
                      and a['workflow_run']['head_branch'] == branch
                      and str(a['workflow_run']['id']) != current]
    else:
        candidates = [int(run_id)]
    for candidate in dict.fromkeys(candidates):
        run = gh_json(f'repos/{repository}/actions/runs/{candidate}')
        if (run['status'] != 'completed' or run['head_branch'] != branch
                or run['path'] != '.github/workflows/verify.yml'
                or run['event'] != 'workflow_dispatch'):
            if run_id != 'auto':
                raise ValueError('Checkpoint must come from a completed manual verification on this branch')
            continue
        destination = root / '.verification/restore'
        destination.mkdir(parents=True, exist_ok=True)
        subprocess.run(['gh', 'run', 'download', str(candidate), '--repo', repository,
                        '--name', 'proof-checkpoint', '--dir', str(destination)], check=True)
        extract_checkpoint(root, destination / 'checkpoint.tar')
        shutil.rmtree(destination)
        print(f'Checkpoint downloaded from run {candidate}.')
        return
    print('No previous same-branch checkpoint available; starting a new build.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['package', 'restore', 'extract'])
    parser.add_argument('--run', default='auto')
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    if args.command == 'package':
        package(ROOT)
    elif args.command == 'restore':
        restore(ROOT, args.run)
    else:
        if not args.archive:
            parser.error('extract requires --archive')
        extract_checkpoint(ROOT, args.archive)


if __name__ == '__main__':
    main()
