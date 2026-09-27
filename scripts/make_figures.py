#!/usr/bin/env python3
"""Draw the README figures from the committed result files (never from typed numbers), plus the banner.

  python scripts/make_figures.py            # writes figures/*.png
"""
import glob
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "figures")
SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"  # validated categorical slots 1-3 (light)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": MUTED, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID,
                     "grid.linewidth": 0.6, "axes.axisbelow": True})


def load(name):
    with open(os.path.join(ROOT, "results", "verified", name), encoding="utf-8") as fh:
        return json.load(fh)


def title(ax, t, sub):
    import textwrap
    fig = ax.figure
    fig.text(0.02, 0.97, t, color=INK, fontsize=12, fontweight="bold", va="top")
    fig.text(0.02, 0.90, "\n".join(textwrap.wrap(sub, 105)), color=INK2, fontsize=9, va="top")
    fig._title_lines = 1 + len(textwrap.wrap(sub, 105))


def save(fig, name):
    top = 0.86 - 0.05 * (getattr(fig, "_title_lines", 1) - 1)
    fig.tight_layout(rect=(0, 0, 1, top))
    fig.savefig(os.path.join(OUT, name), dpi=160)
    plt.close(fig)


def e002():
    d = load("E002_x86_64.json")["mean_r2"]
    arms = ["SU2", "SU32-RANDOM", "SPECTRUM-SHAM", "SHOELACE", "ABELIAN", "SU2-LARGE"]
    vals = [d[a] for a in arms]
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    colors = [S1 if a != "SHOELACE" else S2 for a in arms]
    ax.barh(arms[::-1], vals[::-1], color=colors[::-1], height=0.55)
    for i, v in enumerate(vals[::-1]):
        ax.text(max(v, 0) + 0.02, i, f"{v:.4f}", va="center", color=INK2, fontsize=9)
    ax.set_xlim(-0.05, 1.18)
    ax.set_xlabel("mean held-out R² (20 seeds)")
    ax.grid(axis="y", visible=False)
    title(ax, "E002: holonomy carries a path's signed area",
          "Any noncommuting pair reads it out; commuting operators and large steps carry nothing. "
          "The shoelace formula (orange) gets it exactly for far less.")
    save(fig, "E002_area_readout.png")


def e004():
    d = load("E004_x86_64.json")["accuracy"]
    arms = ["REP", "TABLE", "DIAG", "COUNT-CEILING", "RANDOM-U", "SHAM"]
    labels = ["relation-respecting", "lookup table", "commuting (diag)", "count ceiling", "random noncommuting",
              "spectrum sham"]
    x = np.arange(len(arms))
    m40 = [np.mean(d[a]["40"]) for a in arms]
    m160 = [np.mean(d[a]["160"]) for a in arms]
    fig, ax = plt.subplots(figsize=(7.6, 4.0))
    ax.bar(x - 0.19, m40, 0.36, color=S1, label="L = 40")
    ax.bar(x + 0.19, m160, 0.36, color=S2, label="L = 160")
    ax.axhline(1 / 120, color=MUTED, lw=1, ls="--")
    ax.text(2.0, 1 / 120 + 0.03, "chance 1/120", color=MUTED, fontsize=8, ha="center")
    ax.set_xticks(x, labels, rotation=18, ha="right")
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("test accuracy (mean of 3 seeds)")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="x", visible=False)
    title(ax, "E004: tracking the S5 state needs the group's relations",
          "Noncommutativity alone is at chance; commuting state is capped by letter counts.")
    save(fig, "E004_state_tracking.png")


def e005():
    runs = load("E005_x86_64.json")["runs"]
    seeds = [r["seed"] for r in runs]
    x = np.arange(len(seeds))
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.bar(x - 0.26, [r["full"]["160"][0] for r in runs], 0.25, color=S1, label="learned unitary")
    ax.bar(x, [r["diag"]["160"][0] for r in runs], 0.25, color=S2, label="learned commuting (diag)")
    ax.bar(x + 0.26, [r["init"]["160"][0] for r in runs], 0.25, color=S3, label="untrained")
    ax.set_xticks(x, [f"seed {s}" for s in seeds])
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("accuracy at length 160")
    ax.legend(frameon=False, loc="center right", fontsize=9)
    ax.grid(axis="x", visible=False)
    title(ax, "E005: trained on words of length ≤ 8, tested at 160",
          "3 of 5 seeds learn operators that are exact 20× beyond the training horizon; 2 fail. "
          "Commuting training cannot.")
    save(fig, "E005_learned_extrapolation.png")


def e006():
    path = os.path.join(ROOT, "results", "verified", "E006_x86_64.json")
    runs = []
    if os.path.exists(path):
        runs = json.load(open(path, encoding="utf-8"))["runs"]
        tag = "registered run, seeds 41-80"
    else:
        for f in sorted(glob.glob(os.path.join(ROOT, "results", "exploratory", "E006_pilot_seeds*.jsonl"))):
            runs += [json.loads(ln) for ln in open(f, encoding="utf-8")]
        tag = "exploratory pilot, seeds 21-40"
    ok = np.array([r["acc160"] >= 0.99 for r in runs])
    score = np.array([r["score"] if "score" in r else r["min_eig"] for r in runs])
    rng = np.random.default_rng(0)
    fig, ax = plt.subplots(figsize=(7.6, 3.6))
    jitter = rng.uniform(-0.12, 0.12, len(runs))
    ax.scatter(score[ok] + jitter[ok], np.ones(ok.sum()) + rng.uniform(-0.08, 0.08, ok.sum()), s=46, color=S1,
               edgecolor=SURFACE, linewidth=1.5, label="succeeded at L = 160")
    ax.scatter(score[~ok] + jitter[~ok], np.zeros((~ok).sum()) + rng.uniform(-0.08, 0.08, (~ok).sum()), s=46,
               color=S2, edgecolor=SURFACE, linewidth=1.5, marker="s", label="failed")
    ax.axvline(4.5, color=MUTED, ls="--", lw=1)
    ax.text(4.55, 0.5, "accept ≥ 5", color=MUTED, fontsize=8)
    ax.set_yticks([0, 1], ["failed", "succeeded"])
    ax.set_xticks(range(0, 9))
    ax.set_xlim(-0.3, 8.5)
    ax.set_ylim(-0.4, 1.4)
    ax.set_xlabel("relator score of the trained operators (eigenvalues near 1, of 8), measured before any test")
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    title(ax, "E006: a registered rule-count check predicted which S5 runs would extrapolate", tag + "; the check uses the known S5 relations and is read before any test")
    save(fig, "E006_restart_diagnostic.png")


def e006_policy():
    path = os.path.join(ROOT, "results", "verified", "E006_x86_64.json")
    if not os.path.exists(path):
        return
    d = json.load(open(path, encoding="utf-8"))
    policy = sum(j["success"] for j in d["jobs"])
    blind = sum(d["blind_first_seed"])
    n = len(d["jobs"])
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ax.barh(["restart until the check accepts", "take the first run, no check"], [policy, blind], color=[S1, S2],
            height=0.5)
    for i, v in enumerate([policy, blind]):
        ax.text(v + 0.15, i, f"{v} of {n}", va="center", color=INK2, fontsize=9)
    ax.set_xlim(0, n + 1.5)
    ax.set_xlabel(f"groups of 4 seeds that ended with a working model (of {n})")
    ax.grid(axis="y", visible=False)
    trainings = np.mean([j["trainings"] for j in d["jobs"]])
    title(ax, "E006: restarting on the registered check makes training dependable",
          f"Same 40 fresh seeds, grouped in 10 fours. Mean trainings per group with the check: {trainings:.2f}.")
    save(fig, "E006_restart_policy.png")


def e007():
    path = os.path.join(ROOT, "results", "verified", "E007_x86_64.json")
    if not os.path.exists(path):
        return
    runs = json.load(open(path, encoding="utf-8"))["runs"]
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    for arm, color, marker, label in (("HELDOUT", S1, "o", "one operator per letter"),
                                       ("PAIR", S2, "s", "one operator per seen transition (null)")):
        rs = [r for r in runs if r["arm"] == arm]
        ax.scatter([r["clean160"] for r in rs], [r["held160"] for r in rs], s=46, color=color, marker=marker,
                   edgecolor=SURFACE, linewidth=1.5, label=label, alpha=0.9)
    ax.plot([0, 1], [0, 1], color=MUTED, lw=1, ls="--")
    ax.text(0.62, 0.66, "same accuracy on both", color=MUTED, fontsize=8, rotation=28)
    ax.set_xlim(-0.03, 1.05)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel("accuracy at L = 160 on words WITHOUT the held-out transitions")
    ax.set_ylabel("accuracy WITH them")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    title(ax, "E007: transitions never seen in training",
          "40 registered seeds per arm. Top right: learned what it saw and composed the rest. "
          "Bottom right: learned what it saw, nothing else. A transition memoriser cannot compose.")
    for arm, y, dy in (("HELDOUT", 1.0, -0.09), ("PAIR", 0.0, 0.07)):
        n = sum(1 for r in runs if r["arm"] == arm and r["clean160"] >= 0.99)
        ax.text(0.985, y + dy, f"{n} runs here", ha="right", color=INK2, fontsize=8)
    save(fig, "E007_heldout_composition.png")


def banner():
    fig = plt.figure(figsize=(12, 3.0), facecolor="#0e1116")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor("#0e1116")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 3)
    ax.axis("off")
    # a closed loop of noncommuting steps on the right: the path, and the small holonomy it leaves behind
    rng = np.random.default_rng(7)
    steps = rng.permutation(np.repeat(np.arange(4), 9))
    moves = {0: (1, 0), 1: (-1, 0), 2: (0, 1), 3: (0, -1)}
    pts = [(0, 0)]
    for s in steps:
        dx, dy = moves[int(s)]
        pts.append((pts[-1][0] + dx, pts[-1][1] + dy))
    pts = np.array(pts, dtype=float)
    pts = (pts - pts.min(0)) / max(1, (pts.max(0) - pts.min(0)).max())
    pts = pts * 2.2 + np.array([8.9, 0.4])
    for i in range(len(pts) - 1):
        a = i / (len(pts) - 1)
        ax.plot(pts[i:i + 2, 0], pts[i:i + 2, 1], color=(0.16 + 0.3 * a, 0.47 + 0.2 * a, 0.84), lw=2.2,
                solid_capstyle="round", alpha=0.9)
    ax.scatter(*pts[0], s=60, color="#eb6834", zorder=3)
    for k, r in enumerate((0.55, 0.85, 1.15)):
        t = np.linspace(0, 2 * np.pi, 200)
        ax.plot(10.0 + r * np.cos(t), 1.5 + r * np.sin(t) * 0.9, color="#2a78d6", lw=0.6, alpha=0.18 + 0.05 * k)
    ax.text(0.6, 1.72, "veritas-holo", color="#ffffff", fontsize=38, fontweight="bold", va="center")
    ax.text(0.62, 1.02, "a falsifiable geometric state substrate — measured before it is believed", color="#c3c2b7",
            fontsize=13, va="center")
    ax.text(0.62, 0.52, "E001–E008  ·  registered predictions  ·  null controls  ·  failures kept  ·  x86_64 + Snapdragon",
            color="#898781", fontsize=10, va="center")
    fig.savefig(os.path.join(OUT, "banner.png"), dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    banner()
    e002()
    e004()
    e005()
    e006()
    e006_policy()
    e007()
    print("wrote", sorted(os.listdir(OUT)))
