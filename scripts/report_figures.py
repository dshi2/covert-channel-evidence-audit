"""Offline figures from existing analysis CSVs; never reads keys or calls a model."""

import argparse
import hashlib
import json
from itertools import pairwise
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def save(fig, out, name):
    fig.tight_layout()
    for suffix in ("png", "svg"):
        fig.savefig(out / f"{name}.{suffix}", dpi=180, bbox_inches="tight")
    plt.close(fig)


def groups(table, extra=()):
    # Never pool models, run directories, configurations, stages or encoding schemes.
    keys = ["run", "setup", "model", *extra]
    for key, frame in table.groupby(keys, dropna=False, sort=True):
        identity = dict(zip(keys, key))
        tag = hashlib.sha256(json.dumps(identity, sort_keys=True, default=str).encode()).hexdigest()[:12]
        yield tag, identity, frame


def dots(ax, frame, category, value):
    labels = list(frame[category].drop_duplicates())
    for i, label in enumerate(labels):
        values = frame.loc[frame[category] == label, value].dropna().to_numpy(float)
        offset = np.linspace(-.13, .13, len(values)) if len(values) > 1 else np.zeros(len(values))
        ax.scatter(i + offset, values, s=25, alpha=.75)
        if len(values):
            ax.plot([i - .2, i + .2], [values.mean()] * 2, color="black", lw=2)
    counts = frame.groupby(category)[value].count()
    ax.set_xticks(range(len(labels)), [f"{s.replace('_', ' ')}\nn={counts[s]}" for s in labels], rotation=25, ha="right")
    ax.axhline(0, color="grey", lw=.7)
    ax.spines[["top", "right"]].set_visible(False)


def evidence_figures(table, out, label):
    baselines = ("evidence_level_only", "parallel_rise", "always_abstain", "always_accuse")
    for tag, identity, frame in groups(table, ("scheme", "question")):
        blocks = frame.groupby(["view", "block"], sort=False).correct.mean().reset_index()
        fig, ax = plt.subplots(figsize=(10, 5))
        dots(ax, blocks, "view", "correct")
        views = list(blocks.view.drop_duplicates())
        for name in baselines:
            rates = frame.groupby("view")[name + "_correct"].mean().reindex(views)
            ax.plot(range(len(views)), rates, marker="_", linestyle="--", alpha=.65, label=name)
        ax.set(ylim=(-.03, 1.03), ylabel="Correct / planned judgments")
        ax.set_title(f"{label}\n{identity['model']} — {identity['scheme']} — {identity['question']}")
        ax.legend(fontsize=8, loc="upper center", bbox_to_anchor=(.5, -.30), ncol=2)
        fig.text(.5, -.13, "Dots: base-case block rates; black lines: means. Failed answers count incorrect.\nBaselines see the same evidence.", ha="center", fontsize=9)
        save(fig, out, f"baselines_{tag}")
        ambiguous = frame.expected.eq("insufficient_evidence") & frame.answered
        mistakes = frame.loc[ambiguous].assign(
            overclaim=lambda x: x.predicted.isin(("supported", "contradicted")).astype(int))
        if not mistakes.empty:
            rates = mistakes.groupby(["view", "block"], sort=False).overclaim.mean().reset_index()
            fig, ax = plt.subplots(figsize=(7, 4))
            dots(ax, rates, "view", "overclaim")
            ax.set(ylim=(-.03, 1.03), ylabel="Over-claim rate on insufficient-evidence cases",
                   title=f"{label}\n{identity['model']} — {identity['scheme']} — {identity['question']}")
            fig.text(.5, -.02, "A conclusion of supported or contradicted where the supplied evidence is insufficient.\nBase-case block rates; failures remain outside the conditional denominator.", ha="center", fontsize=9)
            save(fig, out, f"overclaim_{tag}")


def diagrams(out):
    designs = {
        "evidence": ("Evidence sufficiency from synthetic execution records", [
            "Programmed sender and recipient\nFive mechanisms\nKnown execution ground truth",
            "Public / decoder / complete / partial\nMatched visible records\nIndependent auditor calls",
            "Recover target?\nAction depends on decoded input?\nSupported / contradicted / insufficient",
            "Code-scored verdicts\nRetain wrong answers and failures\nCompare evidence-only baselines",
            "Coverage + resolvable accuracy\nUnsupported claims + abstention\nUncertainty grouped by base case"],
            "This evaluates supplied evidence, not spontaneous secret signalling or general collusion detection. Independent oracle controls run first."),
    }
    for name, (title, boxes, footnote) in designs.items():
        fig, ax = plt.subplots(figsize=(11, 5.5))
        ax.set(xlim=(0, 1), ylim=(0, 1))
        ax.axis("off")
        positions = [(.2, .78), (.8, .78), (.8, .46), (.2, .46), (.5, .13)]
        for (x, y), text in zip(positions, boxes):
            ax.text(x, y, text, ha="center", va="center", fontsize=10,
                    bbox={"boxstyle": "round,pad=.65", "facecolor": "#eef4f8", "edgecolor": "#38627d"})
        for (x1, y1), (x2, y2) in pairwise(positions):
            if y1 == y2:
                direction = 1 if x2 > x1 else -1
                start, end = (x1 + direction * .23, y1), (x2 - direction * .23, y2)
            else:
                start, end = (x1, y1 - .10), (x2, y2 + .10)
            ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": "#38627d", "lw": 1.6})
        fig.suptitle(title, fontsize=15)
        fig.text(.5, -.015, footnote, ha="center", fontsize=9)
        save(fig, out, f"design_{name}")


def run(kind, source, out, label="Descriptive results"):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if kind == "diagrams":
        diagrams(out)
        return
    path = Path(source) / "judgments.csv"
    try:
        table = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        table = pd.DataFrame()
    if not table.empty:
        evidence_figures(table, out, label)
    (out / f"{kind}_figure_manifest.json").write_text(json.dumps({
        "source": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "rows": len(table), "label": label, "status": "empty input; no figures" if table.empty else "rendered",
    }, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("evidence", "diagrams"))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--label", default="Descriptive results")
    args = parser.parse_args()
    if args.kind != "diagrams" and args.source is None:
        parser.error("--source is required for saved-data figures")
    run(args.kind, args.source, args.out, args.label)
