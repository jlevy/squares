"""Construct certified parts of the lower-left walls and corner in the source family."""
from fractions import Fraction as F
def altered_wall(case,fam,period,fixed,moving,fs):
    pieces=[];d0,d1=fam['d0'],fam['d1']
    def include(kind,line,lo,hi,density,top=None,tag='fixed'):
        end=min(F(4),hi);top=line if top is None else top
        if lo<end and density>0 and line<=4 and top<=4:pieces.append((int(kind=='v'),lo,end,line,top,density,tag))
    for row in fixed:include(*row)
    for row in fs.repeated(fs.reflect_profile(period),3,True):include(*row,tag='left')
    for kind,c,l,h,w in moving+fs.repeated(period,3):
        if kind=='v':include(kind,c+d0,l,h,w,c+d1,'moving')
        else:include(kind,c,l+d1,h+d0,w,tag='horizontal')
    for x,y,w in fam['V']:include('h',y,x,2+d0,w,tag='seam')
    for j in range(72,160):include('h',F(j,40),F(9,5),F(4),F(1,40),F(j+1,40),'area')
    cuts={int(i):tuple(map(F,(l,h,p)))for i,l,h,p in case['segments']}
    assert len(cuts)==len(case['segments'])and set(cuts)<=set(range(len(pieces)))and cuts
    remaining=[];support=[];saving=F(0)
    for index,(vert,lo,hi,line,top,dens,scope)in enumerate(pieces):
        runs=[(lo,hi,dens)]
        if index in cuts:
            l,h,frac=cuts[index];assert scope!='area'and lo<=l<h<=hi and 0<frac<=1
            box=(line,l,top,h)if vert else(l,line,h,top);assert 0<=min(box) and max(box)<=F(5,2)
            saving+=(h-l)*dens*frac;support.append(box);runs=[(lo,l,dens),(l,h,dens*(1-frac)),(h,hi,dens)]
        for l,h,w in runs:
            if l<h and w>0:remaining.append((vert,l,h,line,top,w*(h-l)))
    assert saving==F(case['subtraction_per_corner'])and saving>0
    return remaining,support,[],[]
