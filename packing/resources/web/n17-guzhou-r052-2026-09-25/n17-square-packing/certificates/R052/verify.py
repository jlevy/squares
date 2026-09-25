#!/usr/bin/env python3
"""R052 exact public replay / R052 精确公开复演。"""
from collections import Counter
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor,as_completed
from fractions import Fraction
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import platform
import subprocess
import sys
import time
import zipfile

ROOT=Path(__file__).resolve().parent
CERT_SHA='d77743eadf7f4bf9c424549a37a4296ea3b23fceee4af8e3d774a5a07e62e825'
CHECKER_SHA='82fad041d66bc7a0f14d9dfe9b9282d8562d50fc4844649d2e684414a7ba24b1'
N=15721
MINIMUM=999426274093
BUDGET=16990246659579
sys.path.insert(0,str(ROOT/'src'))


def need(ok,message):
    if not ok:raise ValueError(message+' / 复验检查失败')


def sha(raw):return hashlib.sha256(raw).hexdigest()


def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path,obj):
    with Path(path).open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(obj,stream,ensure_ascii=False,separators=(',',':'));stream.write('\n')


def check_manifest():
    manifest=read(ROOT/'MANIFEST.json')
    need(manifest['schema']=='n17.r052.public-package.manifest.v1','Wrong manifest schema')
    listed=set()
    for item in manifest['files']:
        name=item['path'];path=Path(name)
        need(not path.is_absolute() and '..' not in path.parts and '\\' not in name and name not in listed and name!='MANIFEST.json','Unsafe or duplicate package path')
        listed.add(name);raw=(ROOT/path).read_bytes()
        need(len(raw)==item['bytes'] and sha(raw)==item['sha256'],'File identity: '+name)
    found={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    need(found==listed,'Package files differ from explicit allowlist')
    return sha((ROOT/'MANIFEST.json').read_bytes())


def block_check(rec,lo,hi,expected):
    need(type(lo) is int and type(hi) is int and 0<=lo<hi<=N,'Noninteger or invalid range')
    need(rec['status']=='PASS_EXACT_MOVABLE_SUPPORT_SCAN' and rec['certificate_sha256']==CERT_SHA and rec['parent_side']=='230650/231001' and rec['measure']=='combined','Block identity/status')
    need(rec['range']==[lo,hi] and all(type(x) is int for x in rec['range']),'Block range')
    need(rec['atoms']==18585 and rec['thresholds']==4504 and rec['budget_units']==BUDGET and not rec['escape_rows'],'Block resources/budget')
    rows=rec['rows']
    need([r['row'] for r in rows]==list(range(lo,hi)) and all(type(r['row']) is int and type(r['minimum_units']) is int and type(r['slabs']) is int and r['slabs']>0 for r in rows),'Block row coverage/types')
    need(rows==expected[lo:hi],'Per-row exact replay differs from accepted ledger')
    need(rec['minimum_units']==min(r['minimum_units'] for r in rows)>=MINIMUM,'Block minimum')
    need(rec['histogram']==dict(Counter(str(r['minimum_units']) for r in rows)) and rec['center_slabs']==sum(r['slabs'] for r in rows),'Block histogram/slabs')


def records():
    identity=check_manifest();pins=read(ROOT/'SOURCE_PIN.json')
    raw=gzip.decompress((ROOT/'certificate/R052_CERTIFICATE.json.gz').read_bytes())
    need(sha(raw)==CERT_SHA==pins['certificate_sha256'],'Candidate identity')
    cert=json.loads(raw)
    need(cert['L']=='4613/1000' and cert['A']=='230650/231001' and Fraction(cert['L'])/Fraction(cert['A'])==Fraction(231001,50000),'Bound identity')
    need(len(cert['entries'])==N and cert['minimum_units']==MINIMUM and cert['budget_units']==BUDGET and 17*MINIMUM-BUDGET==2,'Certificate summary')
    ledger_raw=gzip.decompress((ROOT/'results/BIGINT_ROWS.json.gz').read_bytes())
    need(sha(ledger_raw)==pins['results/BIGINT_ROWS.json.gz']['decompressed_sha256'],'Ledger identity')
    ledger=json.loads(ledger_raw)
    need([r['row'] for r in ledger]==list(range(N)) and min(r['minimum_units'] for r in ledger)==MINIMUM,'Complete ledger')
    result_raw=(ROOT/'results/BIGINT_RESULT.json').read_bytes()
    need(sha(result_raw)==pins['results/BIGINT_RESULT.json']['decompressed_sha256'],'Result identity')
    result=json.loads(result_raw)
    need(result['status']=='PASS_COMPLETE_INDEPENDENT_BIGINT' and result['candidate_sha256']==CERT_SHA and result['checker_sha256']==CHECKER_SHA,'Accepted scan identity')
    need(result['checked_rows']==result['angular_rows']==N and result['minimum_units']==MINIMUM and result['budget_units']==BUDGET and result['surplus_units']==2 and not result['escape_rows'],'Accepted scan totals')
    with zipfile.ZipFile(ROOT/'results/BIGINT_BLOCKS.zip') as archive:
        names=archive.namelist()
        need(len(names)==len(set(names))==123 and set(names)==set(result['chunks']),'Block archive membership')
        cursor=0
        for name in sorted(names):
            data=archive.read(name);need(sha(data)==result['chunks'][name],'Block hash: '+name)
            rec=json.loads(data);lo,hi=rec['range']
            need(lo==cursor and name==f'rows_{lo:05d}_{hi:05d}.json','Block order/name')
            block_check(rec,lo,hi,ledger);cursor=hi
        need(cursor==N,'Incomplete archived coverage')
    return identity,raw,cert,ledger


def containment(cert):
    from structure import check
    result=check(cert)
    need(result['angular_rows']==N and result['strict_containment_inequalities']==4*N and result['budget_units']==BUDGET and result['physical_sites']==18585,'Structure totals')
    need(result['minimum_containment_margin']=='4613/9240040000000000000','Containment margin')
    for a,b,t,core in cert['entries']:
        t=Fraction(t)
        need(1-t*t>=2*t>=0,'Core direction outside first octant')
    need(result['point_orbits']==2354 and result['threshold_orbits']==514 and result['generic_orbits']==54 and result['physical_trigger_groups']==4504,'Resource counts')
    return result


def main():
    need(__debug__,'Python -O is not a verification mode')
    ap=argparse.ArgumentParser(description=__doc__)
    modes=ap.add_mutually_exclusive_group()
    modes.add_argument('--containment',action='store_true')
    modes.add_argument('--python-full',action='store_true')
    modes.add_argument('--bigint-full',action='store_true')
    ap.add_argument('--jobs',type=int,default=4)
    ap.add_argument('--source',type=Path,help='Pinned offline R038 source / 锁定的离线 R038 原源')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    need(1<=args.jobs<=12,'Jobs outside 1..12')
    out=args.output.resolve()
    need(not out.exists() and out!=ROOT and ROOT not in out.parents,'Output must be new and outside package')
    started=time.monotonic();manifest,raw,cert,expected=records()
    structure=containment(cert) if args.containment or args.python_full or args.bigint_full else None
    out.mkdir(parents=True)
    mode='records';rows=None
    inp={'manifest_sha256':manifest,'certificate_sha256':CERT_SHA,'verifier_sha256':sha(Path(__file__).read_bytes()),'python':sys.version,'platform':platform.platform(),'jobs':args.jobs}
    if args.python_full or args.bigint_full:
        candidate=out/'CANDIDATE.json';candidate.write_bytes(raw)
        if args.python_full:
            import numpy,numba,llvmlite
            import python_replay
            inp.update(numpy=numpy.__version__,numba=numba.__version__,llvmlite=llvmlite.__version__)
            mode='python-full';rows=[]
            with ProcessPoolExecutor(max_workers=args.jobs,initializer=python_replay.initialize,initargs=(str(candidate),)) as pool:
                for row in pool.map(python_replay.row_minimum,range(N),chunksize=16):
                    need(row['minimum_units']==expected[row['row']]['minimum_units'],'Fresh Python minimum mismatch')
                    rows.append(row)
                    if len(rows)%256==0:print(json.dumps({'mode':mode,'completed_rows':len(rows),'total_rows':N}),flush=True)
        else:
            from prepare_secondary import reconstruct
            mode='bigint-full';script=reconstruct(out/'secondary.js',args.source)
            inp['node']=subprocess.check_output(['node','--version'],text=True).strip()
            need(int(inp['node'].lstrip('v').split('.')[0])>=24,'Node 24 or newer required')
            inp['checker_sha256']=CHECKER_SHA
            ranges=[(lo,min(N,lo+128)) for lo in range(0,N,128)]
            def run(pair):
                lo,hi=pair
                need(sha(script.read_bytes())==CHECKER_SHA and sha(candidate.read_bytes())==CERT_SHA,'Fresh input/code changed')
                proc=subprocess.run(['node',str(script),'--certificate',str(candidate),'--expected-sha',CERT_SHA,'--A',cert['A'],'--measure','combined','--start',str(lo),'--stop',str(hi)],capture_output=True,text=True)
                need(proc.returncode==0,'Node replay failed: '+proc.stderr)
                rec=json.loads(proc.stdout);block_check(rec,lo,hi,expected)
                return lo,hi,rec
            completed={}
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                for future in as_completed([pool.submit(run,pair) for pair in ranges]):
                    lo,hi,rec=future.result();completed[lo]=rec
                    write(out/f'rows_{lo:05d}_{hi:05d}.json',rec)
                    if len(completed)%8==0:print(json.dumps({'mode':mode,'completed_chunks':len(completed),'total_chunks':len(ranges)}),flush=True)
            rows=[r for lo in sorted(completed) for r in completed[lo]['rows']]
            need(sha(script.read_bytes())==CHECKER_SHA,'Checker changed during run')
        need(sha(candidate.read_bytes())==CERT_SHA and [r['row'] for r in rows]==list(range(N)),'Fresh complete coverage')
        need(min(r['minimum_units'] for r in rows)==MINIMUM,'Fresh global minimum')
        write(out/'ROWS.json',rows)
    elif args.containment:mode='containment'
    need(check_manifest()==manifest,'Package changed during verification')
    inp['mode']=mode;write(out/'INPUT.json',inp)
    result={'status':'PASS_R052_'+mode.upper().replace('-','_'),'mode':mode,'bound':'231001/50000','candidate_sha256':CERT_SHA,'manifest_sha256':manifest,'checked_rows':N if rows is not None else 0,'archived_rows':N,'minimum_units':MINIMUM,'budget_units':BUDGET,'strict_surplus_units':2,'structure':structure,'seconds':time.monotonic()-started,'scope':'Fresh full centre replay only in full modes / 仅 full 模式重新计算完整中心空间'}
    write(out/'RESULT.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)


if __name__=='__main__':main()
