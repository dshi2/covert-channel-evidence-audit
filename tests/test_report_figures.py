import importlib.util
import json
from pathlib import Path

import pandas as pd

SPEC = importlib.util.spec_from_file_location(
    "report_figures", Path(__file__).resolve().parents[1] / "scripts/report_figures.py")
figures = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(figures)


def test_empty_input_is_recorded_not_plotted_as_zero(tmp_path):
    (tmp_path / "judgments.csv").write_text("\n")
    out = tmp_path / "out"
    figures.run("evidence", tmp_path, out)
    assert not list(out.glob("*.png"))
    assert json.loads((out / "evidence_figure_manifest.json").read_text())["rows"] == 0


def test_failed_cases_remain_in_planned_denominator(tmp_path, monkeypatch):
    common = {"run": "test", "setup": "test", "model": "synthetic", "scheme": "affine",
              "question": "dependent", "view": "decoder", "block": 1,
              **{name + "_correct": False for name in
                 ("evidence_level_only", "parallel_rise", "always_abstain", "always_accuse")}}
    table = pd.DataFrame([
        common | {"expected": "insufficient_evidence", "predicted": "supported", "correct": True, "answered": True},
        common | {"expected": "insufficient_evidence", "predicted": None, "correct": False, "answered": False},
    ])
    plotted = []

    def capture(fig, _out, name):
        if name.startswith("baselines"):
            plotted.extend(fig.axes[0].collections[0].get_offsets()[:, 1])
        figures.plt.close(fig)

    monkeypatch.setattr(figures, "save", capture)
    figures.evidence_figures(table, tmp_path, "SYNTHETIC")
    assert plotted == [.5]
