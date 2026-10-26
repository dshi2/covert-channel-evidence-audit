# When Do Execution Records Support Recovery and Dependence Claims?

Can an LLM auditor tell whether a hidden signal was merely recoverable from a seller's actions, or whether the actions actually depended on it? Five programmed mechanisms are shown under four evidence views in 20 matched blocks (400 cases per model). This tests reasoning about supplied records, not discovery of unknown covert channels.

[Report (PDF)](paper/report.pdf) · [Tables and figures](REPORTING.md)

![Study design](figures/report2_evidence_audit_design.png)

**Figure 1.** *Design of the evidence audit. Each of 20 blocks contains five scripted sender–recipient mechanisms. Each case is shown to the auditor in four views that add evidence step by step: public prices and actions, the recipient's decoding record, some of the policy trials, and all of them. The auditor judges separately whether the target was recovered and whether the action depended on it, and is graded against what the shown records establish. The key test is a matched pair with identical decoder records: one policy uses the signal and the other ignores it but happens to match, so only the complete trials can tell them apart.*

## Results

<!-- RESULTS:START -->
| Model | Complete evidence: correct dependence judgments | Partial execution: correct dependence judgments | Unsupported positives in ambiguous partial cases |
|---|---:|---:|---:|
| DeepSeek | 100/100 | 98/100 | 1/36 |
| Qwen | 100/100 | 87/100 | 8/36 |
| GPT-OSS | 96/100 | 92/100 | 0/36 |
<!-- RESULTS:END -->

- With one trial output hidden, Qwen claimed dependence without support in 8/36 ambiguous cases; GPT-OSS never did, but ruled it out without support in 6/36.
- Complete records were easier but did not remove all errors.
- On the non-public views, models beat an evidence-level-only baseline on the same cases by 16 to 52 percentage points.

Counts are raw; intervals resample matched blocks, not individual judgments.

![Results](figures/results_summary.png)

**Figure 2.** *How often each model drew a dependence conclusion the evidence did not support, in ambiguous cases where the correct answer was "not enough evidence". The left panel shows unsupported claims that the action depended on the signal; the right panel shows unsupported claims that it did not. Points are mean error rates within matched blocks, with 95% intervals. With partial trials, Qwen over-claimed dependence most often (21.6%), while GPT-OSS never over-claimed but most often ruled dependence out without support (16.7%). The public view is not shown, and the complete view has no ambiguous cases.*

Metrics and intervals are in [results/exports](results/README.md). Rebuild the table and figure with `python -m scripts.build_readme_results` (no API calls).

## Install and test

Requires Python 3.12 or newer.

```bash
git clone https://github.com/dshi2/covert-channel-evidence-audit.git
cd covert-channel-evidence-audit
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -c requirements-tested.txt -e '.[dev]'
bash scripts/get_starter.sh
python -m pip install -c requirements-tested.txt ./starter/util ./starter/algorithmic-pricing-llms
python -m pytest -q
```

## Rebuild from raw runs

```bash
python -m scripts.check_covert_controls --out reports/controls
python -m scripts.run_saved_report data/recovery/deepseek41 data/recovery/qwen38 data/recovery/gptoss120 --out reports/recovery
python -m scripts.build_paper_tables reports/recovery/tables/judgments.csv --out reports/paper-tables
python -m scripts.plot_metrics reports/recovery/tables/summary.csv --out reports/primary-panels --metrics unsupported_positive resolved_accuracy
python -m scripts.build_paper_diagrams --out reports/designs
```

Each data folder holds one model's `manifest.json` and `case_*.jsonl` journals. The raw run archive is not bundled yet. Mistral's incomplete run is analysed separately. These commands make no model calls.

## Layout

```text
paper/       Report and supporting materials
notebooks/   Colab launcher used for collection (paid model calls)
sprint/      Case generation, collection and analysis on the shared engine
scripts/     Controls, report builders and figures
configs/     Model and experiment settings
results/     Bundled numerical exports with hashes
provenance/  Collection source snapshots
tests/       Tests
```

## What is new and when it was done

This project was carried out entirely within the Apart AI Collusion Research Sprint (23–26 October 2026). No code or data predates the sprint; the first commit is from 25 October 2026.

It builds on the sprint starter kit ([poseidon-research/collusion_hackathon](https://github.com/poseidon-research/collusion_hackathon), commit `d585a7b`), which packages the pricing harness of Romero, Sauer and Peist:

- **Used unchanged:** the market functions and prompt texts. They are downloaded at install time, not copied here.
- **Adapted:** `sprint/prompt.py` rebuilds the starter's prompt construction and reuses its response-format text; a test checks that the output matches the starter exactly.
- **New:** everything else, including the evidence-audit cases, grading, model client, analysis, controls and figures.

The version submitted with the report is tagged [`pre-maintenance-2026-10-26`](https://github.com/dshi2/covert-channel-evidence-audit/tree/pre-maintenance-2026-10-26), committed on 26 October at 11:19 UTC, before the 11:59 UTC deadline. Later commits only tidy documentation and code layout; they add no experiments or results.

## Source

Author: **Drishti Sharma, Independent**. Exported from the sprint source recorded in `provenance/source.json`. The companion paper's code is in [llm-pricing-deterrence-audit](https://github.com/dshi2/llm-pricing-deterrence-audit).

The market model and prompts come from [the Apart starter](https://github.com/poseidon-research/collusion_hackathon), based on [algorithmic_pricing_llms](https://github.com/luciasauer/algorithmic_pricing_llms); it is fetched, not bundled, and keeps its own license. The code in this repository is released under the [MIT License](LICENSE).

The evidence audit is called `covert` in code and configs, and its runs live in folders named `fallback2_*`; these names are stored in the run data.
