# -*- coding: utf-8 -*-
"""
Figure for Section 3.3: dataset availability for model validation.
(a) Studies in each dataset availability category (n = 564).
(b) Quantities reported by the 145 'Other parameters' studies
    (a study can be counted in more than one group).
Run in Spyder (F5). Output: figure_dataset_availability.png next to this script.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

_avail = {f.name for f in fm.fontManager.ttflist}
plt.rcParams.update({
    'font.family': 'Arial' if 'Arial' in _avail else 'DejaVu Sans',
    'axes.spines.top': False, 'axes.spines.right': False,
})
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()
OUTPUT = os.path.join(SCRIPT_DIR, 'figure_dataset_availability.png')

# ---------------------------------------------------------------- data
TOTAL = 564
CATS = [  # label, count, colour (same palette as the Figure 4 summary)
    ("Yes", 134, '#1D9E75'),
    ("Other parameters", 145, '#C08000'),
    ("Secondary", 108, '#534AB7'),
    ("NA", 177, '#888780'),
]
HIGH_INFO = 30  # 'Yes' studies that also report v, w, Reynolds stress, TKE or Cd
assert sum(c[1] for c in CATS) == TOTAL, "category counts must sum to 564"

OTHER_N = 145
OTHER = [  # recount of the '2 Primary but not v' tab
    ("Lateral or depth-averaged\nstreamwise velocity", 36),
    ("Mean velocity at a few points", 29),
    ("Bulk hydraulics (depth,\ndischarge, Re, Fr)", 14),
    ("Spatially averaged\nvertical profile", 13),
    ("Flow resistance\n(Manning, friction factor)", 12),
    ("Sediment transport", 12),
    ("TKE or turbulence intensity", 12),
    ("Reynolds stress", 11),
    ("Drag coefficient", 10),
    ("Transverse velocity (v)", 7),
    ("Longitudinal dispersion", 6),
    ("Secondary flow", 4),
    ("Bed shear stress", 2),
]
INK, MUTED, GRID = '#2C2C2A', '#5F5E5A', '#E4E2DC'

# ---------------------------------------------------------------- figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18 / 2.54, 10 / 2.54), dpi=300,
                               gridspec_kw={'width_ratios': [1, 1.25], 'wspace': 1.0})
fig.patch.set_facecolor('white')

# (a) categories
ys = list(range(len(CATS)))[::-1]
for y, (lab, n, col) in zip(ys, CATS):
    if lab == "Yes":
        ax1.barh(y, n - HIGH_INFO, height=0.62, color=col, linewidth=0, zorder=3)
        ax1.barh(y, HIGH_INFO, left=n - HIGH_INFO, height=0.62, color='#0F6E56',
                 edgecolor='white', linewidth=1.0, zorder=3)
    else:
        ax1.barh(y, n, height=0.62, color=col, linewidth=0, zorder=3)
    lbl = f"{n} ({n / TOTAL * 100:.1f}%)"
    if lab == "Yes":
        lbl += f"\nincl. {HIGH_INFO} high-information"
        ax1.text(n - HIGH_INFO / 2, y, str(HIGH_INFO), va='center', ha='center',
                 fontsize=6.5, color='white', fontweight='bold', zorder=4)
    ax1.text(n + 4, y, lbl, va='center', ha='left', fontsize=7, color=INK, linespacing=1.15)
ax1.set_yticks(ys)
ax1.set_yticklabels([c[0] for c in CATS], fontsize=7.5, color=INK)
ax1.set_xlim(0, 300)
ax1.set_xticks([0, 50, 100, 150, 200])
ax1.set_ylim(-0.55, len(CATS) - 0.45)
ax1.set_xlabel("Number of studies", fontsize=7.5, color=MUTED)
ax1.tick_params(axis='x', labelsize=6.5, colors=MUTED)
ax1.tick_params(axis='y', length=0)
ax1.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
for s in ('left', 'bottom'):
    ax1.spines[s].set_color(GRID)
ax1.set_title(f"(a) Dataset availability (n = {TOTAL})", loc='left', fontsize=8,
              fontweight='bold', color=INK, pad=6)

# (b) Other parameters
ys2 = list(range(len(OTHER)))[::-1]
for y, (lab, n) in zip(ys2, OTHER):
    ax2.barh(y, n, height=0.62, color='#C08000', linewidth=0, zorder=3)
    ax2.text(n + 0.8, y, str(n), va='center', ha='left', fontsize=6.5, color=INK)
ax2.set_yticks(ys2)
ax2.set_yticklabels([o[0] for o in OTHER], fontsize=6.3, color=INK, linespacing=1.0)
ax2.set_xlim(0, 42)
ax2.set_xlabel("Number of studies", fontsize=7.5, color=MUTED)
ax2.tick_params(axis='x', labelsize=6.5, colors=MUTED)
ax2.tick_params(axis='y', length=0)
ax2.xaxis.grid(True, color=GRID, linewidth=0.6, zorder=0)
for s in ('left', 'bottom'):
    ax2.spines[s].set_color(GRID)
ax2.set_title(f"(b) Quantities in 'Other parameters' (n = {OTHER_N})", loc='left',
              fontsize=8, fontweight='bold', color=INK, pad=6)

plt.savefig(OUTPUT, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Saved -> {OUTPUT}")
plt.show()
