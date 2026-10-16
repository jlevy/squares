#!/usr/bin/env python3
"""Independent orchestration of the continuous-pose and integer-axis kernels."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction as Q
import json
import math
from pathlib import Path
import re
import subprocess
import time
from generator import ROOT, DEFAULT_ENDPOINTS, generate, local, require, save, sha

FLAGS = ['-O2', '-std=c++17', '-fno-fast-math', '-ffp-contract=off']

def build():
    folder = ROOT/'build'
    folder.mkdir(exist_ok=True)
    sources = {p.name:sha(p) for p in sorted((ROOT/'kernel').iterdir()) if p.suffix in ('.cpp','.h')}
    version = subprocess.check_output(['c++','--version'],text=True).splitlines()[0]
    info = dict(compiler=version,flags=FLAGS,sources=sources)
    cache = folder/'build.json'
    old = json.loads(cache.read_text()) if cache.exists() else {}
    for name in ('continuous_pose','axis_integer_grid'):
        binary = folder/name
        if old.get('configuration') != info or not binary.exists() or old.get('binaries',{}).get(name) != sha(binary):
            subprocess.run(['c++',*FLAGS,'kernel/'+name+'.cpp','-o','build/'+name],cwd=ROOT,check=True,capture_output=True,text=True)
    result = {'configuration':info,'binaries':{n:sha(folder/n) for n in ('continuous_pose','axis_integer_grid')}}
    save(cache,result)
    return result

def execute(name, arguments, out, deadline, input_hash):
    start = time.monotonic()
    row = dict(arguments=arguments,input_sha256=input_hash,timed_out=False)
    remaining = deadline-start
    if remaining <= 0:
        return dict(row,exit_code=None,timed_out=True,seconds=0,stdout='',stderr='Run deadline reached')
    try:
        p = subprocess.run([str(ROOT/'build'/name),*arguments],cwd=out,capture_output=True,text=True,timeout=remaining)
        row.update(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
        try:
            row['kernel'] = json.loads(p.stdout)
        except (ValueError,TypeError):
            pass
    except subprocess.TimeoutExpired:
        row.update(exit_code=None,timed_out=True,stdout='',stderr='Run deadline reached')
    row['seconds'] = time.monotonic()-start
    return row

def identity_ok(row):
    z = row.get('kernel',{})
    return (not row['timed_out'] and z.get('arguments') == row['arguments']
            and z.get('input_sha256') == row['input_sha256'])

def admit_slab(row,tau):
    z = row.get('kernel',{})
    require(identity_ok(row) and row['exit_code'] == 0, 'Slab execution or identity mismatch')
    require(z.get('status') == 'verified', 'Slab unresolved')
    require([z.get(k) for k in ('pl','ph','den')] == list(map(int,row['arguments'][:3])), 'Slab domain mismatch')
    require(type(z.get('nodes')) is int and type(z.get('leaves')) is int and z['leaves']>0 and z['nodes']==2*z['leaves']-1, 'Slab binary cover mismatch')
    v=z.get('lower_bound')
    require(type(v) in (float,int) and math.isfinite(v) and Q(v)>=tau, 'Slab capture bound failed')
    require(type(z.get('max_depth')) is int and 0<=z['max_depth']<=123, 'Slab depth mismatch')
    require(type(z.get('angle_splits')) is int and 0<=z['angle_splits']<z['nodes'], 'Slab split count mismatch')
    row['minimum_capture_lower']=str(Q(v))

def admit_axis(row,tau,manifest):
    z=row.get('kernel',{})
    require(identity_ok(row) and row['exit_code']==0 and z.get('status')=='AXIS_COVERAGE_PROVED', 'Axis coverage refused')
    require(z.get('direct_sum_matches') is True and int(z['scale'])==int(manifest['axis_scale']), 'Axis reconciliation or scale mismatch')
    require(0<int(z['evaluation_abs_bound'])<2**125 and z['evaluation_abs_bound']==manifest['axis_evaluation_bound'], 'Axis overflow bound mismatch')
    require(type(z['x_nodes']) is int and type(z['y_nodes']) is int and 0<z['x_nodes']*z['y_nodes']<=90000000, 'Axis grid mismatch')
    v=Q(int(z['minimum_numerator']),int(z['scale']))
    require(v>=tau,'Axis capture below threshold')
    row['minimum_capture_lower']=str(v)

def parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',required=True);p.add_argument('--params')
    p.add_argument('--n',type=int,required=True);p.add_argument('--core',type=Q,required=True)
    p.add_argument('--tau',type=Q,required=True);p.add_argument('--workers',type=int,default=2)
    p.add_argument('--node-budget',type=int,default=30000000)
    p.add_argument('--endpoints',nargs='+',help='Integer numerators over 1000000, space or comma separated')
    p.add_argument('--label');p.add_argument('--resume',type=Path,help='Previous receipt.json: reuse its accepted slabs when inputs, build, premises and endpoints match');p.add_argument('--timeout',type=float,default=2400,help='Overall wall-clock cap in seconds (at most 172800)')
    return p

def main(argv=None):
    a=parser().parse_args(argv)
    label=a.label or Path(a.candidate).stem
    require(re.fullmatch(r'[A-Za-z0-9_.-]+',label) and label not in ('.','..'), 'Invalid label')
    out=local(ROOT/'runs'/label)
    out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    receipt={'status':'REFUSED','label':label,'slabs':[],'refused_slabs':[],'errors':[]}
    try:
        require(1<=a.workers<=64,'Use 1 to 64 workers')   # 91 10/11: the 2-worker cap was for the build machine; GCP runs use more
        require(0<a.timeout<=172800 and 0<a.node_budget<2**63,'Invalid timeout or node budget')
        deadline=start+a.timeout
        endpoints=DEFAULT_ENDPOINTS if not a.endpoints else [int(v) for token in a.endpoints for v in token.split(',')]
        require(len(endpoints)>=2 and all(x<y for x,y in zip(endpoints,endpoints[1:])), 'Endpoints must strictly increase')
        eps,last=Q(endpoints[0],10**6),Q(endpoints[-1],10**6)
        require(0<eps<last<Q(1,2) and last**2+2*last-1>=0,'Incomplete angle coverage')
        cert,manifest=generate(a.candidate,out,a.core,a.tau,eps,a.params)
        receipt.update(input_sha256=manifest['candidate_sha256'],manifest_sha256=sha(out/'manifest.json'),manifest=manifest)
        require(cert['n']==a.n,'Candidate n mismatch')
        L,M=cert['L'],cert['mass']
        receipt.update(claim=f's({a.n}) > {L/a.core}',claim_fraction=str(L/a.core),
                       premises={'n':str(a.n),'L':str(L),'B':str(a.core),'tau':str(a.tau),'M':str(M),
                                 'counting_margin':str(a.n*a.tau-M),'geometry_margin':str(L**2-2*a.core**2),
                                 'epsilon':str(eps),'last_t':str(last),'angle_coverage_polynomial':str(last**2+2*last-1),
                                 'axis_side':manifest['axis_side'],'axis_containment_margin':manifest['axis_containment_margin']},
                       endpoints=endpoints,denominator=10**6)
        require(a.n*a.tau>M,'Counting inequality failed')
        require(L**2>2*a.core**2,'Geometry inequality failed')
        receipt['build']=build()
        axis=execute('axis_integer_grid',['axis_input.txt'],out,deadline,manifest['files']['axis_input.txt'])
        receipt['axis']=axis
        # Axis failure suffices to refuse; do not spend a full slab run on a failed control.
        admit_axis(axis,a.tau,manifest)
        save(out/'receipt.json',receipt)
        # 91 10/12: resume after a lost machine.  A previous receipt's slab is reused only if the candidate, the generated
        # kernel input, the build (binaries), the premises and the endpoints are identical, the slab's echoed arguments
        # equal the ones this run would pass, and it passes admit_slab again.
        reuse={}
        if a.resume:
            try:prev=json.loads(Path(a.resume).read_text())
            except (OSError,ValueError):prev={}
            same=(prev.get('input_sha256')==receipt['input_sha256'] and prev.get('manifest',{}).get('files')==manifest['files']
                  and prev.get('build')==receipt['build'] and prev.get('premises')==receipt['premises'] and prev.get('endpoints')==endpoints)
            for row in (prev.get('slabs',[]) if same else []):
                i=row.get('index')
                if type(i) is not int or not 0<=i<len(endpoints)-1 or not row.get('accepted'):continue
                args=list(map(str,(endpoints[i],endpoints[i+1],10**6,a.tau.numerator,a.tau.denominator,a.node_budget)))
                r=dict(row)
                if r.get('arguments')!=args or r.get('input_sha256')!=manifest['files']['certificate_input.txt']:continue
                try:admit_slab(r,a.tau)
                except (ValueError,KeyError,TypeError,OverflowError):continue
                r['accepted']=True;r['resumed']=True;reuse[i]=r
            receipt['resumed_from']={'receipt_sha256':sha(Path(a.resume)) if Path(a.resume).exists() else None,'compatible':bool(same),'slabs_reused':len(reuse)}
        def slab(i,lo,hi):
            if i in reuse:return reuse[i]
            args=list(map(str,(lo,hi,10**6,a.tau.numerator,a.tau.denominator,a.node_budget)))
            row=execute('continuous_pose',args,out,deadline,manifest['files']['certificate_input.txt'])
            row['index']=i
            try:
                admit_slab(row,a.tau)
                row['accepted']=True
            except (ValueError,KeyError,TypeError,OverflowError) as e:
                row['accepted']=False;row['reason']=str(e)
                z=row.get('kernel',{})
                row['witness_pose']={k:z[k] for k in ('u','v','w','du','dv','dw','center_lower') if k in z} or None
            return row
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            futures=[pool.submit(slab,i,lo,hi) for i,(lo,hi) in enumerate(zip(endpoints,endpoints[1:]))]
            for f in as_completed(futures):
                row=f.result();receipt['slabs'].append(row)
                receipt['slabs'].sort(key=lambda r:r['index'])
                save(out/'receipt.json',receipt)
                print(json.dumps({'slab':row['index'],'accepted':row['accepted'],'nodes':row.get('kernel',{}).get('nodes')}),flush=True)
        receipt['refused_slabs']=[r for r in receipt['slabs'] if not r['accepted']]
        require(len(receipt['slabs'])==len(endpoints)-1 and not receipt['refused_slabs'],'Not every slab verified')
        require(all(sha(out/name)==value for name,value in manifest['files'].items()),'Generated input changed during run')
        require(sha(a.candidate)==manifest['candidate_sha256'],'Candidate changed during run')
        receipt['status']='VERIFIED'
    except (ValueError,KeyError,TypeError,OSError,OverflowError,subprocess.SubprocessError) as e:
        # Avoid compiler diagnostics containing machine-specific paths in stored receipts.
        receipt['errors'].append(type(e).__name__ if isinstance(e,(OSError,subprocess.SubprocessError)) else str(e))
    receipt['seconds']=time.monotonic()-start
    receipt['summary']={'status':receipt['status'],'claim':receipt.get('claim'),
                        'slabs_completed':len(receipt['slabs']),
                        'nodes':sum(r.get('kernel',{}).get('nodes',0) for r in receipt['slabs']),
                        'leaves':sum(r.get('kernel',{}).get('leaves',0) for r in receipt['slabs']),
                        'seconds':receipt['seconds'],'errors':receipt['errors']}
    save(out/'receipt.json',receipt)
    print(json.dumps(receipt['summary'],sort_keys=True),flush=True)
    return 0 if receipt['status']=='VERIFIED' else 1

if __name__=='__main__':
    raise SystemExit(main())
