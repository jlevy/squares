"""两套精确程序重算整个有限对偶。
Recompute the entire finite dual with two exact programs.
"""
from pathlib import Path
import argparse,json,os,subprocess,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'verifier'))
from exact import ROOT,ORIGINAL,load,save,sha,require
from check import generate_input

def main():
 ap=argparse.ArgumentParser(description='精确支撑族障碍 / Exact support-family obstruction')
 ap.add_argument('--output',type=Path,required=True,help='全新外部目录 / Fresh external directory');a=ap.parse_args()
 require(__debug__ and not os.environ.get('PYTHONOPTIMIZE'),'ASSERTIONS')
 out=a.output.resolve();require(out!=ROOT and ROOT not in out.parents,'EXTERNAL_OUTPUT');out.mkdir(parents=True,exist_ok=False)
 for key in ('LD_PRELOAD','LD_LIBRARY_PATH','CXXFLAGS','CFLAGS','PYTHONPATH'):require(not os.environ.get(key),'UNREVIEWED_ENVIRONMENT')
 cert=ROOT/'obstruction/certificate.json';data=load(cert,True)
 require(sha(cert)=='f4edfa9a08efaffe8916d3da2c2a8ff567489a2185319de742e8b9e97e3939f9','DUAL_CERTIFICATE_IDENTITY')
 _,text=generate_input(data);input_file=out/'input.txt';input_file.write_text(text)
 paths=['obstruction/check.cpp','obstruction/check.py','obstruction/run.py','tests/oracle.py','verifier/exact.py']
 hashes={p:sha(ROOT/p) for p in paths};start=time.monotonic();stages=[]
 def run(name,command,expected=0):
  t=time.monotonic()
  with (out/(name+'.stdout')).open('wb') as so,(out/(name+'.stderr')).open('wb') as se:
   r=subprocess.run(command,cwd=ROOT,stdout=so,stderr=se,timeout=1800)
  stages.append({'stage':name,'exit_code':r.returncode,'expected_exit':expected,'seconds':time.monotonic()-t,
                 'stdout_sha256':sha(out/(name+'.stdout')),'stderr_sha256':sha(out/(name+'.stderr'))})
  save(out/'stages.json',stages);require(r.returncode==expected,'DUAL_STAGE:'+name)
 run('python',[sys.executable,'-B','obstruction/check.py','--output',str(out/'python.json')])
 exe=out/'dual';run('build-cpp',['g++','-O3','-std=c++17','obstruction/check.cpp','-o',str(exe)])
 run('cpp',[str(exe),str(input_file)])
 py=load(out/'python.json');cpp=load(out/'cpp.stdout')
 for key in ('max_column','max_score_numerator','max_score_denominator','strict_scaled_slack'):
  require(str(py[key])==str(cpp[key]),'EXACT_DUAL_DISAGREEMENT')
 require(py['sites']==cpp['sites']==2526 and py['poses']==cpp['poses']==388,'ALL_COEFFICIENTS')
 lines=text.splitlines();header=lines[0].split();header[-1]='1'
 false=out/'one-pose.txt';false.write_text(' '.join(header)+'\n'+'\n'.join(lines[1:2527])+'\n'+lines[2527]+'\n')
 run('false-dual',[str(exe),str(false)],2)
 require(load(out/'false-dual.stdout')['status']=='DUAL_REFUSED','NEGATIVE_CONTROL')
 require(hashes=={p:sha(ROOT/p) for p in paths},'SOURCE_CHANGED')
 result={'schema':'n40-support-obstruction/v1','status':'EXACT_DUAL_CODE_DISTINCT_CHECKED',
         'scope':'original-2526-uniform-D4-rectangle-orbits','target':'168/25','sites':2526,'poses':388,
         'coefficients_per_implementation':980088,'source_sha256':ORIGINAL,'certificate_sha256':sha(cert),
         'code_sha256':hashes,'input_sha256':sha(input_file),'binary_sha256':sha(exe),'python':py,'cpp':cpp,
         'actual_exits':{r['stage']:r['exit_code'] for r in stages},'stages':stages,'seconds':time.monotonic()-start,
         'packing_upper_bound':False,'positive_bound_at_target':False}
 save(out/'obstruction.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
