"""Render a protein-folding background: unfolded chain (left) -> folded ubiquitin 1UBQ (right)."""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from scipy.interpolate import CubicSpline

pdb_path, out_path = sys.argv[1], sys.argv[2]

ca = np.array([[float(l[30:38]), float(l[38:46]), float(l[46:54])]
               for l in open(pdb_path) if l.startswith("ATOM") and l[12:16].strip() == "CA"])
ca -= ca.mean(0)

def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

folded = ca @ rot(0.4, 0.9, 0.2).T
folded = folded / np.abs(folded[:, :2]).max() * 3.9
folded[:, 0] += 3.6  # place on the right
folded[:, 1] += 0.1

# unfolded chain: loose wavy coil trailing to the left, ending at the N-terminus
rng = np.random.default_rng(7)
n_un = 40
t = np.linspace(0, 1, n_un)
start = folded[0]
xs = np.linspace(start[0] - 9.5, start[0], n_un)
ys = start[1] + 0.9 * np.sin(t * 7.0) * (1 - t) + 0.25 * rng.standard_normal(n_un).cumsum() * 0.15 - 1.2 * (1 - t)
zs = np.linspace(-2.5, start[2], n_un) + 0.6 * np.cos(t * 5)
unfolded = np.stack([xs, ys, zs], 1)[:-1]

chain = np.vstack([unfolded, folded])
fold_weight = np.concatenate([np.linspace(0.35, 0.85, len(unfolded)), np.ones(len(folded))])

u = np.arange(len(chain))
cs = CubicSpline(u, chain)
uu = np.linspace(0, len(chain) - 1, len(chain) * 12)
P = cs(uu)
W = np.interp(uu, u, fold_weight)

z = P[:, 2]
zn = (z - z.min()) / (z.max() - z.min())
segs = np.stack([P[:-1, :2], P[1:, :2]], 1)
order = np.argsort(zn[:-1])  # painter's algorithm: far first
segs, zs_, ws = segs[order], zn[:-1][order], W[:-1][order]

W_IN, H_IN, DPI = 19.2, 10.8, 100
fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
bg = "#0b0f0d"
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)
ax.set_xlim(-8.3, 8.3)
ax.set_ylim(-4.67, 4.67)
ax.set_aspect("equal")
ax.axis("off")

green = np.array([127, 255, 181]) / 255
cyan = np.array([46, 245, 255]) / 255
cols = (green[None] * (1 - zs_[:, None] * 0.35) + cyan[None] * zs_[:, None] * 0.35)
bright = (0.25 + 0.75 * zs_) * ws

# glow layers then core
for lw, a in [(26, 0.025), (14, 0.05), (7, 0.12)]:
    rgba = np.c_[cols, a * bright]
    ax.add_collection(LineCollection(segs, colors=rgba, linewidths=lw * (0.6 + 0.6 * zs_), capstyle="round"))
rgba = np.c_[cols * (0.45 + 0.55 * zs_[:, None]), 0.95 * bright]
ax.add_collection(LineCollection(segs, colors=rgba, linewidths=3.2 * (0.55 + 0.75 * zs_), capstyle="round"))

# CA beads on folded part
fz = (folded[:, 2] - z.min()) / (z.max() - z.min())
ax.scatter(folded[:, 0], folded[:, 1], s=10 + 30 * fz, c=[green], alpha=0.25 + 0.6 * fz, zorder=5, linewidths=0)

fig.savefig(out_path, dpi=DPI, facecolor=bg)
print("saved", out_path)
