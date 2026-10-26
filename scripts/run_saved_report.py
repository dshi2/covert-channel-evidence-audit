"""Rebuild tables and figures from saved journals, without API calls."""

import argparse
import hashlib
import json
import platform
import subprocess
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path

import matplotlib

matplotlib.use("Agg")


def hashes(runs):
    return {str(path.resolve()): hashlib.sha256(path.read_bytes()).hexdigest()
            for run in runs for path in sorted(run.iterdir())
            if path.is_file() and (path.suffix == ".jsonl" or path.name == "manifest.json")}


def environment(root):
    """Commit, uncommitted-change flag and library versions; None where git is unavailable."""
    def git(*args):
        try:
            return subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                                  text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    status = git("status", "--porcelain")
    return {"git_commit": git("rev-parse", "HEAD"),
            "git_uncommitted_changes": None if status is None else bool(status),
            "python": platform.python_version(),
            "packages": {name: metadata.version(name)
                         for name in ("numpy", "pandas", "scipy", "matplotlib")}}


def run_report(runs, out, label="Descriptive snapshot"):
    from scripts import report_figures
    from scripts.plot_metrics import plot_metrics
    from sprint import covert_analyze

    runs = [Path(p).resolve() for p in runs]
    out = Path(out).resolve()
    if len({p.name for p in runs}) != len(runs):
        raise ValueError("Run folder names must be unique; analysis identifies runs by folder name")
    for directory in runs:
        if not directory.is_dir():
            raise ValueError(f"Missing run folder: {directory}")
        if out == directory or out.is_relative_to(directory) or directory.is_relative_to(out):
            raise ValueError("Report output must be separate from input run folders")
        if not (directory / "manifest.json").is_file():
            raise ValueError(f"Run manifest missing: {directory}")
    out.mkdir(parents=True, exist_ok=False)
    before = hashes(runs)
    manifest = {"experiment": "evidence", "label": label,
                "created_utc": datetime.now(UTC).isoformat(),
                "inputs": before, "status": "started"}
    # Hash the implementation too, including staged edits absent from a git commit.
    root = Path(covert_analyze.__file__).resolve().parents[1]
    manifest["analysis_source"] = {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for subdir in ("sprint", "scripts") for p in sorted((root / subdir).glob("*.py"))}
    manifest["runner_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest["environment"] = environment(root)
    manifest_path = out / "report_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    tables, figures = out / "tables", out / "figures"
    try:
        covert_analyze.export_tables(runs, tables)
        report_figures.run("evidence", tables, figures, label)
        plot_metrics(tables / "summary.csv", figures / "metrics", label)
        if hashes(runs) != before:
            raise RuntimeError("Input files changed during analysis. Use a stable snapshot and rerun to a new output folder")
        manifest["status"] = "complete"
        manifest["outputs"] = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(out.rglob("*")) if p.is_file() and p != manifest_path}
    except Exception as exc:
        manifest.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path, help="Model run folders, not the parent directory")
    parser.add_argument("--out", required=True, type=Path, help="New report folder; never overwrites")
    parser.add_argument("--label", default="Descriptive snapshot")
    args = parser.parse_args()
    print(run_report(args.runs, args.out, args.label))


if __name__ == "__main__":
    main()
