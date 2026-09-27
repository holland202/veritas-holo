import sys, os, json, importlib.util, numpy as np
ROOT="/home/claude/veritas-holo"; sys.path.insert(0, ROOT)
spec=importlib.util.spec_from_file_location("e006run", os.path.join(ROOT,"experiments","E006_restart_diagnostic","run.py"))
e006=importlib.util.module_from_spec(spec); sys.modules["e006run"]=e006; spec.loader.exec_module(e006)
from veritas_holo.learn import train_operators
def round_spectrum(O,k):
    w,V=np.linalg.eig(O); roots=np.exp(2j*np.pi*np.arange(k)/k)
    R=V@np.diag(roots[np.argmin(abs(w[:,None]-roots[None]),1)])@np.linalg.inv(V)
    u,_,vh=np.linalg.svd(R); return u@vh
def project(ops, rounds=20):
    Rt,Rc=round_spectrum(ops[0],2),round_spectrum(ops[1],5)
    for _ in range(rounds):
        P=round_spectrum(Rt@Rc,4)            # E005 convention: "t c" = U_t U_c
        Rc=round_spectrum(0.5*(Rt.conj().T@P+Rc),5)
        Rt=round_spectrum(0.5*(P@Rc.conj().T+Rt),2)
    return np.stack([Rt,Rc])
def one(seed):
    ops=train_operators(e006.WORDS, e006.Y, e006.e005.DIM, np.random.default_rng(seed))
    s0,_=e006.relator_score(ops); a0=e006.e005.score(ops, seed)
    pr=project(ops); s1,_=e006.relator_score(pr); a1=e006.e005.score(pr, seed)
    return dict(seed=seed, score=s0, acc160=a0[160][0], score_proj=s1, acc160_proj=a1[160][0], dist=float(np.linalg.norm(pr-ops)))
if __name__=="__main__":
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(2) as ex, open(sys.argv[3],"a") as fh:
        for r in ex.map(one, range(int(sys.argv[1]), int(sys.argv[2]))):
            fh.write(json.dumps(r)+"\n"); fh.flush(); print(r, flush=True)
