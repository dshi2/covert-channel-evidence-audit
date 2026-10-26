"""Report design figures; no live data or collection code is modified."""
import argparse
import os
from pathlib import Path

os.environ.setdefault('MPLCONFIGDIR', '/tmp/collusion-report-mpl')
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path('reports/designs')
INK = '#162b3b'
BLUE = '#235b83'
TEAL = '#16756f'
PALE = '#edf4f9'
GREEN = '#edf7f5'
GRAY = '#536471'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'svg.fonttype': 'none', 'pdf.fonttype': 42})


def canvas(height, bottom=0):
    fig, ax = plt.subplots(figsize=(10, height - bottom))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.set(xlim=(0, 10), ylim=(bottom, height))
    ax.axis('off')
    return fig, ax


def label(ax, x, y, text, size=12, color=INK, weight='normal', ha='center'):
    return ax.text(x, y, text, ha=ha, va='center', fontsize=size,
                   color=color, weight=weight, linespacing=1.35)


def box(ax, x, y, w, h, text, color=BLUE, fill=PALE, size=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.025,rounding_size=0.08',
                               facecolor=fill, edgecolor=color, linewidth=1.25))
    label(ax, x+w/2, y+h/2, text, size)


def arrow(ax, a, b, color=GRAY):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle='-|>', mutation_scale=12,
                                 linewidth=1.3, color=color))


def save(fig, name):
    for ext in ('png', 'svg', 'pdf'):
        fig.savefig(OUT / f'{name}.{ext}', dpi=300, facecolor='white')
    plt.close(fig)


def evidence():
    fig, ax = canvas(9.4, bottom=.5)
    label(ax, 5, 9.06, 'What does the supplied evidence establish?', 19, weight='bold')
    box(ax, .35, 8.14, 9.3, .58,
        'Scripted sender + recipient: 5 mechanism types in each of 20 evaluation blocks\nUsed; ignored; ignored but matching; decoding failed; coincidence', size=12)
    label(ax, 5, 7.73, 'Each case is shown in four views, in separate auditor calls', 12, GRAY)
    for x in [1.45, 3.82, 6.18, 8.55]:
        arrow(ax, (x, 7.52), (x, 7.19))
    specs=[(.35,'PUBLIC','Price and\naction trace'),
           (2.72,'DECODER','Public trace +\ndecoding record'),
           (5.08,'PARTIAL EXECUTION','Decoder view +\npartial policy trials'),
           (7.45,'COMPLETE','Decoder view +\nall policy trials')]
    for x,title,body in specs:
        box(ax, x, 6.05, 2.2, 1.1, '', size=11)
        label(ax,x+1.1,6.87,title,10.2,BLUE,'bold')
        label(ax,x+1.1,6.45,body,12)
        arrow(ax,(x+1.1,6.05),(x+1.1,5.68))
    box(ax, .35, 4.61, 9.3, 1.02,
        'LLM auditor returns two separate judgments\n1  Was the target recovered?     2  Does action depend on decoded input?\nFor each: supported / contradicted / insufficient evidence', size=12)
    arrow(ax,(5,4.61),(5,4.39))
    box(ax, .35, 3.01, 9.3, 1.32,
        'MATCHED HARD NEGATIVE: SAME DECODER EVIDENCE\n'
        'Both recover target T and produce action T. Dependence is still insufficiently evidenced.\n'
        'Dependent policy: another input changes the action. Ignored-but-matching: all inputs yield T.\n'
        'Complete trials distinguish the two policies; the observed match alone cannot.',
        TEAL, GREEN, 11.2)
    arrow(ax,(5,3.01),(5,2.69))
    box(ax,.35,1.82,9.3,.82,
        'Code-based reference: grade only what the visible records establish\nMatched ambiguous cases prevent hidden truth from rewarding an unjustified guess\nScripted positive/negative controls + baselines on the same evaluation cases', TEAL,GREEN,11.5)
    arrow(ax,(5,1.82),(5,1.52))
    box(ax,.35,.69,9.3,.77,
        'Report coverage, resolved accuracy and unsupported conclusions\nRetain missing replies; compare evidence views within matched blocks\n400 planned cases/model • 2 judgments/case • uncertainty clustered by 20 blocks',size=11.5)
    save(fig,'report2_evidence_audit_design')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('reports/designs'))
    args = parser.parse_args()
    OUT = args.out
    OUT.mkdir(parents=True, exist_ok=True)
    evidence()
    print(f'Saved PNG, SVG and PDF diagram to {OUT}')
