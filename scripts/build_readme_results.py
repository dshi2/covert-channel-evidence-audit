"""Rebuild the README table and figure from bundled, hashed analysis exports."""
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
NAMES = {'deepseek/deepseek-v4.1-flash-1017': 'DeepSeek',
         'qwen/qwen3.8-flash': 'Qwen', 'openai/gpt-oss-120b': 'GPT-OSS'}


def build():
    source = ROOT / 'results/exports'
    manifest = json.loads((ROOT / 'results/export_manifest.json').read_text())
    for name, record in manifest['files'].items():
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != record['bundled_sha256']:
            raise ValueError(f'Export hash mismatch: {name}')
    frame = pd.read_csv(source / 'metrics.csv')
    rows = ['| Model | Complete evidence: correct dependence judgments | Partial execution: correct dependence judgments | Unsupported positives in ambiguous partial cases |',
            '|---|---:|---:|---:|']
    for model, name in NAMES.items():
        group = frame[(frame.model == model) & (frame.question == 'dependent')]
        values = [group[(group.view == v) & (group.metric == m)].iloc[0]
                  for v, m in [('complete', 'correct_per_planned_judgment'),
                               ('partial_execution', 'correct_per_planned_judgment'),
                               ('partial_execution', 'unsupported_positive')]]
        cells = [f'{int(r.numerator)}/{int(r.denominator)}' for r in values]
        rows.append('| ' + ' | '.join([name] + cells) + ' |')
    text = '\n'.join(rows)
    (ROOT / 'results/README_TABLE.md').write_text(text + '\n')
    plt.rcParams.update({'font.size': 12, 'axes.titlesize': 13, 'axes.labelsize': 12,
                         'xtick.labelsize': 11, 'ytick.labelsize': 11})
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), sharey=True)
    for ax, metric, title in zip(axes, ['unsupported_positive', 'unsupported_negative'],
                                ['Unsupported positive judgments', 'Unsupported negative judgments']):
        for model_i, (model, name) in enumerate(NAMES.items()):
            for view_i, view in enumerate(('decoder', 'partial_execution')):
                r = frame[(frame.model == model) & (frame.question == 'dependent') &
                          (frame.view == view) & (frame.metric == metric)].iloc[0]
                x = view_i + (model_i - 1)*.16
                ax.errorbar(x, 100*r.mean_block_rate,
                            yerr=[[100*(r.mean_block_rate-r.ci_low)], [100*(r.ci_high-r.mean_block_rate)]],
                            fmt='o', color=['#245c80', '#bb6a25', '#5a7b42'][model_i],
                            capsize=3, label=name if view_i == 0 else None)
        ax.set(title=title, xticks=[0, 1], xticklabels=['Decoder records', 'Partial execution'],
               xlim=(-.5, 1.5), ylim=(-2, 45))
        ax.spines[['top', 'right']].set_visible(False)
    axes[0].set_ylabel('Mean within-block error rate (%)')
    axes[1].legend(frameon=False, fontsize=11)
    fig.tight_layout(pad=2)
    for ext in ('png', 'svg'):
        fig.savefig(ROOT / f'figures/results_summary.{ext}', dpi=180)
    plt.close(fig)
    readme = ROOT / 'README.md'
    content = readme.read_text()
    start, end = '<!-- RESULTS:START -->', '<!-- RESULTS:END -->'
    if start in content:
        before, rest = content.split(start, 1)
        _, after = rest.split(end, 1)
        readme.write_text(before + start + '\n' + text + '\n' + end + after)


if __name__ == '__main__':
    build()
