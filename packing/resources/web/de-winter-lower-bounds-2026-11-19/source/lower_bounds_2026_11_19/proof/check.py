"""Validate the exact inputs, center domains, angular intervals and integer receipts."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
import gzip,hashlib,json,math,sys
import bm
here=Path(__file__).resolve().parent
def require(ok,msg):
    if not ok:raise ValueError(msg)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def input_bytes(rects):
    return (str(len(rects))+'\n'+''.join(' '.join(map(str,r))+'\n' for r in rects)).encode()
def header(a,r,kernel="square"):
    d=F(a['proof_net']['step']);t=r*d;c,s,e=t.denominator**2-t.numerator**2,2*t.numerator*t.denominator,t.denominator**2+t.numerator**2
    original_t=t
    if e>10**13 and kernel in ('octagon','octagon-gram'):
        t=t.limit_denominator(1800000)
        c,s,e=t.denominator**2-t.numerator**2,2*t.numerator*t.denominator,t.denominator**2+t.numerator**2
    require(c>0 and s>=0 and c*c+s*s==e*e and e<=10**13,'invalid direction')
    cut=math.floor(e*bm.G*F(a['B'])/2);left=max(F(0),original_t-d/2);v=(1+2*left-left*left)/(2*(1+left*left));lo=math.floor(bm.G*F(a['L'])/2);hi=math.ceil(bm.G*(F(a['L'])-v))
    if kernel in ("octagon","octagon-gram"):return [c,s,e,bm.G//2,0,lo,lo,hi,hi,math.ceil(10**7*(d+2*abs(t-original_t))/(1+min(t,left)**2))]
    return [c,s,e,cut//e,cut%e,lo,lo,hi,hi]
def read_level(folder,record):
    f=folder/record['measure'];data=f.read_bytes();require(digest(data)==record['measure_sha256'],'measure checksum')
    a=json.loads(gzip.decompress(data));raw=(folder/record['receipts']).read_bytes();require(digest(raw)==record['receipts_sha256'],'receipt checksum')
    receipts=[json.loads(line) for line in gzip.decompress(raw).splitlines()]
    return a,receipts
@lru_cache(128)
def check_rows(encoded):
    a=json.loads(encoded);rows=list(bm.rows(a));return digest(input_bytes(rows)),len(rows)
def verify(folder):
    m=json.load(open(folder/'manifest.json'));kernel=m.get('kernel','square');require(kernel in ('square','octagon','octagon-gram'),'unknown kernel');source={'square':'bmcheck.cpp','octagon':'octagon.cpp','octagon-gram':'gram.cpp'}[kernel];require(digest((here/source).read_bytes())==m['native_sha256'] and digest((here/'bm.py').read_bytes())==m['wrapper_sha256'],'source checksum')
    require((bm.G,bm.DS,bm.M)==(2**30,2**32,2**48),'wrong fixed point units')
    n=m['n'];L=F(m['side']);intervals=[];seen=set();nodes=0;basis=None
    for level in m['levels']:
        a,receipts=read_level(folder,level);k=level['K'];D=F(a['proof_net']['step']);B=F(a['B'])
        require(0<L<=20 and a['n']==n and F(a['L'])==L and a['proof_net']['last']==k and D==F(83,200*k) and 0<D<1,'wrong measure domain')
        require(0<B and B*(1+D/(1-D*D/4))<1,'angular core escapes')
        fields={j:a[j]for j in ('n','L','rectangles','total_mass','points')}
        enc=json.dumps(fields,sort_keys=True,separators=(',',':'));key=digest(enc.encode())
        require(basis in (None,key),'measure changed between angular levels');basis=key
        rd,count=check_rows(enc);require(rd==level['rects_sha256'] and count==level['rectangles'],'integer inputs changed')
        for row in receipts:
            r=row['r'];require(isinstance(r,int) and 0<=r<=k and (k,r)not in seen and row['verdict']=='PASS','invalid receipt')
            require(row['header']==header(a,r,kernel) and row['nodes']==2*row['leaves']-1 and row['leaves']>0 and 0<=row['depth']<=65 and row['lower_units']>=bm.M,'unverified center domain')
            seen.add((k,r));t=r*D;intervals.append((max(F(0),t-D/2),t+D/2));nodes+=row['nodes']
    end=F(0)
    for left,right in sorted(intervals):
        require(left<=end,'uncovered orientation interval');end=max(end,right)
    require(end*end+2*end>=1,'missing orientations near 45 degrees')
    require(len(seen)==m['directions'] and nodes==m['nodes'],'incorrect proof totals')
    v=json.load(open(folder/'verification.json'));require(v['n']==n and F(v['side'])==L and v['verified_bins']==len(seen) and v['nodes']==nodes,'incorrect result')
    return m
if __name__=='__main__':
    for folder in sorted(here.glob('*/manifest.json')):
        result=verify(folder.parent);print(result['n'],result['side'],result['directions'],flush=True)
