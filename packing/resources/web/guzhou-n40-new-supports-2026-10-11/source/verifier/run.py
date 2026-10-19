"""完整连续姿态验证，所有输出隔离于源码。
Complete continuous-pose verification with outputs isolated from source.
"""
import argparse,concurrent.futures,datetime,json,os,platform,resource,subprocess,sys,time
from pathlib import Path
from exact import *

def main():
 ap=argparse.ArgumentParser(description='完整复跑 / Complete replay')
 ap.add_argument('--output',type=Path,required=True,help='新外部目录 / Fresh external directory')
 ap.add_argument('--workers',type=int,default=4,help='并行进程数 / Worker processes')
 a=ap.parse_args();require(__debug__ and not os.environ.get('PYTHONOPTIMIZE'),'PYTHON_OPTIMIZATION')
 require(platform.system()=='Linux' and platform.machine()=='x86_64','PLATFORM');require(1<=a.workers<=8,'WORKERS')
 for k in ('CFLAGS','CXXFLAGS','LDFLAGS','LD_PRELOAD','LD_LIBRARY_PATH','PYTHONPATH'):require(not os.environ.get(k),'ENVIRONMENT:'+k)
 out=a.output.resolve();require(out!=ROOT and ROOT not in out.parents,'EXTERNAL_OUTPUT');out.mkdir(parents=True,exist_ok=False)
 resource.setrlimit(resource.RLIMIT_CORE,(0,0));env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
 start=time.monotonic();started=datetime.datetime.now(datetime.timezone.utc).isoformat();state={'status':'RUNNING','stages':[]}
 def execute(name,cmd,cwd=ROOT,expected=(0,),timeout=1800):
  st=time.monotonic()
  with (out/(name+'.stdout')).open('wb') as o,(out/(name+'.stderr')).open('wb') as e:p=subprocess.run(cmd,cwd=cwd,env=env,stdout=o,stderr=e,timeout=timeout)
  state['stages'].append({'stage':name,'exit_code':p.returncode,'seconds':time.monotonic()-st,'stdout_sha256':sha(out/(name+'.stdout')),'stderr_sha256':sha(out/(name+'.stderr'))})
  save(out/'execution.json',state);require(p.returncode in expected,'FAILED_STAGE:'+name)
 try:
  from audit import content,fingerprints
  content(ROOT);source=fingerprints(ROOT);sc=scalar();pose,axis,admission=make_inputs(ROOT/'certificate/certified_candidate.json')
  for folder in ('build','pose','slabs','controls'):(out/folder).mkdir()
  (out/'pose/certificate_input.txt').write_bytes(pose);(out/'axis-input.txt').write_bytes(axis)
  exe=out/'build/continuous';axe=out/'build/axis';rounding=out/'build/rounding'
  print('build-and-controls',flush=True)
  execute('build-pose',['g++',*FLAGS,'verifier/continuous_pose.cpp','-o',str(exe)])
  execute('build-axis',['g++',*FLAGS,'verifier/axis_integer_grid.cpp','-o',str(axe)])
  binaries={'pose':sha(exe),'axis':sha(axe)}
  execute('unit-tests',[sys.executable,'-B','-m','unittest','discover','-s','tests','-p','test_admission.py','-v'])
  execute('exact-oracle',[sys.executable,'-B','tests/test_kernel.py','--output',str(out/'oracle')])
  execute('build-rounding',['g++',*FLAGS,'-I','verifier','tests/rounding_harness.cpp','-o',str(rounding)])
  execute('ieee-neighbors',[str(rounding)])
  execute('wrong-rounding',[str(rounding),'rounding'],out/'pose',expected=(-6,))
  execute('ftz',[str(rounding),'ftz'],out/'pose',expected=(-6,))
  execute('reject-ndebug',['g++','-std=c++17','-DNDEBUG','-c','verifier/continuous_pose.cpp','-o',str(out/'build/rejected.o')],expected=(1,))
  execute('reject-fastmath',['g++','-std=c++17','-ffast-math','-c','verifier/continuous_pose.cpp','-o',str(out/'build/rejected.o')],expected=(1,))
  for label,rho,expected in [('positive',Q(2),0),('negative',Q(1,2),3)]:
   d=out/'controls'/label;d.mkdir();text='\n'.join([enclose(L),enclose(B),'1',' '.join(enclose(v) for v in (0,0,L,L,rho))])+'\n';(d/'certificate_input.txt').write_text(text)
   execute('synthetic-'+label,[str(exe),'1','415000','1000000','4999','5000','10000'],d,expected=(expected,),timeout=60)
  execute('limited-budget',[str(exe),'100000','110000','1000000','4999','5000','1'],out/'pose',expected=(3,))
  require(load(out/'synthetic-negative.stdout')['status']==load(out/'limited-budget.stdout')['status']=='unresolved','UNRESOLVED_CONTROL')
  print('axis',flush=True);execute('axis',[str(axe),str(out/'axis-input.txt')])
  axis_rec={'exit_code':0,'input_sha256':AXIS_INPUT,'source_sha256':AXIS,'binary_sha256':binaries['axis'],'stdout':(out/'axis.stdout').read_text(),'stderr_sha256':sha(out/'axis.stderr')}
  axis_check=admit_axis(axis_rec,binaries['axis']);print('continuous-slabs',flush=True)
  def slab(item):
   i,(lo,hi)=item;prefix=out/'slabs'/f'slab-{i:03d}';args=[str(lo),str(hi),'1000000','4999','5000','30000000'];st=time.monotonic();ret=None
   with prefix.with_suffix('.stdout').open('wb') as o,prefix.with_suffix('.stderr').open('wb') as e:
    try:ret=subprocess.run([str(exe),*args],cwd=out/'pose',env=env,stdout=o,stderr=e,timeout=1800).returncode
    except subprocess.TimeoutExpired:pass
   r={'index':i,'arguments':args,'exit_code':ret,'timed_out':ret is None,'seconds':time.monotonic()-st,'input_sha256':POSE,'source_sha256':KERNEL,'binary_sha256':binaries['pose'],'stdout':prefix.with_suffix('.stdout').read_text(),'stderr_sha256':sha(prefix.with_suffix('.stderr'))}
   save(prefix.with_suffix('.json'),r);print(f'slab {i+1}/43 exit={ret}',flush=True);return r
  slabs=list(zip(P['endpoints'],P['endpoints'][1:]))
  with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:rows=list(pool.map(slab,enumerate(slabs)))
  coverage=admit_slabs(rows,binaries['pose']);require(source==fingerprints(ROOT),'SOURCE_CHANGED')
  require(binaries=={'pose':sha(exe),'axis':sha(axe)} and sha(out/'pose/certificate_input.txt')==POSE and sha(out/'axis-input.txt')==AXIS_INPUT,'RUNTIME_CHANGED')
  (out/'slabs.jsonl').write_text(''.join(json.dumps(z,sort_keys=True,separators=(',',':'))+'\n' for z in rows));save(out/'axis.json',axis_rec)
  r={'schema':'n40-continuous-replay/v1','status':'REPLAYED_SAME_KERNEL','author_claim_status':'CERTIFIED','claim':sc['claim'],
     'parameters':P,'scalar':sc,'coverage':coverage,'axis':axis_check,'admission':admission,'binaries':binaries,'source_sha256':source,
     'slabs_sha256':sha(out/'slabs.jsonl'),'axis_sha256':sha(out/'axis.json'),'oracle':load(out/'oracle/oracle.json'),'ieee':load(out/'ieee-neighbors.stdout'),
     'stages':state['stages'],'compile_flags':FLAGS,'workers':a.workers,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
     'python':sys.version.split()[0],'platform':'x86_64 Linux','started_utc':started,'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'seconds':time.monotonic()-start,'source_commit':os.environ.get('GITHUB_SHA'),'external_review_of_new_kernel':False,'code_distinct_full':False,'method_distinct_full':False,'formal_proof':False}
  save(out/'verification.json',r)
  print('exact-support-family',flush=True)
  with (out/'obstruction.stdout').open('wb') as so,(out/'obstruction.stderr').open('wb') as se:
   dual=subprocess.run([sys.executable,'-B','obstruction/run.py','--output',str(out/'dual')],cwd=ROOT,env=env,stdout=so,stderr=se,timeout=1800)
  require(dual.returncode==0,'DUAL_REPLAY')
  import shutil
  shutil.copyfile(out/'dual/obstruction.json',out/'obstruction.json')
  require(source==fingerprints(ROOT),'SOURCE_CHANGED_AFTER_DUAL')
  r['full_entry_seconds']=time.monotonic()-start;r['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save(out/'verification.json',r)
  state.update(status='COMPLETE',claim=sc['claim'],coverage=coverage,seconds=time.monotonic()-start);save(out/'execution.json',state)
  print(json.dumps({'status':r['status'],'claim':r['claim'],**coverage,'counting_margin':'1/500'}),flush=True)
 except BaseException as e:
  state.update(status='INCOMPLETE',error=type(e).__name__+': '+str(e));save(out/'execution.json',state);raise
if __name__=='__main__':main()
