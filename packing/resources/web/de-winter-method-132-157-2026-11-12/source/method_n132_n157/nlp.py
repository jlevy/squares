"""IPOPT (via CasADi) local optimiser with fixed separating-axis assignment, re-selected between solves."""
import numpy as np, math, time, casadi as ca
import slp
def select(S,P,reach,vspan):
    n=len(P); X,Y,_,_=slp.verts(P)
    pairs=slp.get_pairs(P,math.sqrt(2)+reach)
    g,A,B,ax,sg,vals=slp.pair_data(P,pairs,X,Y)
    keep=g<reach
    A,B,ax,sg,vals=A[keep],B[keep],ax[keep],sg[keep],vals[keep]
    mask=vals<=(vals.min(1)[:,None]+vspan)
    pi,vi=np.nonzero(mask)
    return A[pi],vi,B[pi],ax[pi],sg[pi]
def solve_once(S,P,reach=0.25,vspan=0.3,dmax=0.3,tmax_th=0.25,tol=1e-11,maxiter=300,frozen=None,verbose=False,Slo=None):
    n=len(P)
    a_,vi,b_,ax,sg=select(S,P,reach,vspan)
    x=ca.MX.sym('x',n); y=ca.MX.sym('y',n); th=ca.MX.sym('th',n); s=ca.MX.sym('s')
    c=ca.cos(th); sn=ca.sin(th)
    al=[int(v) for v in a_]; bl=[int(v) for v in b_]
    ox=ca.DM(slp.OX[vi]); oy=ca.DM(slp.OY[vi])
    wx=x[al]+ox*c[al]-oy*sn[al]; wy=y[al]+ox*sn[al]+oy*c[al]
    m0=ca.DM((ax==0).astype(float)); m1=ca.DM((ax==1).astype(float)); sgd=ca.DM(sg)
    axx=m0*c[bl]-m1*sn[bl]; axy=m0*sn[bl]+m1*c[bl]
    gp=sgd*((wx-x[bl])*axx+(wy-y[bl])*axy)-0.5
    # walls: all vertices of squares near walls
    X,Y,_,_=slp.verts(P)
    near=np.nonzero((X.min(1)<dmax+0.8)|(Y.min(1)<dmax+0.8)|(X.max(1)>S-dmax-0.8)|(Y.max(1)>S-dmax-0.8))[0]
    ii=np.repeat(near,4); vv=np.tile(np.arange(4),len(near)); il=[int(v) for v in ii]
    oxw=ca.DM(slp.OX[vv]); oyw=ca.DM(slp.OY[vv])
    vx=x[il]+oxw*c[il]-oyw*sn[il]; vy=y[il]+oxw*sn[il]+oyw*c[il]
    g=ca.vertcat(gp,vx,vy,s-vx,s-vy)
    z=ca.vertcat(x,y,th,s)
    nlp={'x':z,'f':s,'g':g}
    opts={'ipopt.print_level':5 if verbose else 0,'print_time':0,'ipopt.tol':tol,'ipopt.constr_viol_tol':1e-11,'ipopt.acceptable_tol':1e-9,
          'ipopt.max_iter':maxiter,'ipopt.mu_strategy':'adaptive','ipopt.bound_push':1e-9,'ipopt.bound_frac':1e-9,'ipopt.slack_bound_push':1e-9,'ipopt.slack_bound_frac':1e-9,
          'ipopt.mu_init':1e-4,'ipopt.sb':'yes','ipopt.linear_solver':'mumps'}
    solver=ca.nlpsol('S','ipopt',nlp,opts)
    z0=np.concatenate([P[:,0],P[:,1],P[:,2],[S]])
    lb=np.concatenate([P[:,0]-dmax,P[:,1]-dmax,P[:,2]-tmax_th,[S-2*dmax if Slo is None else Slo]]); ub=np.concatenate([P[:,0]+dmax,P[:,1]+dmax,P[:,2]+tmax_th,[S+0.5]])
    if frozen is not None:
        fz=np.asarray(frozen)
        for o in (0,n,2*n): lb[o+fz]=z0[o+fz]; ub[o+fz]=z0[o+fz]
    r=solver(x0=z0,lbx=lb,ubx=ub,lbg=0,ubg=ca.inf)
    zz=np.array(r['x']).ravel()
    Pn=np.stack([zz[:n],zz[n:2*n],zz[2*n:3*n]],1); Sn=float(zz[3*n])
    st=solver.stats()
    return Sn,Pn,st['return_status'],st['iter_count']
def fix(S,P):
    """tiny uniform inflation to make a solution with violation ~1e-10 exactly feasible"""
    v=slp.violation(S,P)
    for _ in range(3):
        if v<=0: break
        lam=1+4*v; P=P.copy(); P[:,:2]=P[:,:2]*lam+v; S=S*lam+2*v
        v=slp.violation(S,P)
    return S,P,v
def compact(S,P,rounds=30,verbose=False,tmax=None,stop_above=None,dmax=0.12,tmax_th=0.06,tphase=True,frozen=None,gtol=1e-10):
    """LP translation phase, then repeated IPOPT solves with complete pair model. returns S,P,viol"""
    t0=time.time(); v=slp.violation(S,P)
    if tphase and v<=2e-10:
        S,P,v=slp.tphase(S,P,frozen=frozen)
        if verbose: print('tphase S=%.12f v=%.1e %.1fs'%(S,v,time.time()-t0),flush=True)
    best=(S,P,v); reach=2*math.sqrt(2)*dmax+1.42*tmax_th+0.02; fails=0
    for k in range(rounds):
        try:
            Sn,Pn,status,its=solve_once(best[0],best[1],reach=reach,vspan=1.5*tmax_th+0.05,dmax=dmax,tmax_th=tmax_th,frozen=frozen)
        except Exception as e:
            if verbose: print('ipopt error',e)
            break
        vn=slp.violation(Sn,Pn)
        if verbose: print('round',k,'S=%.12f viol=%.2e %s its=%d %.1fs'%(Sn,vn,status,its,time.time()-t0),flush=True)
        if vn>1e-7:
            fails+=1
            if fails>=2: break
            continue
        Sn,Pn,vn=fix(Sn,Pn)
        gain=best[0]-Sn
        if Sn<best[0] and vn<=0: best=(Sn,Pn,vn)
        if gain<gtol: break
        if tmax is not None and time.time()-t0>tmax: break
        if stop_above is not None and k>=4 and best[0]>stop_above: break
    return best
