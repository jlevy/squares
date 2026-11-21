"""Recompile and replay accepted interval checks. Optional controls shrink every rectangle weight."""
from pathlib import Path
import argparse,subprocess,tempfile,concurrent.futures
import check
def replay(folder,workers,sample,controls):
    m=check.verify(folder)
    with tempfile.TemporaryDirectory()as tmp:
        p=Path(tmp);bin=p/'bmcheck';subprocess.run(['c++','-O3','-std=c++17',check.here/({'square':'bmcheck.cpp','octagon':'octagon.cpp','octagon-gram':'gram.cpp'}[m.get('kernel','square')]),'-o',bin],check=True)
        todo=[]
        for lev in m['levels']:
            a,rows=check.read_level(folder,lev);rect=p/('rect'+str(lev['K']));rr=list(check.bm.rows(a));rect.write_bytes(check.input_bytes(rr))
            selected=rows if not sample else [max(rows,key=lambda r:r['nodes'])]
            for r in selected:todo.append((rect,r,lev['K'],False))
            if controls:
                neg=p/('shrunken'+str(lev['K']));neg.write_bytes(check.input_bytes([(*j[:-2],j[-2]//4,j[-1]//4)for j in rr]));todo.append((neg,selected[0],lev['K'],True))
        def execute(job):
            file,r,k,neg=job;h=p/f"h_{k}_{r['r']}_{neg}";h.write_text(' '.join(map(str,r['header']))+'\n')
            q=subprocess.run([bin,file,h,'2100000'],capture_output=True,text=True);v=q.stdout.split()
            if neg:check.require(v and v[0]=='UNDECIDED','negative control passed')
            else:
                check.require(q.returncode==0 and v[0]=='PASS' and int(v[5])>=check.bm.M,'positive replay failed')
            return 1
        with concurrent.futures.ThreadPoolExecutor(workers)as ex:counts=sum(ex.map(execute,todo))
        print(folder.name,'replayed',counts,'checks',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--workers',type=int,default=2);p.add_argument('--sample',action='store_true');p.add_argument('--controls',action='store_true');a=p.parse_args();replay(Path(a.folder).resolve(),a.workers,a.sample,a.controls)
