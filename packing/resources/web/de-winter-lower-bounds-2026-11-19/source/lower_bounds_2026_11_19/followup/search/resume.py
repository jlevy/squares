"""Resume a partial geometric certificate in a separate work directory."""
import argparse,gzip,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('tag',nargs='?');ap.add_argument('--workers',type=int,default=4);ap.add_argument('--output',type=Path,default=Path('squaremath_search_work'));a=ap.parse_args()
rows=json.loads((p/'candidates.json').read_text())
if a.tag is None:
 for r in rows:print(r['tag'],r['verified_bins'],'passing angle intervals retained')
 sys.exit()
r=next((r for r in rows if r['tag']==a.tag),None)
if r is None:raise SystemExit('The requested candidate is absent.')
out=a.output.resolve();out.mkdir(exist_ok=True,parents=True);os.environ['SQUAREMATH_SEARCH_OUTPUT']=str(out)
from search import search,proof
binary=out/'gram'
if not binary.is_file():subprocess.run(['c++','-O3','-std=c++17',proof/'gram.cpp','-o',binary],check=True)
if r['source']<0:
 sub=Path('mix')/str(-r['source']);(out/sub).mkdir(exist_ok=True,parents=True)
 for name in ('measure.json.gz','recipe.json'):shutil.copy(p/sub/name,out/sub/name)
 src=out/sub/'measure.json.gz'
else:
 folder=proof/f"n{r['source']}";meta=json.loads((folder/'manifest.json').read_text());src=folder/meta['levels'][0]['measure']
assert hashlib.sha256(src.read_bytes()).hexdigest()==r['measure_sha256']
place=out/a.tag;place.mkdir(exist_ok=True);log=place/'checked.jsonl'
if not log.exists():log.write_bytes(gzip.decompress((p/'candidates'/(a.tag+'.jsonl.gz')).read_bytes()))
search(r['n'],r['source'],r['side_text'],r['K'],r['mode'],a.workers)
