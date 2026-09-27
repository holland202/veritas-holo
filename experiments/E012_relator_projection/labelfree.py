"""Label-free pipeline pilot: choose relator orders by fit + finite closure, build the closure codebook with its own
multiplication table, certify with that table, then check long runs against the true labels."""
import sys, numpy as np, itertools, time, json
sys.path.insert(0,"."); import relproj as rp, core, cert
def closure(R, limit=1500, tol=1e-6):
    els=[np.eye(R.shape[1],dtype=complex)]; words=[()]; flat=[els[0].reshape(-1)]; i=0
    while i < len(els):
        for g in range(len(R)):
            x=R[g]@els[i]; d=np.sum(abs(np.array(flat)-x.reshape(-1))**2,1)
            if d.min()>tol:
                els.append(x); words.append(words[i]+(g,)); flat.append(x.reshape(-1))
                if len(els)>limit: return None
        i+=1
    E=np.array(els); F=np.array(flat)
    table=np.array([[int(np.argmin(np.sum(abs(F-(R[g]@E[e]).reshape(-1))**2,1))) for g in range(len(R))] for e in range(len(E))])
    return E, words, table
def choose(ops, ks=range(2,7)):
    best=None
    for tri in itertools.product(ks,ks,ks):
        R=rp.project(ops,20,tri); res=float(np.linalg.norm(R[0]-ops[0])+np.linalg.norm(R[1]-ops[1]))
        if best is not None and res>=best[0]: continue
        c=closure(R)
        if c is None: continue
        best=(res,tri,c)
    return best
def margin_table(book, ops, table):
    worst=np.inf
    for e in range(len(book)):
        for g in range(len(ops)):
            x=ops[g]@book[e]; d=np.sqrt((abs(x[None]-book)**2).sum((1,2))); t=table[e,g]
            worst=min(worst, float(np.min(np.delete(d,t))-d[t]))
    return worst
def run(seed, delta, L=10000, n=32):
    _,ops,_=core.setup(seed,delta)
    res,tri,(book,words,table)=choose(ops)
    m=margin_table(book,ops,table)
    # map discovered elements to true states through the word that reached them
    def state(w):
        s=core.E
        for g in w: s=core.NEXT[s,g]
        return s
    label=np.array([state(w) for w in words])
    rng=np.random.default_rng(seed+10**6); W=rng.integers(0,2,(n,L))
    h=np.broadcast_to(np.eye(5,dtype=complex),(n,5,5)).copy(); s=np.full(n,core.E)
    for k in range(L):
        h=ops[W[:,k]]@h; s=core.NEXT[s,W[:,k]]
        idx=np.argmin((abs(h[:,None]-book[None])**2).sum((2,3)),1); h=book[idx].copy()
    acc=float(np.mean(label[idx]==s))
    return dict(seed=seed,delta=delta,orders=list(tri),size=len(book),margin=round(m,4),acc=acc,
                bijective=len(set(label.tolist()))==len(label)==120)
if __name__=="__main__":
    from concurrent.futures import ProcessPoolExecutor
    a,b,out=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
    jobs=[(s,d) for s in range(a,b) for d in (0.1,0.15,0.2,0.3)]
    with ProcessPoolExecutor(2) as ex, open(out,"a") as fh:
        for r in ex.map(run,*zip(*jobs)):
            fh.write(json.dumps(r)+"\n"); fh.flush(); print(r,flush=True)
