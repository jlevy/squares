from pathlib import Path
import sys,subprocess,csv,json,argparse
p=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(add_help=False);parser.add_argument('--n',type=int);o,_=parser.parse_known_args()
recent={int(r['n'])for r in csv.DictReader(open(p/'followup/lower_bounds.csv'))}|{r['n']for r in json.load(open(p/'followup/inherited.json'))}|{int(f.name[1:])for f in (p/'followup/upper').glob('n*')}|{int(r['n'])for r in json.load(open(p/'followup/repeated/claims.json'))}|{int(r['n'])for r in json.load(open(p/'followup/envelopes/claims.json'))}
if (p/'followup/corner_trim/claims.json').is_file():recent.update(r['n'] for r in json.load(open(p/'followup/corner_trim/claims.json')))
programs=[p/'verify_previous.py',p/'followup/verify.py']if o.n is None else [p/'followup/verify.py' if o.n in recent or o.n in {r['n'] for r in json.load(open(p/'followup/mass_reserve/claims.json'))} else p/'verify_previous.py']
for f in programs:subprocess.run([sys.executable,f,*sys.argv[1:]],check=True)
