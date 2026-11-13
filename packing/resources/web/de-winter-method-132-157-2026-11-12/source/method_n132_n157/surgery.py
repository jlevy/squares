import numpy as np, math
import slp
ATOL=0.15
def nrm(t): return (t+np.pi/4)%(np.pi/2)-np.pi/4
def overlaps(P,q,tol=1e-9):
    """does square q (x,y,th) overlap any square in P (array)?"""
    if len(P)==0: return False
    d=np.hypot(P[:,0]-q[0],P[:,1]-q[1]); idx=np.nonzero(d<1.4143)[0]
    if len(idx)==0: return False
    Q=np.vstack([P[idx],q[None,:]]); m=len(idx)
    pairs=np.stack([np.arange(m),np.full(m,m)],1)
    X,Y,_,_=slp.verts(Q)
    g=slp.pair_data(Q,pairs,X,Y)[0]
    return bool((g<-tol).any())
def transpose(P):
    Q=P.copy(); Q[:,0]=P[:,1]; Q[:,1]=P[:,0]; Q[:,2]=nrm(np.pi/2-P[:,2]); return Q
def up_y(Sx,Sy,P,yc,extra=0.01):
    """insert one layer above the horizontal cut y=yc. returns Sy_new,P_new,n_added"""
    P=P.copy(); P[:,2]=nrm(P[:,2])
    lower=P[:,1]<=yc; up=~lower
    step=1.0/np.cos(P[:,2])
    near=lower&(P[:,1]>yc-1.3)
    shift=(step[near].max() if near.any() else 1.0)+extra
    P2=P.copy(); P2[up,1]+=shift
    order=np.argsort(-P[:,1]); new=[]
    for i in order:
        if not lower[i] or P[i,1]<yc-2.0: continue
        q=np.array([P[i,0],P[i,1]+step[i],P[i,2]])
        if q[1]+0.5*(abs(math.cos(q[2]))+abs(math.sin(q[2])))>Sy+shift+1e-9: continue
        if overlaps(P2,q,tol=ATOL): continue
        if new and overlaps(np.array(new),q,tol=ATOL): continue
        new.append(q)
    Pn=np.vstack([P2]+([np.array(new)] if new else []))
    return Sy+shift,Pn,len(new)
def up_step(S,P,xc,yc):
    Sy,P1,ny=up_y(S,S,P,yc)
    T=transpose(P1)                   # now x<->y ; box is (Sy) x (S)
    Sx,T2,nx=up_y(Sy,S,T,xc)
    P2=transpose(T2)
    return max(Sx,Sy),P2,ny,nx
def down_y(Sx,Sy,P,yc,slack=0.02):
    """delete every square whose vertical lattice cell (height 1/cos(theta)) contains the cut y=yc and lower the rest.
    returns Sy_new,P_new,n_removed"""
    P=P.copy(); P[:,2]=nrm(P[:,2])
    h=1.0/np.cos(P[:,2])
    rem=(P[:,1]>=yc-h/2)&(P[:,1]<yc+h/2)
    up=(P[:,1]>=yc+h/2)
    shift=1.0-slack
    P2=P.copy(); P2[up,1]-=shift
    return Sy-shift,P2[~rem],int(rem.sum())
def down_step(S,P,xc,yc):
    Sy,P1,ny=down_y(S,S,P,yc)
    T=transpose(P1)
    Sx,T2,nx=down_y(Sy,S,T,xc)
    return max(Sx,Sy),transpose(T2),ny,nx
