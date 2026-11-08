"""Render public aggregate organizer comparisons; never reads participant text."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
ROOT = Path(__file__).resolve().parent
scores = json.loads((ROOT.parent / 'preliminary-results-2026-11-07.json').read_text())
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12, 'pdf.fonttype': 42})
fig, axes = plt.subplots(1, 2, figsize=(10, 3.45), gridspec_kw={'width_ratios': [1.5, 1]})
colors = ['#E3E6E8', '#315B70']
for ax in axes:
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.spines['bottom'].set_color('#BBC3C7')
    ax.tick_params(axis='y', length=0)
    ax.grid(axis='x', color='#E8ECEE', zorder=0)
    ax.set_axisbelow(True)
for task, y in [(1, 1), (2, 0)]:
    d = scores['tasks'][str(task)]
    for value, yy, color in [(d['human_avg_user_chars'], y+.16, colors[0]), (d['avg_user_chars'], y-.16, colors[1])]:
        axes[0].barh(yy, value, height=.26, color=color, edgecolor="#26333D", linewidth=.6, hatch="///" if color == colors[0] else None, zorder=3)
        axes[0].text(value+9, yy, str(value), va='center', fontsize=12)
axes[0].set(yticks=[1, 0], yticklabels=['Task 1', 'Task 2'], xlim=(0, 650), xticks=[0, 200, 400, 600], ylim=(-.5, 1.5), xlabel='Mean characters per user utterance')
axes[0].set_title('A  Longer replies in both tasks', loc='left', fontsize=13, fontweight='bold', pad=14)
d = scores['tasks']['2']
for value, y, color in [(d['human_avg_user_turns'], .16, colors[0]), (d['avg_user_turns'], -.16, colors[1])]:
    axes[1].barh(y, value, height=.26, color=color, edgecolor="#26333D", linewidth=.6, hatch="///" if color == colors[0] else None, zorder=3)
    axes[1].text(value+.09, y, f'{value:.1f}', va='center', fontsize=12)
axes[1].set(yticks=[0], yticklabels=['Task 2'], xlim=(0, 5.5), xticks=[0, 1, 2, 3, 4, 5], ylim=(-.5, .5), xlabel='Mean user turns per conversation')
axes[1].set_title('B  More user turns', loc='left', fontsize=13, fontweight='bold', pad=14)
fig.legend(handles=[Patch(facecolor=colors[0], edgecolor='#26333D', hatch='///', label='Human conversations (organizer mean)'), Patch(color=colors[1], label='Our simulator')], loc='upper center', bbox_to_anchor=(.5, 1.02), ncol=2, frameon=False)
fig.subplots_adjust(left=.085, right=.96, bottom=.20, top=.77, wspace=.50)
fig.savefig(ROOT / 'results-comparison.pdf', bbox_inches='tight')
fig.savefig(ROOT / 'results-comparison.png', dpi=180, bbox_inches='tight')
