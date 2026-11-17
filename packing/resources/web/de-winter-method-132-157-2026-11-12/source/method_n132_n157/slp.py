"""Sequential LP engine for unit squares in a square.  P: (n,3) x,y,theta ; S side.
T-steps: rotations frozen (model exact for the chosen separating axes).
R-steps: rotations free, with second-order correction (re-solve with curvature-corrected right-hand side)."""
import numpy as np, math, time
from scipy.spatial import cKDTree
from scipy.optimize import linprog
from scipy.sparse import coo_matrix, csr_matrix, hstack
OX=np.array([0.5,-0.5,-0.5,0.5]); OY=np.array([0.5,0.5,-0.5,-0.5])
LPOPT={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10}
NLP=[0]
def verts(P):
    c=np.cos(P[:,2])[:,None]; s=np.sin(P[:,2])[:,None]
    X=P[:,0][:,None]+OX*c-OY*s; Y=P[:,1][:,None]+OX*s+OY*c
    dX=-OX*s-OY*c; dY=OX*c-OY*s
    return X,Y,dX,dY
def pair_data(P,pairs,X,Y):
    i=pairs[:,0]; j=pairs[:,1]
    A=np.concatenate([i,j]); B=np.concatenate([j,i])
    cb=np.cos(P[B,2]); sb=np.sin(P[B,2])
    dx=X[A]-P[B,0][:,None]; dy=Y[A]-P[B,1][:,None]
    pu=dx*cb[:,None]+dy*sb[:,None]; pv=-dx*sb[:,None]+dy*cb[:,None]
    cand=np.stack([pu.min(1)-0.5, -pu.max(1)-0.5, pv.min(1)-0.5, -pv.max(1)-0.5],axis=1)
    m=len(pairs)
    both=np.concatenate([cand[:m],cand[m:]],axis=1)
    k=both.argmax(1); g=both[np.arange(m),k]
    sel=np.where(k<4,np.arange(m),np.arange(m)+m); kk=k%4
    As=A[sel]; Bs=B[sel]; ax=kk//2; sg=np.where(kk%2==0,1.0,-1.0)
    p=np.where((ax==0)[:,None],pu[sel],pv[sel])
    vals=sg[:,None]*p-0.5
    return g,As,Bs,ax,sg,vals
def get_pairs(P,r):
    t=cKDTree(P[:,:2]); return t.query_pairs(r,output_type='ndarray')
def violation(S,P):
    X,Y,_,_=verts(P)
    w=min(X.min(),Y.min(),S-X.max(),S-Y.max())
    pairs=get_pairs(P,1.4143)
    if len(pairs)==0: return max(0.0,-w)
    g=pair_data(P,pairs,X,Y)[0]
    return max(0.0,-w,-g.min())
def build(S,P,r,rth):
    """rows: f0 + G z >= 0 ; z=[dx,dy,dth,dS].  returns G,f0,desc"""
    n=len(P); X,Y,dX,dY=verts(P)
    reach=2*math.sqrt(2)*r+1.5*rth+1e-9
    vtol=3*rth+1e-9
    pairs=get_pairs(P,math.sqrt(2)+reach)
    rows=[];cols=[];dat=[];f0=[]; nr=0
    if len(pairs):
        g,A,B,ax,sg,vals=pair_data(P,pairs,X,Y)
        keep=g<reach
        g,A,B,ax,sg,vals=g[keep],A[keep],B[keep],ax[keep],sg[keep],vals[keep]
        cb=np.cos(P[B,2]); sb=np.sin(P[B,2])
        axx=np.where(ax==0,cb,-sb); axy=np.where(ax==0,sb,cb)
        dax=np.where(ax==0,-sb,-cb); day=np.where(ax==0,cb,-sb)
        mask=vals<=(vals.min(1)[:,None]+vtol)
        pi,vi=np.nonzero(mask)
        a_=A[pi]; b_=B[pi]; s_=sg[pi]
        wx=X[a_,vi]; wy=Y[a_,vi]; dwx=dX[a_,vi]; dwy=dY[a_,vi]
        f=vals[pi,vi]
        gAx=s_*axx[pi]; gAy=s_*axy[pi]
        gAt=s_*(dwx*axx[pi]+dwy*axy[pi])
        gBt=s_*((wx-P[b_,0])*dax[pi]+(wy-P[b_,1])*day[pi])
        k=len(pi); rid=np.arange(k)
        rows+= [rid,rid,rid,rid,rid,rid]; cols+=[a_,n+a_,2*n+a_,b_,n+b_,2*n+b_]; dat+=[gAx,gAy,gAt,-gAx,-gAy,gBt]
        f0.append(f); nr=k
        dp=(a_,vi,b_,ax[pi],s_)
    else:
        dp=(np.zeros(0,int),)*3+(np.zeros(0,int),np.zeros(0))
    tolw=r+0.71*rth+1e-9; dw=[]
    for wid,(arr,darr,off,sign,useS) in enumerate(((X,dX,0,1.0,False),(Y,dY,n,1.0,False),(X,dX,0,-1.0,True),(Y,dY,n,-1.0,True))):
        f=arr if not useS else S-arr
        ii,vv=np.nonzero(f<tolw+(2*r if useS else 0))
        k=len(ii); rid=nr+np.arange(k)
        rows+=[rid,rid]; cols+=[off+ii,2*n+ii]; dat+=[np.full(k,sign),sign*darr[ii,vv]]
        if useS:
            rows.append(rid); cols.append(np.full(k,3*n)); dat.append(np.ones(k))
        f0.append(f[ii,vv]); nr+=k; dw.append((ii,vv))
    rows=np.concatenate(rows); cols=np.concatenate(cols); dat=np.concatenate(dat); f0=np.concatenate(f0)
    G=coo_matrix((dat,(rows,cols)),shape=(nr,3*n+1)).tocsr()
    return G,f0,(dp,dw)
def evalf(S,P,desc):
    dp,dw=desc; X,Y,_,_=verts(P)
    a_,vi,b_,ax,s_=dp
    out=[]
    if len(a_):
        cb=np.cos(P[b_,2]); sb=np.sin(P[b_,2])
        axx=np.where(ax==0,cb,-sb); axy=np.where(ax==0,sb,cb)
        out.append(s_*((X[a_,vi]-P[b_,0])*axx+(Y[a_,vi]-P[b_,1])*axy)-0.5)
    for wid,(ii,vv) in enumerate(dw):
        arr=X if wid%2==0 else Y
        out.append(arr[ii,vv] if wid<2 else S-arr[ii,vv])
    return np.concatenate(out)
def solve(G,f0,n,r,rth,mode,rho,frozen,rotmask,dSlo,dShi,corr=None):
    nr=G.shape[0]
    A=hstack([G,csr_matrix(np.ones((nr,1)))],format='csr')
    c=np.zeros(3*n+2)
    if mode=='compact': c[3*n]=1.0; c[3*n+1]=rho
    else: c[3*n+1]=1.0
    rt=np.full(n,rth)
    if rotmask is not None: rt=np.where(rotmask,rth,0.0)
    lb=np.concatenate([np.full(2*n,-r),-rt,[dSlo,0.0]]); ub=np.concatenate([np.full(2*n,r),rt,[dShi,np.inf]])
    if frozen is not None:
        fz=np.asarray(frozen)
        for o in (0,n,2*n): lb[o+fz]=0; ub[o+fz]=0
    b=f0 if corr is None else f0+corr
    NLP[0]+=1
    res=linprog(c,A_ub=-A,b_ub=b,bounds=np.stack([lb,ub],1),method='highs',options=LPOPT)
    if res.status!=0: return None
    return res.x
def apply(S,P,z):
    n=len(P); Pn=P.copy(); Pn[:,0]+=z[:n]; Pn[:,1]+=z[n:2*n]; Pn[:,2]+=z[2*n:3*n]
    return S+z[3*n],Pn
def step(S,P,r,rth=0.0,mode='compact',rho=1000.0,frozen=None,rotmask=None,soc=2,srange=None):
    """one LP step (with second-order correction when rth>0). returns S,P,v or None"""
    n=len(P); G,f0,desc=build(S,P,r,rth)
    dS=(2*r+rth) if srange is None else srange
    lo,hi=(-dS,dS) if mode=='compact' else (0.0,0.0)
    z=solve(G,f0,n,r,rth,mode,rho,frozen,rotmask,lo,hi)
    if z is None: return None
    Sn,Pn=apply(S,P,z); vn=violation(Sn,Pn)
    if rth>0 and mode=='compact':
        for k in range(soc):
            if vn<=1e-12: break
            ft=evalf(Sn,Pn,desc); corr=ft-(f0+G@z[:3*n+1])
            z2=solve(G,f0,n,r,rth,mode,rho,frozen,rotmask,lo,hi,corr=corr)
            if z2 is None: break
            S2,P2=apply(S,P,z2); v2=violation(S2,P2)
            if v2<vn: z,Sn,Pn,vn=z2,S2,P2,v2
            else: break
    return Sn,Pn,vn
def compact(S,P,rT=0.2,rR=0.01,ftol=2e-10,maxouter=40,verbose=False,frozen=None,rotmask=None,tmax=None,nR=20,stop_above=None,vacc=1e-9):
    """minimise S from a (nearly) feasible start. returns S,P,viol"""
    t0=time.time(); v=violation(S,P)
    def log(*a):
        if verbose: print(*a,flush=True)
    r2=rR
    for outer in range(maxouter):
        S_start=S
        if v<=ftol:
            r=rT
            for it in range(40):
                out=step(S,P,r,0.0,'compact',frozen=frozen)
                ok=False
                if out is not None:
                    Sn,Pn,vn=out
                    if vn<=max(v,ftol) and Sn<S-1e-13:
                        ok=True; gain=S-Sn; S,P,v=Sn,Pn,vn
                if ok:
                    if gain<1e-11: break
                else:
                    r*=0.5
                    if r<1e-6: break
            log('outer',outer,'T: S=%.12f v=%.1e'%(S,v))
        r=r2; small=0
        for it in range(nR):
            out=step(S,P,r,r,'compact',frozen=frozen,rotmask=rotmask)
            ok=False
            if out is not None:
                Sn,Pn,vn=out
                if vn<=max(vacc,v) and Sn<S-1e-14:
                    ok=True; dS=S-Sn; S,P,v=Sn,Pn,vn
            if ok:
                r=min(r*1.6,rR)
                small=small+1 if dS<1e-12 else 0
                if small>=2: break
            else:
                r*=0.4
                if r<1e-9: break
        r2=max(min(r*4,rR),1e-6)
        for it in range(6):          # clean up residual violation
            if v<=ftol: break
            rr=max(30*v,1e-9)
            out=step(S,P,rr,rr,'compact',frozen=frozen,rotmask=rotmask,soc=1,srange=100*rr)
            if out is None: break
            Sn,Pn,vn=out
            if vn<v: S,P,v=Sn,Pn,vn
            else: break
        log('outer',outer,'R: S=%.12f v=%.1e r=%.1e  %.1fs'%(S,v,r,time.time()-t0))
        if abs(S_start-S)<1e-11 and v<=ftol: break
        if tmax is not None and time.time()-t0>tmax: break
        if stop_above is not None and outer>=1 and S>stop_above: break
    return S,P,v
def repair(S,P,rT=0.1,rR=0.02,maxit=150,target=2e-10,verbose=False,frozen=None,rotmask=None,tmax=None):
    """minimise max violation at fixed S (alternating T and R steps). returns P,v"""
    v=violation(S,P); r=rT; rr=rR; t0=time.time(); mode=0; fails=0
    for it in range(maxit):
        if v<=target: break
        if mode==0: out=step(S,P,r,0.0,'repair',frozen=frozen)
        else: out=step(S,P,rr,rr,'repair',frozen=frozen,rotmask=rotmask)
        acc=False
        if out is not None:
            _,Pn,vn=out
            if vn<v*(1-1e-3): P,v=Pn,vn; acc=True
        if acc:
            fails=0
            if mode==1: rr=min(rr*1.3,0.05)
        else:
            fails+=1
            if mode==0: r*=0.5
            else: rr*=0.5
        mode=1-mode
        if verbose and it%10==0: print(it,'viol=%.3e r=%.1e rr=%.1e'%(v,r,rr),flush=True)
        if (r<1e-5 and rr<1e-6) or fails>=8: break
        if tmax is not None and time.time()-t0>tmax: break
    return P,v

def tphase(S,P,rT=0.25,ftol=2e-10,frozen=None,maxit=60):
    """translation-only compaction (exact model). start must be feasible."""
    v=violation(S,P); r=rT
    if v>ftol: return S,P,v
    for it in range(maxit):
        out=step(S,P,r,0.0,'compact',frozen=frozen)
        ok=False
        if out is not None:
            Sn,Pn,vn=out
            if vn<=max(v,ftol) and Sn<S-1e-13:
                ok=True; gain=S-Sn; S,P,v=Sn,Pn,vn
        if ok:
            if gain<1e-9: break
        else:
            r*=0.5
            if r<1e-5: break
    return S,P,v
