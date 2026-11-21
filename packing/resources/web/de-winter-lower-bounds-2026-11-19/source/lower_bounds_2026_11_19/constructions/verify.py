"""Rebuild each central-strip construction directly from its earlier rational measure."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import gzip,json,itertools,hashlib
HERE=Path(__file__).resolve().parent

def read(file):
    with gzip.open(file,'rt') as stream:
        return json.load(stream)

def rows(measure):
    result=defaultdict(F)
    for row in measure['rectangles']:
        result[tuple(map(F,row['rectangle']))]+=F(row['mass'])
    return dict(result)

def rebuild(source,j):
    L=F(source['L'])
    assert j>=1 and L>1
    middle=(L-1)/2
    bands=[(F(0),middle,0),*((middle,middle+1,offset) for offset in range(j+1)),(middle+1,L,j)]
    def split(a,b):
        for low,high,offset in bands:
            l,h=max(a,low),min(b,high)
            if l<h:
                yield l+offset,h+offset
    placed=defaultdict(F)
    for (x,y,X,Y),mass in rows(source).items():
        density=mass/((X-x)*(Y-y))
        for (l,h),(u,v) in itertools.product(split(x,X),split(y,Y)):
            placed[l,u,h,v]+=density*(h-l)*(v-u)
    return placed

def check(case):
    src=HERE/case['input_file']
    assert hashlib.sha256(src.read_bytes()).hexdigest()==case['input_sha256']
    source=read(src)
    target=read(HERE.parent/'sources'/case['output_file'])
    placed=rebuild(source,case['added_strips'])
    total=sum(placed.values())
    assert total==F(case['raw_mass'])
    assert F(target['L'])==F(source['L'])+case['added_strips']
    scale=F(target['total_mass'])/total
    assert {square:mass*scale for square,mass in placed.items()}==rows(target)
    return len(placed)

if __name__=='__main__':
    if not __debug__:raise SystemExit('Run with assertions enabled.')
    for rec in json.loads((HERE/'cases.json').read_text()):
        count=check(rec)
        print(f"Reconstructed all {count:,} rational rectangle weights for n={rec['n']}.")
