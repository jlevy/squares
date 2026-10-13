"""公开目录、哈希和数学收据审计。
Public-tree, hash and mathematical-receipt audit.
"""
from pathlib import Path
import argparse,json,re,shutil,zipfile
from exact import *
DOCS={'README.md','PROOF.md','REPRODUCIBILITY.md','VERIFICATION.md','SOURCES.md'}
STATIC=DOCS|{'LICENSE','licenses/wand125.txt','licenses/tokoharu.txt','licenses/jlevy-squares.txt',
 'certificate/certified_candidate.json','certificate/parameters.json',
 'verifier/exact.py','verifier/run.py','verifier/audit.py','verifier/continuous_pose.cpp','verifier/axis_integer_grid.cpp',
 'tests/oracle.py','tests/test_kernel.py','tests/kernel_harness.cpp','tests/rounding_harness.cpp','tests/test_admission.py',
 '.gitattributes','.gitignore','.github/workflows/verify.yml'}
OUTPUTS={'results/verification.json','results/slabs.jsonl','results/axis.json'}

def files(root):return sorted(p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts)
def fingerprints(root):return {n:sha(root/n) for n in sorted(STATIC)}
def manifest(root):
 (root/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(root).as_posix()+'\n' for p in files(root) if p.name!='SHA256SUMS'))

def bilingual(path):
 lines=path.read_text().splitlines();i=0;fence=False
 while i<len(lines):
  if lines[i].startswith('```'):fence=not fence;i+=1;continue
  if fence or not lines[i].strip():i+=1;continue
  m=re.match(r'^(#{1,6} )?ZH: .+',lines[i]);require(m is not None,'UNPAIRED_LINE:'+path.name+':'+str(i+1))
  require(i+1<len(lines) and lines[i+1].startswith((m.group(1) or '')+'EN: '),'MISSING_ENGLISH')
  i+=2
 require(not fence,'UNFINISHED_CODE_BLOCK')

def content(root):
 present={p.relative_to(root).as_posix() for p in files(root)}
 require(STATIC|{'SHA256SUMS','results/verification.json'}<=present and present<=STATIC|OUTPUTS|{'SHA256SUMS'},'UNEXPECTED_OR_MISSING_FILES')
 expected={}
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);require(re.fullmatch('[0-9a-f]{64}',h) is not None and n not in expected,'HASH_FORMAT');expected[n]=h
 require(expected=={p.relative_to(root).as_posix():sha(p) for p in files(root) if p.name!='SHA256SUMS'},'HASH_MISMATCH')
 for p in files(root):
  require(not p.is_symlink(),'SYMLINK');text=p.read_text(encoding='utf-8')
  require(not re.search(r'gh[pousr]_[A-Za-z0-9]{24,}|github_pat_[A-Za-z0-9_]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY',text),'SECRET_PATTERN')
  require(not re.search(r'/(?:Users|home)/[^/\s]+/|[A-Z]:\\Users\\|/'+r'mnt/data/',text),'PERSONAL_PATH')
  if p.name in DOCS:
   bilingual(p)
   require(not re.search(r'本地线程|本对话|给用户|移交|工作区|START_HERE|N40_RETURN|local thread|chat history',text,re.I),'INTERNAL_EXPLANATION')
   for link in re.findall(r'\]\(([^)]+)\)',text):
    if '://' not in link and not link.startswith('#'):require((root/link.split('#')[0]).is_file(),'BROKEN_LINK:'+link)
 require(load(root/'certificate/parameters.json')==P,'PARAMETERS')
 require(sha(root/'verifier/continuous_pose.cpp')==KERNEL and sha(root/'verifier/axis_integer_grid.cpp')==AXIS,'KERNEL_IDENTITY')
 _,_,inputs=make_inputs(root/'certificate/certified_candidate.json')
 return {'status':'CONTENT_CHECKED','files':len(present),'bytes':sum(p.stat().st_size for p in files(root)),'bilingual_documents':5,'inputs':inputs}

def evidence(root):
 r=load(root/'results/verification.json')
 if r['status']=='PENDING_REPLAY':return {'verification':'PENDING_REPLAY'}
 require(r['schema']=='n40-continuous-replay/v1' and r['status']=='REPLAYED_SAME_KERNEL','VERIFICATION_LEVEL')
 require(r['parameters']==P and r['scalar']==scalar() and r['claim']==scalar()['claim'],'THEOREM')
 require(r['source_sha256']==fingerprints(root),'EXECUTED_SOURCE_IDENTITY')
 require(r['slabs_sha256']==sha(root/'results/slabs.jsonl') and r['axis_sha256']==sha(root/'results/axis.json'),'EVIDENCE_IDENTITY')
 coverage=admit_slabs([loads(s) for s in (root/'results/slabs.jsonl').read_text().splitlines()],r['binaries']['pose'])
 axis=admit_axis(load(root/'results/axis.json'),r['binaries']['axis'])
 require(r['coverage']==coverage and r['axis']==axis and r['compile_flags']==FLAGS,'EVIDENCE_CONTENT')
 expected={'build-pose':0,'build-axis':0,'unit-tests':0,'exact-oracle':0,'build-rounding':0,'ieee-neighbors':0,
 'wrong-rounding':-6,'ftz':-6,'reject-ndebug':1,'reject-fastmath':1,'synthetic-positive':0,'synthetic-negative':3,'limited-budget':3,'axis':0}
 require(len(r['stages'])==len(expected) and {x['stage']:x['exit_code'] for x in r['stages']}==expected,'INCOMPLETE_STAGES')
 o=r['oracle'];require(o['status']=='PASSED_FINITE_ORACLE_TESTS' and o['cases']==160 and o['exact_pose_checks']==4014 and o['exact_area_checks']==3568,'ORACLE_SCOPE')
 require(o['kernel_sha256']==KERNEL and o['driver_sha256']==sha(root/'tests/test_kernel.py') and o['oracle_sha256']==sha(root/'tests/oracle.py'),'ORACLE_IDENTITY')
 require(r['ieee']=={'status':'PASSED','values':1000008,'seed':4010041010},'IEEE_CONTROL')
 for key in ('external_review_of_new_kernel','code_distinct_full','method_distinct_full','formal_proof'):require(r[key] is False,'OVERCLAIMED_STATUS')
 return {'verification':r['status'],'coverage':coverage,'axis':axis,'counting_margin':'1/500'}

def main():
 ap=argparse.ArgumentParser(description='公开核查或归档 / Audit or archive')
 ap.add_argument('--check',action='store_true',help='核查目录 / Check directory')
 ap.add_argument('--package',action='store_true',help='生成已复跑包 / Package replayed source')
 ap.add_argument('--runtime',type=Path,help='完整运行结果 / Complete replay results')
 ap.add_argument('--output',type=Path,help='新归档目录 / Fresh archive directory')
 a=ap.parse_args();require(__debug__ and a.check!=a.package,'OPERATION')
 report=content(ROOT);report.update(evidence(ROOT))
 if a.package:
  require(a.runtime is not None and a.output is not None,'PACKAGE_ARGUMENTS')
  out=a.output.resolve();require(out!=ROOT and ROOT not in out.parents,'EXTERNAL_OUTPUT')
  out.mkdir(parents=True,exist_ok=False);target=out/'n40-square-packing'
  for n in sorted(STATIC):
   dest=target/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dest)
  for n in sorted(OUTPUTS):
   dest=target/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.runtime/Path(n).name,dest)
  manifest(target);report=content(target);report.update(evidence(target));require(report['verification']=='REPLAYED_SAME_KERNEL','INCOMPLETE_REPLAY')
  archive=out/'n40-continuous-1340000-199529.zip'
  with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for p in files(target):
    info=zipfile.ZipInfo('n40-square-packing/'+p.relative_to(target).as_posix(),(2000,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
  with zipfile.ZipFile(archive) as z:require(z.testzip() is None,'CRC')
  (out/(archive.name+'.sha256')).write_text(sha(archive)+'  '+archive.name+'\n')
  report['archive_sha256']=sha(archive);save(out/'audit.json',report)
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
