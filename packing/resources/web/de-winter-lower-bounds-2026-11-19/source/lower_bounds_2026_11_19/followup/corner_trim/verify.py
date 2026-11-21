"""Check a local repair and every implied periodic bound using the anchor certificate."""
from fractions import Fraction as F
from pathlib import Path
from tempfile import TemporaryDirectory
from concurrent.futures import ThreadPoolExecutor
import gzip,hashlib,json,math,subprocess,sys

def verify(folder,outer,replay=False,workers=4):
    anchor=folder/'proof'
    claim=json.loads((folder/'claim.json').read_text())
    mf=anchor/'manifest.json'
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(mf)==claim['source_sha']
    meta=outer.check.verify(anchor)
    outer.check_case(dict(n=meta['n'],exact=meta['side'],previous_upper_endpoint='0'),False,workers,anchor)
    data,_=outer.check.read_level(anchor,meta['levels'][0])
    S,C,need=map(F,(claim['anchor_side'],claim['corner'],claim['removed_mass']))
    assert S==F(data['L']) and 0<C<(S-3)/2 and need>0
    bm=outer.check.bm
    recipe=folder/'multipliers.json'
    factors=json.loads(recipe.read_text()) if recipe.exists() else None
    if claim.get('split_long_rectangles'):
        split_module=outer.load_module(folder.parent/'split_corner.py','split_corner_measure')
        refined=split_module.split_rows(data,C)
        assert sum(F(r['mass']) for r in refined['rectangles'])==F(data['total_mass'])
        data=refined
    records=[]
    available=F(0)
    proposal=F(0)
    for idx,r in enumerate(data['rectangles']):
        a,b,A,B=map(F,r['rectangle'])
        near=(A<=C or a>=S-C) and (B<=C or b>=S-C)
        w=F(r['mass'])
        coef=F(factors[str(idx)]) if factors is not None and near else F(1)
        assert coef>=0
        if near:
            available+=w
            proposal+=w*coef
        records.append((a,b,A,B,w,near,coef))
    ratio=(available-need)/proposal
    assert ratio==F(claim['factor'])>0 and available==F(claim['available'])
    # Rebuild the complete corrected source, then retain the terms used for the clocked local tests.
    modified=[];subset=[]
    for a,b,A,B,w,near,coef in records:
        r=dict(rectangle=list(map(str,(a,b,A,B))),mass=str(w*coef*ratio if near else w))
        modified.append(r)
        if min(a,S-A)<=C+F(142,100) and min(b,S-B)<=C+F(142,100):subset.append(r)
    assert sum(F(r['mass']) for r in modified)==F(data['total_mass'])-need
    local=dict(data,rectangles=subset,total_mass=str(sum(F(r['mass'])for r in subset)))
    radius=F(707107,10**6)
    assert 2*radius**2>1
    low=math.floor(bm.G*(S-C-radius))
    assert low==claim['lower_grid']
    rows=[r for r in bm.rows(local) if r[6]>=low-math.ceil(bm.G*radius) and r[7]>=low-math.ceil(bm.G*radius)]
    raw=outer.check.input_bytes(rows)
    assert hashlib.sha256(raw).hexdigest()==claim['rect_sha']
    receipts=json.loads(gzip.decompress((folder/'receipts.json.gz').read_bytes()))
    spans=[];keys=set()
    for r in receipts:
        k,j=r['K'],r['r']
        assert isinstance(k,int) and k>0 and isinstance(j,int) and 0<=j<=k and (k,j) not in keys
        keys.add((k,j))
        step=F(83,200*k)
        hdr=outer.check.header(dict(data,B='1',proof_net=dict(step=str(step),last=k)),j,'octagon-gram')
        hdr[5]=max(hdr[5],low);hdr[6]=max(hdr[6],low)
        assert hdr==r['header'] and hdr[5]<=hdr[7] and hdr[6]<=hdr[8]
        assert r['verdict']=='PASS' and r['nodes']==2*r['leaves']-1 and r['leaves']>0 and 0<=r['depth']<=65 and r['lower_units']>=bm.M
        spans.append((max(F(0),(j-F(1,2))*step),(j+F(1,2))*step))
    end=F(0)
    for left,right in sorted(spans):
        assert left<=end
        end=max(end,right)
    assert end**2+2*end>=1 and len(receipts)==claim['directions'] and sum(r['nodes']for r in receipts)==claim['nodes']
    period=outer.load_module(folder.parent.parent/'repeated/period_verify.py','trimmed_period')
    z=dict(data,rectangles=modified,total_mass=str(F(data['total_mass'])-need))
    M,b,c=period.inspect(z,3)
    for entry in json.loads((folder/'bounds.json').read_text()):
        d=entry['offset'];m=M+2*d*b+d*d*c
        assert d>=-1 and F(entry['side'])==S+d and m==F(entry['mass'])<entry['n'] and F(entry['side'])>F(entry['previous_upper_endpoint'])
    d=claim['offset']
    assert M+2*d*b+d*d*c==F(claim['new_mass']) and F(claim['old_mass'])-need==F(claim['new_mass'])<claim['n']
    if replay:
        with TemporaryDirectory() as td:
            tmp=Path(td);binary=tmp/'gram';grid=tmp/'rectangles';grid.write_bytes(raw)
            src=outer.project/'proof/gram.cpp'
            assert digest(src)==meta['native_sha256']
            subprocess.run(['c++','-O3','-std=c++17',str(src),'-o',str(binary)],check=True)
            def execute(r):
                hdr=tmp/f"h{r['K']}_{r['r']}";hdr.write_text(' '.join(map(str,r['header'])))
                ans=subprocess.run([binary,grid,hdr,'350000'],capture_output=True,text=True,check=True).stdout.split()
                assert ans==list(map(str,[r[k] for k in ('verdict','nodes','leaves','clips','depth','lower_units')]))
            with ThreadPoolExecutor(workers) as ex:list(ex.map(execute,receipts))
    return len(receipts)
