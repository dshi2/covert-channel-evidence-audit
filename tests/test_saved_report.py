import json

import pandas as pd
import pytest

from scripts.run_saved_report import hashes, run_report


def test_saved_report_end_to_end(tmp_path):
    from sprint.covert import cases

    source = tmp_path / "evidence"
    source.mkdir()
    planned = cases([101, 102], "affine")
    (source / "manifest.json").write_text(json.dumps({"model": {"model": "scripted"}, "cases": planned}))
    # One unanswered case must remain in the planned denominator.
    for case in planned[1:]:
        (source / f"case_{case['id']}.jsonl").write_text(json.dumps(
            {"event": "complete", "result": {"reply": case["expected"]}}) + "\n")
    before = hashes([source])
    out = tmp_path / "report"
    run_report([source], out, label="SCRIPTED TEST DATA")
    manifest = json.loads((out / "report_manifest.json").read_text())
    assert manifest["status"] == "complete" and manifest["inputs"] == before == hashes([source])
    assert set(manifest["environment"]["packages"]) == {"numpy", "pandas", "scipy", "matplotlib"}
    assert list((out / "figures").rglob("*.png"))
    assert list((out / "tables").glob("*.csv"))
    table = pd.read_csv(out / "tables" / "judgments.csv")
    assert len(table) == 80 and table.answered.sum() == 78
    assert list((out / "figures" / "metrics").glob("*.pdf"))
    with pytest.raises(FileExistsError):
        run_report([source], out)


def test_report_rejects_overlapping_input_output(tmp_path):
    with pytest.raises(ValueError, match="separate"):
        run_report([tmp_path], tmp_path / "output")
