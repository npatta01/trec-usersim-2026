#!/usr/bin/env python3
"""Render public documentation diagrams. Requires matplotlib, no network or keys.

Run from any directory: python scripts/render_doc_diagrams.py
PNG files render directly on GitHub; SVG files retain editable text.
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'images'
C = {
    'ink': '#172b46', 'muted': '#52647c', 'line': '#8192aa',
    'blue': '#eaf1ff', 'blue_edge': '#3e67c9',
    'teal': '#e5f5ef', 'teal_edge': '#268269',
    'amber': '#fff4df', 'amber_edge': '#b97a20',
    'red': '#fdeeed', 'red_edge': '#b85a55',
    'neutral': '#f3f5f9', 'neutral_edge': '#a1aec2',
}
plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none',
                     'svg.hashsalt': 'trec-usersim-docs-v1'})


def canvas(height, title, subtitle):
    fig, ax = plt.subplots(figsize=(6.4, height / 100), dpi=100)
    fig.patch.set_facecolor('white')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set_xlim(0, 640)
    ax.set_ylim(height, 0)
    ax.axis('off')
    ax.text(40, 45, title, fontsize=23, fontweight='bold', color=C['ink'], va='top')
    ax.text(40, 96, subtitle, fontsize=15, color=C['muted'], va='top', linespacing=1.35)
    return fig, ax


def box(ax, y, title, body, *, height=110, tone='blue', x=40, width=560):
    ax.add_patch(FancyBboxPatch((x, y), width, height,
        boxstyle='round,pad=0,rounding_size=14', linewidth=1.4,
        edgecolor=C[tone+'_edge'], facecolor=C[tone]))
    title_text = ax.text(x+22, y+20, title, fontsize=17, fontweight='bold', color=C['ink'], va='top')
    title_text._doc_right = x + width - 18
    if body:
        body_text = ax.text(x+22, y+52, body, fontsize=15, color=C['ink'], va='top', linespacing=1.3)
        body_text._doc_right = x + width - 18


def arrow(ax, start, end, *, color=None, points=None, dashed=False):
    color = color or C['line']
    if points:
        xs, ys = zip(start, *points, end)
        ax.plot(xs, ys, color=color, linewidth=1.7, linestyle='--' if dashed else '-')
        start = points[-1]
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=13,
        linewidth=1.7, color=color, shrinkA=0, shrinkB=0,
        linestyle='--' if dashed else '-'))


def note(ax, y, text):
    ax.text(40, y, text, fontsize=14, color=C['muted'], va='top', linespacing=1.35)


def save(fig, name):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for ax in fig.axes:
        for text in ax.texts:
            bounds = text.get_window_extent(renderer)
            right = getattr(text, '_doc_right', 620)
            if bounds.x1 > right or bounds.y0 < 12 or bounds.y1 > fig.bbox.height:
                raise ValueError(f'Clipped diagram text: {text.get_text()}')
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / (name+'.png'), dpi=200, metadata={'Software':'TREC UserSim documentation'})
    fig.savefig(OUT / (name+'.svg'), metadata={'Date': None, 'Creator':'TREC UserSim documentation'})
    svg = OUT / (name+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)


def tasks():
    fig, ax = canvas(1100, 'Task 1 vs Task 2',
        'We write the researcher. The organizer supplies\nthe dataset-search assistant.')
    ax.text(40, 184, 'TASK 1  /  Predict one message', fontsize=17,
            fontweight='bold', color=C['blue_edge'], va='top')
    box(ax, 230, 'Organizer supplies a prefix',
        'Persona, goal and conversation so far.\nIt can be an opening or any later turn.')
    arrow(ax, (320, 340), (320, 375))
    box(ax, 375, 'Return one researcher message',
        'One prediction, then a new supplied input.\nOur prediction is not added to the next prefix.', height=120)
    ax.text(40, 560, 'TASK 2  /  Play the conversation', fontsize=17,
            fontweight='bold', color=C['teal_edge'], va='top')
    box(ax, 605, 'We generate a researcher turn',
        'Persona, goal and full conversation text.\nOutput: message plus a stop decision.', tone='teal', width=510)
    arrow(ax, (295, 715), (295, 750))
    box(ax, 750, 'Receive the organizer response',
        'Assistant reply: extend our history.\nNew scenario: reset the conversation.', tone='teal', width=510)
    arrow(ax, (550, 805), (550, 660), color=C['teal_edge'],
          points=[(590,805), (590,660)], dashed=True)
    arrow(ax, (295, 860), (295, 910))
    box(ax, 910, 'A new conversation resets context',
        'A stop ends a conversation. Recognized\norganizer completion ends the whole run.', tone='neutral', height=110)
    note(ax, 1040, 'Full history means utterance text.\nRaw metadata is retained privately.')
    save(fig, 'task-comparison')


def pipeline():
    fig, ax = canvas(1260, 'Inside one researcher turn',
        'Two model calls. Exact requests and results\nare retained privately.')
    stages = [
        (175, '1  Build the researcher context',
         'Persona + goal fields + available utterance text.\nNo future human reply or reference answer.', 'neutral'),
        (330, '2  Map the conversation speakers',
         'Researcher history → assistant role.\nSearch-assistant history → user role.', 'blue'),
        (485, '3  Draft with Luna',
         'Task 1: next-message text.\nTask 2: text + boolean stop decision.', 'blue'),
        (640, '4  Make one editor call with Luna',
         'Same context, draft and recent researcher voice.\nTask 1 official: fidelity. Task 2: style.', 'teal'),
        (795, '5  Validate and save',
         'Reject invalid output; checkpoint before sending.\nTask 2 keeps the draft’s stop boolean.', 'neutral'),
        (950, '6  Submit through the organizer API',
         'Validate reply, reset or completion.\nPreserve evidence if the outcome is uncertain.', 'neutral'),
    ]
    for i, (y, title, body, tone) in enumerate(stages):
        box(ax, y, title, body, height=115, tone=tone)
        if i: arrow(ax, (320, y-40), (320, y-4))
    note(ax, 1110, 'Full history is resent explicitly for each request.\nNo automatic compaction or repeated judge/retry loop.\n\nEditing preserves the stop flag in code; preserving\nmeaning and natural voice still requires evaluation.')
    save(fig, 'researcher-pipeline')


def recovery():
    fig, ax = canvas(1380, 'Recovery without duplicates',
        'The server may save our message before an error.\nDo not automatically resend that message.')
    box(ax, 180, 'Save the request before sending',
        'Keep the response or transport-error record.\nKeep a pending marker if outcome is uncertain.', tone='neutral', height=115)
    arrow(ax, (320, 295), (320, 335))
    box(ax, 340, 'Classify the response',
        'Valid reply or new scenario: advance normally.\nRecognized completion: finish the run.', tone='blue', height=115)
    arrow(ax, (320, 455), (320, 500))
    box(ax, 505, 'Read and verify the server session',
        'Check the ID, scenario and exact history.\nAn original timeout waits for a delayed reply.', tone='amber', height=115)
    ax.text(40, 665, 'Choose an action only from verified evidence:', fontsize=15,
            fontweight='bold', color=C['ink'], va='top')
    box(ax, 710, 'Matching delayed reply',
        'Reconcile the saved exchange and continue.\nNo repost and no administrative close.', tone='teal', height=115)
    box(ax, 865, 'Verified unanswered turn',
        'After grace, recheck the unanswered turn.\nClose once within policy; verify advancement.', tone='amber', height=115)
    box(ax, 1020, 'Uncertain or mismatched evidence',
        'Halt and preserve the original records.\nAn uncertain closing request also halts.', tone='red', height=115)
    ax.plot([40, 20, 20], [562, 562, 1077], color=C['line'], linewidth=1.7)
    for y, tone in ((767,'teal'), (922,'amber'), (1077,'red')):
        arrow(ax, (20,y), (40,y), color=C[tone+'_edge'])
    note(ax, 1190, 'Administrative closes are recorded separately from\nnatural researcher stops. They do not prove satisfaction.\n\nThe completed run kept a 30-minute timeout grace.\nSpend, turn and outage bounds remain active.')
    save(fig, 'recovery-flow')


if __name__ == '__main__':
    tasks()
    pipeline()
    recovery()
    print('Rendered 3 PNG and 3 SVG documentation diagrams in', OUT)
