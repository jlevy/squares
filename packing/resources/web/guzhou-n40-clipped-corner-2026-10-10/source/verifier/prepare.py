import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import tarfile
import tomllib
import urllib.request

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(description='准备固定依赖 / Prepare pinned dependencies')
    ap.add_argument('--runtime',type=Path,required=True,help='运行目录 / Runtime directory')
    args=ap.parse_args()
    vendor=args.runtime/'vendor'
    vendor.mkdir(parents=True,exist_ok=False)
    packages=tomllib.loads((ROOT/'verifier/sqverify_fast/Cargo.lock').read_text())['package']
    result=[]
    for package in packages:
        if 'source' not in package:
            continue
        name=package['name']+'-'+package['version']
        url='https://static.crates.io/crates/'+package['name']+'/'+name+'.crate'
        request=urllib.request.Request(url,headers={'User-Agent':'n40-square-packing-reproduction'})
        raw=urllib.request.urlopen(request,timeout=180).read()
        digest=hashlib.sha256(raw).hexdigest()
        if digest!=package['checksum']:
            raise RuntimeError('DEPENDENCY_HASH_MISMATCH:'+name)
        files={}
        with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as archive:
            for item in archive.getmembers():
                parts=PurePosixPath(item.name).parts
                if not parts or parts[0]!=name or '..' in parts or PurePosixPath(item.name).is_absolute():
                    raise RuntimeError('UNSAFE_ARCHIVE_PATH')
                target=vendor.joinpath(*parts)
                if item.isdir():
                    target.mkdir(parents=True,exist_ok=True)
                elif item.isfile():
                    content=archive.extractfile(item).read()
                    target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(content)
                    files['/'.join(parts[1:])]=hashlib.sha256(content).hexdigest()
                else:
                    raise RuntimeError('UNSUPPORTED_ARCHIVE_ENTRY')
        (vendor/name/'.cargo-checksum.json').write_text(json.dumps({'files':files,'package':digest}),encoding='utf-8')
        result.append({'name':name,'sha256':digest,'url':url,'files':len(files)})
        print(name,flush=True)
    (args.runtime/'dependencies.json').write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__=='__main__':
    main()
