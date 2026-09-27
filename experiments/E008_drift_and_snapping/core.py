import itertools, sys, time, numpy as np
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from veritas_holo import expi
T,C=(1,0,2,3,4),(1,2,3,4,0)
PERMS=list(itertools.permutations(range(5))); IDX={p:i for i,p in enumerate(PERMS)}
def pm(g):
    m=np.zeros((5,5)); 
    for i in range(5): m[g[i],i]=1
    return m
P=np.stack([pm(p) for p in PERMS])            # codebook: 120 exact class matrices
NEXT=np.array([[IDX[tuple(g[p[i]] for i in range(5))] for g in (T,C)] for p in PERMS])
def haar(n,rng):
    q,r=np.linalg.qr(rng.standard_normal((n,n))+1j*rng.standard_normal((n,n))); return q*(np.diag(r)/abs(np.diag(r)))
def run(seed,L,delta,snap_every,n=32):
    rng=np.random.default_rng(seed)
    V=haar(5,rng)
    ops=np.stack([V@pm(g)@V.conj().T for g in (T,C)])
    if delta>0:
        ops=np.stack([expi(delta*(lambda m:(m+m.conj().T)/2)(rng.standard_normal((5,5))+1j*rng.standard_normal((5,5))))@o for o in ops])
    book=np.einsum('ij,kjl,ml->kim',V,P,V.conj())   # codebook in the rotated basis
    words=rng.integers(0,2,(n,L))
    h=np.broadcast_to(np.eye(5,dtype=complex),(n,5,5)).copy(); s=np.full(n,IDX[tuple(range(5))])
    for k in range(L):
        h=ops[words[:,k]]@h; s=NEXT[s,words[:,k]]
        if snap_every and (k+1)%snap_every==0:
            d=((abs(h[:,None]-book[None])**2).sum((2,3))); h=book[np.argmin(d,1)].copy()
    d=((abs(h[:,None]-book[None])**2).sum((2,3))); pred=np.argmin(d,1)
    dev=float(np.max(np.linalg.norm(h-book[s],axis=(1,2))))
    return float(np.mean(pred==s)), dev
if __name__=="__main__":
    for L in (10**3,10**4,10**5):
        t=time.time()
        print(L, 'exact-rotated', run(1,L,0,0), 'noisy1e-2', run(1,L,1e-2,0), 'noisy1e-2+snap1', run(1,L,1e-2,1), 'noisy1e-2+snap10', run(1,L,1e-2,10), round(time.time()-t,1), flush=True)
