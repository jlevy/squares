"""发布目录完整性检查与可复现归档。
Publication integrity checks and reproducible archives.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile
from finite import candidate_bytes, finite_check, PARAMS, read_source, require, sha, validate_nodes
ROOT = Path(__file__).resolve().parents[1]
BASE = {'.gitattributes','.gitignore','.github/workflows/verify.yml','LICENSE','SHA256SUMS',
        'README.md','PROOF.md','REPRODUCIBILITY.md','VERIFICATION.md','SOURCES.md',
        'licenses/jlevy-squares.txt','licenses/wand125.txt',
        'certificate/certified_candidate.json','certificate/parameters.json',
        'verifier/prepare.py','verifier/finite.py','verifier/run.py','verifier/release.py',
        'tests/test_finite.py','results/verification.json'}
RUST = {'Cargo.lock','Cargo.toml','build.rs','rust-toolchain.toml',
        'src/axis.rs','src/certificate.rs','src/exact.rs','src/interval.rs','src/lib.rs',
        'src/main.rs','src/oracle.rs','src/rotated.rs','src/rotated_tests.rs',
        'tests/adversarial.rs','tests/declared_net.rs'}
ALLOWED = BASE | {'verifier/sqverify_fast/'+p for p in RUST} | {'results/nodes.jsonl'}

def files(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts)

def manifest(root):
    return {p.relative_to(root).as_posix():sha(p) for p in files(root) if p.name != 'SHA256SUMS'}

def write_manifest(root):
    (root/'SHA256SUMS').write_text(''.join(d+'  '+p+'\n' for p,d in manifest(root).items()), encoding='utf-8')

def check_pairs(path):
    lines = path.read_text(encoding='utf-8').splitlines()
    i, fenced = 0, False
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            fenced = not fenced; i += 1; continue
        if fenced or not line.strip():
            i += 1; continue
        match = re.match(r'^(#{1,6} )?ZH: (.+)$', line)
        require(match is not None, 'BILINGUAL_LINE:'+path.name+':'+str(i+1))
        require(i+1 < len(lines) and lines[i+1].startswith((match.group(1) or '')+'EN: '), 'BILINGUAL_PAIR')
        i += 2
    require(not fenced, 'UNCLOSED_CODE_FENCE')

def audit(root, verify_hashes=True):
    paths = {p.relative_to(root).as_posix() for p in files(root)}
    require(paths <= ALLOWED and BASE <= paths, 'PUBLIC_FILE_SET')
    require({'verifier/sqverify_fast/'+p for p in RUST} <= paths, 'VENDORED_SOURCE_SET')
    for p in files(root):
        require(not p.is_symlink(), 'SYMLINK')
        text = p.read_text(encoding='utf-8')
        require(not re.search(r'gh[pousr]_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{30,}', text), 'TOKEN_PATTERN')
        require(not re.search(r'/(?:Users|home)/[^/\s]+/|[A-Z]:\\Users\\|/'+r'mnt/data/', text), 'PERSONAL_PATH')
        if p.suffix == '.md':
            check_pairs(p)
            require(not re.search(r'本地线程|用户|本对话|移交|工作区|START_HERE|N40_RETURN|local thread|chat history', text, re.I), 'INTERNAL_PROSE')
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in target and not target.startswith('#'):
                    require((root/target.split('#')[0]).is_file(), 'BROKEN_DOCUMENT_LINK')
    if verify_hashes:
        expected = {}
        for line in (root/'SHA256SUMS').read_text().splitlines():
            digest, path = line.split('  ', 1)
            require(path not in expected and re.fullmatch('[0-9a-f]{64}', digest), 'MANIFEST_FORMAT')
            expected[path] = digest
        require(expected == manifest(root), 'MANIFEST_IDENTITY')
    parameters = json.loads((root/'certificate/parameters.json').read_text())
    _, finite = finite_check(root/'certificate/certified_candidate.json', parameters)
    result = json.loads((root/'results/verification.json').read_text())
    if result['status'] == 'CODE_DISTINCT_FULL':
        require(result['finite'] == finite and result['parameters'] == PARAMS, 'RECEIPT_SCALARS')
        require(result['nodes_sha256'] == sha(root/'results/nodes.jsonl'), 'RECEIPT_NODE_FILE')
        rows = [json.loads(s) for s in (root/'results/nodes.jsonl').read_text().splitlines()]
        derived = hashlib.sha256(candidate_bytes(read_source(root/'certificate/certified_candidate.json'))).hexdigest()
        require(result['derived_candidate_sha256'] == derived, 'DERIVED_IDENTITY')
        validate_nodes(result['node_summary'], rows, derived)
        for path, digest in result['code_and_input_sha256'].items():
            require(path in paths and sha(root/path) == digest, 'EXECUTED_CODE_IDENTITY')
        require(all(c['exit_code'] == 0 for c in result['commands']), 'EXECUTION_EXIT')
    else:
        require(result['status'] == 'PENDING_INDEPENDENT_REPLAY', 'UNRECOGNIZED_VERIFICATION_STATE')
    return {'status':'PUBLICATION_CONTENT_CHECKED','files':len(paths),
            'bytes':sum(p.stat().st_size for p in files(root)),
            'bilingual_documents':5,'verification_status':result['status'],
            'simple_counting_margin':finite['simple_counting_margin']}

def main():
    ap = argparse.ArgumentParser(description='完整性检查或归档 / Integrity check or archive')
    ap.add_argument('--check', action='store_true', help='核查目录 / Check directory')
    ap.add_argument('--package', action='store_true', help='生成公开归档 / Create public archive')
    ap.add_argument('--runtime', type=Path, help='完整运行目录 / Complete-run directory')
    ap.add_argument('--out', type=Path, help='归档输出目录 / Archive output directory')
    a = ap.parse_args()
    require(a.check != a.package, 'SELECT_ONE_OPERATION')
    report = audit(ROOT)
    if a.package:
        require(a.runtime is not None and a.out is not None, 'PACKAGE_ARGUMENTS')
        target = a.out.resolve()/'n40-square-packing'
        require(ROOT != target and ROOT not in target.parents, 'EXTERNAL_OUTPUT_REQUIRED')
        target.mkdir(parents=True, exist_ok=False)
        for source in files(ROOT):
            dest = target/source.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source,dest)
        for name in ('verification.json','nodes.jsonl'):
            shutil.copyfile(a.runtime/'replay'/name, target/'results'/name)
        write_manifest(target)
        report = audit(target)
        require(report['verification_status'] == 'CODE_DISTINCT_FULL', 'FULL_REPLAY_REQUIRED')
        archive = a.out/'n40-670854.zip'
        with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in files(target):
                info = zipfile.ZipInfo('n40-square-packing/'+p.relative_to(target).as_posix(), (2000,1,1,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info,p.read_bytes())
        with zipfile.ZipFile(archive) as z:
            require(z.testzip() is None, 'ZIP_CRC')
        report['archive_sha256'] = sha(archive)
        (a.out/'audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
