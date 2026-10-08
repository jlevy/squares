#!/usr/bin/env bash
# Linux/macOS entry point; --bootstrap supports Linux x86_64 and aarch64.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
exec python3 - "$@" <<'PY'
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
import tarfile
import time

sys.path.insert(0, str(Path.cwd() / 'scripts'))
from verification_artifacts import validated_success


def threads(value):
    if not re.fullmatch(r'[1-9][0-9]*', value) or not 1 <= int(value) <= 64:
        raise argparse.ArgumentTypeError('Choose a whole number of threads from 1 to 64.')
    return int(value)


parser = argparse.ArgumentParser(description='Resume full Lean replay and final axiom audit.')
parser.add_argument('--bootstrap', action='store_true', help='Install the pinned toolchain and fetch pinned dependency caches; install elan on Linux if absent.')
parser.add_argument('--jobs', type=threads, default=1, help='Lean worker threads per module; modules compile serially (default: 1).')
parser.add_argument('--fresh', action='store_true', help='Ignore accepted receipts and replay all modules.')
parser.add_argument('--plan', action='store_true', help='Check sources and print the dependency plan without installing or running Lean.')
parser.add_argument('--ci', action='store_true', help='Require a clean Git checkout and append a privacy-filtered Actions summary.')
args = parser.parse_args()
root = Path.cwd()
os.umask(0o077)
state = root / '.verification'
state.mkdir(exist_ok=True)
lock = (state / 'runner.lock').open('a')
try:
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except BlockingIOError:
    raise SystemExit('A verification script is already running in this checkout.')
run_id = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + str(os.getpid())
run_dir = state / 'runs' / run_id
run_dir.mkdir(parents=True)
progress = re.compile(r'\[([0-9]+)/([0-9]+)\] (accepted|cached|blocked|failed) [A-Za-z0-9_.]+\n?\Z')
checking = re.compile(r'\[([0-9]+)/([0-9]+)\] checking ([A-Za-z0-9_.]+)\n?\Z')
summary = {'status': 'NOT_VERIFIED', 'lean_worker_threads': args.jobs}


def duration(seconds):
    minutes, seconds = divmod(max(0, int(seconds)), 60)
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'


def run(command, log_name, show_progress=False):
    """Keep raw logs private and terminate/reap the whole child group on cancel."""
    with (run_dir / log_name).open('ab') as log:
        child = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 start_new_session=True)
        started = previous = time.monotonic()
        compile_seconds = 0.0
        compile_count = 0
        had_failure = False
        current_module = None
        compiler_errors = []
        try:
            for line in child.stdout:
                log.write(line)
                log.flush()
                decoded = line.decode('utf-8', errors='replace')
                checking_match = checking.fullmatch(decoded) if show_progress else None
                if checking_match:
                    current_module = checking_match[3]
                    compiler_errors = []
                    print(decoded.rstrip() + ' | elapsed ' + duration(time.monotonic() - started), flush=True)
                elif current_module and len(compiler_errors) < 3:
                    # Only expose errors attributed to the current source file, never
                    # arbitrary process output, tracebacks, or environment details.
                    relative = decoded.removeprefix(str(root) + os.sep).rstrip()
                    source = current_module.replace('.', '/') + '.lean'
                    if re.match(re.escape(source) + r':\d+:\d+: error:', relative):
                        # A path can include spaces, so redact the rest of that line
                        # instead of risking partial disclosure of a home directory.
                        relative = re.sub(r'(?<![\w.])(?:/[A-Za-z_~]|[A-Za-z]:[\\/]).*',
                                          '[local path omitted]', relative)
                        relative = ''.join(char if char.isprintable() else ' ' for char in relative)
                        compiler_errors.append(relative[:600])
                match = progress.fullmatch(decoded) if show_progress else None
                if match:
                    completed, total = int(match[1]), int(match[2])
                    if not 0 < completed <= total:
                        continue
                    if match[3] in {'accepted', 'cached'}:
                        # A later replay/audit failure must not be attributed to
                        # a module whose compilation already succeeded.
                        current_module = None
                        compiler_errors = []
                    now = time.monotonic()
                    if match[3] == 'accepted':
                        compile_count += 1
                        compile_seconds += now - previous
                    had_failure |= match[3] in {'blocked', 'failed'}
                    previous = now
                    if had_failure:
                        eta = 'unavailable (module failure)'
                    elif completed == total:
                        eta = 'module replay finished; final audit pending'
                    elif compile_count < 10:
                        eta = 'collecting samples'
                    else:
                        eta = duration(compile_seconds / compile_count * (total - completed))
                    print(f'{decoded.rstrip()} | {100 * completed / total:.2f}% of modules'
                          f' | elapsed {duration(now - started)} | rough ETA: {eta}', flush=True)
            code = child.wait()
        except BaseException:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass
            # The group leader can exit while a compiler descendant ignores TERM.
            # Stop any survivors before checkpoint packaging can read their files.
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            child.wait()
            raise
        finally:
            child.stdout.close()
    if code:
        for diagnostic in compiler_errors:
            print('  ' + diagnostic, flush=True)
        if current_module:
            print('Module log: .verification/' + current_module + '.log', flush=True)
        raise RuntimeError('A verification stage failed; inspect the local run logs.')


def capture(command):
    return subprocess.check_output(command, stderr=subprocess.DEVNULL).decode().strip()


def bootstrap():
    for tool in ['git', 'curl', 'tar']:
        if not shutil.which(tool):
            raise RuntimeError('Missing prerequisite: ' + tool)
    if not shutil.which('elan'):
        arch = platform.machine()
        digests = {
            'x86_64': '42b94d4244e8353142c456ec0e4ca6528fd898a6c604d4059f494e706e431f63',
            'aarch64': '05febd124d84ebf994b2e7479922a5650b1e950c17ae3bd1ddd776b65bb72bf9',
        }
        if platform.system() != 'Linux' or arch not in digests:
            raise RuntimeError('Install elan separately on this platform, then retry.')
        # Official v4.2.4 release asset digests, checked against GitHub release metadata.
        url = 'https://github.com/leanprover/elan/releases/download/v4.2.4/elan-' + arch + '-unknown-linux-gnu.tar.gz'
        archive = run_dir / 'elan.tar.gz'
        run(['curl', '--proto', '=https', '--tlsv1.2', '--fail', '--location', '--silent',
             '--show-error', '--retry', '3', '--output', str(archive), url], 'bootstrap.log')
        if hashlib.sha256(archive.read_bytes()).hexdigest() != digests[arch]:
            raise RuntimeError('Elan archive checksum mismatch; nothing was installed.')
        # Extract only the expected regular executable, never arbitrary archive paths.
        with tarfile.open(archive, 'r:gz') as bundle:
            member = bundle.getmember('elan-init')
            if not member.isfile():
                raise RuntimeError('Unexpected elan installer archive.')
            installer = run_dir / 'elan-init'
            installer.write_bytes(bundle.extractfile(member).read())
        installer.chmod(0o700)
        run([str(installer), '-y', '--no-modify-path', '--default-toolchain', 'none'], 'bootstrap.log')
        installer.unlink()
        archive.unlink()
    run(['elan', 'toolchain', 'install', (root / 'lean-toolchain').read_text().strip()], 'bootstrap.log')
    # Do not call verify.py --setup: it restores superseded generated sources.
    run(['lake', 'exe', 'cache', 'get'], 'bootstrap.log')


def check_dependencies():
    manifest = json.loads((root / 'lake-manifest.json').read_text())
    for package in manifest['packages']:
        package_dir = root / manifest['packagesDir'] / package['name']
        if (package['type'] != 'git' or not (package_dir / '.git').exists()
                or capture(['git', '-C', str(package_dir), 'rev-parse', 'HEAD']) != package['rev']
                or capture(['git', '-C', str(package_dir), 'status', '--porcelain', '--untracked-files=all'])):
            raise RuntimeError('A dependency does not match its pinned clean revision.')


def stop(_signum, _frame):
    raise KeyboardInterrupt


signal.signal(signal.SIGTERM, stop)
exit_code = 1
try:
    if not shutil.which('git'):
        raise RuntimeError('Git is required.')
    commit = capture(['git', 'rev-parse', 'HEAD'])
    if re.fullmatch(r'[0-9a-f]{40,64}', commit):
        summary['commit'] = commit
    dirty = bool(capture(['git', 'status', '--porcelain', '--untracked-files=all']))
    summary['checkout_modified'] = dirty
    if args.ci and dirty:
        raise RuntimeError('The CI checkout has local changes; review them before rerunning.')
    if args.plan:
        run([sys.executable, 'scripts/verify.py', '--all', '--plan'], 'plan.log')
        summary['status'] = 'SOURCE_PLAN_PASSED_NOT_COMPILED'
        print('Source and dependency plan passed; Lean was not run.', flush=True)
    else:
        elan_bin = Path(os.environ.get('ELAN_HOME', str(Path.home() / '.elan'))) / 'bin'
        os.environ['PATH'] = str(elan_bin) + os.pathsep + os.environ.get('PATH', '')
        config_names = ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']
        config_before = {name: (root / name).read_bytes() for name in config_names}
        if args.bootstrap:
            print('Preparing the pinned toolchain and dependency cache.', flush=True)
            bootstrap()
        if not shutil.which('elan') or not shutil.which('lake'):
            raise RuntimeError('Elan/Lake are missing; rerun with --bootstrap on Linux.')
        if any((root / name).read_bytes() != data for name, data in config_before.items()):
            raise RuntimeError('Bootstrap changed the pinned configuration; review before replay.')
        check_dependencies()
        # A previous successful result must never describe this attempt.
        for name in ['result.json', 'incomplete-result.json', 'final-audit.json']:
            previous = state / name
            if previous.exists():
                previous.replace(run_dir / ('previous-' + name))
        command = [sys.executable, 'scripts/verify.py', '--all', '--jobs', str(args.jobs)]
        if args.fresh:
            command.append('--fresh')
        print('Replaying all local modules; matching accepted receipts may be reused.', flush=True)
        run(command, 'replay.log', show_progress=True)
        print('Auditing current source hashes, receipts, and final theorem axioms.', flush=True)
        run([sys.executable, 'scripts/finalize_verification.py'], 'finalize.log')
        result = json.loads((state / 'result.json').read_text())
        audit = json.loads((state / 'final-audit.json').read_text())
        summary.update(validated_success(result, audit))
        if summary['trust_model'] == 'lean_kernel_and_native_compiler':
            print('Full replay and final axiom audit passed with compiled numerical certificates; '
                  'the recorded checks additionally trust the Lean compiler.', flush=True)
        else:
            print('Full replay and final kernel-only axiom audit passed.', flush=True)
    exit_code = 0
except KeyboardInterrupt:
    summary['status'] = 'INTERRUPTED_NOT_VERIFIED'
    print('Verification stopped; completed matching receipts remain reusable.', flush=True)
    exit_code = 130
except (RuntimeError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
    summary['status'] = 'FAILED_NOT_VERIFIED'
    # RuntimeError messages above are fixed text; other exceptions can contain local paths.
    print(str(error) if type(error) is RuntimeError else 'Verification failed; inspect the local run logs.', flush=True)
finally:
    payload = json.dumps(summary, indent=2) + '\n'
    (run_dir / 'summary.json').write_text(payload)
    (state / 'runner-summary.json').write_text(payload)
    if args.ci and os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as out:
            out.write('### Proof verification\n\n```json\n' + payload + '```\n\n')
            out.write('Diagnostics and receipts are in `.verification/`; the CI artifact steps retain selected outputs after replay.\n')
    print('Local status: .verification/runner-summary.json', flush=True)
    print('Private logs: .verification/runs/' + run_id + '/', flush=True)
raise SystemExit(exit_code)
PY
