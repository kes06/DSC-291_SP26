import itertools
import math
import random
import time


def sign_plus(x):
    return 1 if x >= 0 else -1


def dot(w, x):
    s = 0.0
    for wi, xi in zip(w, x):
        s += wi * xi
    return s


def make_sparse_target(d, k_true=2, seed=0):
    rng = random.Random(seed)
    w_true = [0.0] * d
    coords = list(range(d))
    rng.shuffle(coords)
    support = coords[:k_true]
    for idx in support:
        w_true[idx] = rng.choice([-1.5, -1.0, 1.0, 1.5])
    return w_true


def sample_from_target(n, w_true, noise=0.4, seed=0):
    rng = random.Random(seed)
    d = len(w_true)

    X, y = [], []
    for _ in range(n):
        x = [rng.gauss(0.0, 1.0) for _ in range(d)]
        z = dot(w_true, x) + noise * rng.gauss(0.0, 1.0)
        X.append(x)
        y.append(sign_plus(z))
    return X, y


def agreement(w, X, y):
    c = 0
    for xi, yi in zip(X, y):
        if sign_plus(dot(w, xi)) == yi:
            c += 1
    return c / len(X)


def logistic_objective(w, X, y, lam):
    total = 0.0
    for xi, yi in zip(X, y):
        yz = yi * dot(w, xi)
        # stable log(1+exp(-yz))
        if yz >= 0:
            total += math.log1p(math.exp(-yz))
        else:
            total += -yz + math.log1p(math.exp(yz))
    total /= len(X)
    l1 = sum(abs(v) for v in w)
    return total + lam * l1


def train_logistic_l1_subgrad(X, y, lam=0.02, lr=0.2, steps=150):
    d = len(X[0])
    n = len(X)
    w = [0.0] * d
    for t in range(steps):
        grad = [0.0] * d
        for xi, yi in zip(X, y):
            yz = yi * dot(w, xi)
            # derivative of log(1+exp(-yz)) wrt w: -yi*xi/(1+exp(yz))
            coeff = -yi / (1.0 + math.exp(yz))
            for j in range(d):
                grad[j] += coeff * xi[j]
        for j in range(d):
            grad[j] /= n
            if w[j] > 0:
                grad[j] += lam
            elif w[j] < 0:
                grad[j] -= lam
            else:
                # any value in [-lam, lam] is valid; pick 0 for stability
                pass
        eta = lr / math.sqrt(t + 1.0)
        for j in range(d):
            w[j] -= eta * grad[j]
    return w


def sparse_grid_search(X, y, k, grid_vals):
    d = len(X[0])
    best_w = [0.0] * d
    best_acc = -1.0
    supports = []
    for s in range(0, k + 1):
        supports.extend(itertools.combinations(range(d), s))

    for S in supports:
        if len(S) == 0:
            w = [0.0] * d
            acc = agreement(w, X, y)
            if acc > best_acc:
                best_acc = acc
                best_w = w
            continue

        for coeffs in itertools.product(grid_vals, repeat=len(S)):
            w = [0.0] * d
            for idx, c in zip(S, coeffs):
                w[idx] = float(c)
            acc = agreement(w, X, y)
            if acc > best_acc:
                best_acc = acc
                best_w = w
    return best_w, best_acc


def run_once(n, d, k, seed):
    w_true = make_sparse_target(d=d, k_true=min(2, k), seed=seed)
    Xtr, ytr = sample_from_target(n=n, w_true=w_true, seed=seed + 1)
    Xva, yva = sample_from_target(n=max(200, n // 2), w_true=w_true, seed=seed + 2)

    t0 = time.perf_counter()
    wb, acc_tr_b = sparse_grid_search(Xtr, ytr, k=k, grid_vals=[-2, -1, 1, 2])
    t1 = time.perf_counter()
    acc_va_b = agreement(wb, Xva, yva)

    t2 = time.perf_counter()
    ws = train_logistic_l1_subgrad(Xtr, ytr, lam=0.02, lr=0.25, steps=160)
    t3 = time.perf_counter()
    acc_tr_s = agreement(ws, Xtr, ytr)
    acc_va_s = agreement(ws, Xva, yva)
    obj_s = logistic_objective(ws, Xtr, ytr, lam=0.02)

    nnz_s = sum(1 for v in ws if abs(v) > 1e-6)

    return {
        "baseline_time": t1 - t0,
        "baseline_train_acc": acc_tr_b,
        "baseline_val_acc": acc_va_b,
        "surrogate_time": t3 - t2,
        "surrogate_train_acc": acc_tr_s,
        "surrogate_val_acc": acc_va_s,
        "surrogate_obj": obj_s,
        "surrogate_nnz": nnz_s,
    }


def avg_runs(configs, repeats=3):
    out = []
    for cfg in configs:
        agg = None
        for r in range(repeats):
            m = run_once(seed=100 + 17 * r + 3 * cfg["n"] + cfg["d"], **cfg)
            if agg is None:
                agg = {k: 0.0 for k in m.keys()}
            for k, v in m.items():
                agg[k] += v
        for k in agg:
            agg[k] /= repeats
        out.append((cfg, agg))
    return out


def print_table(title, rows):
    print("\n" + title)
    print("n d k | t_sparse(s) t_sur(s) | trainAcc_sparse trainAcc_sur | valAcc_sparse valAcc_sur | surrogate_obj nnz_sur")
    for cfg, m in rows:
        print(
            f"{cfg['n']:>3} {cfg['d']:>2} {cfg['k']:>1} | "
            f"{m['baseline_time']:.4f} {m['surrogate_time']:.4f} | "
            f"{m['baseline_train_acc']:.3f} {m['surrogate_train_acc']:.3f} | "
            f"{m['baseline_val_acc']:.3f} {m['surrogate_val_acc']:.3f} | "
            f"{m['surrogate_obj']:.3f} {m['surrogate_nnz']:.1f}"
        )


def main():
    # scaling in d (n fixed)
    cfg_d = [{"n": 120, "d": d, "k": 2} for d in [6, 8, 10, 12]]
    rows_d = avg_runs(cfg_d, repeats=3)
    print_table("Scaling with d (n=120, k=2)", rows_d)

    # scaling in n (d fixed)
    cfg_n = [{"n": n, "d": 10, "k": 2} for n in [60, 120, 180, 240]]
    rows_n = avg_runs(cfg_n, repeats=3)
    print_table("Scaling with n (d=10, k=2)", rows_n)


if __name__ == "__main__":
    main()
