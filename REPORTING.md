# Reproducing the report

All commands run offline from saved journals. Each input is one model's run folder; each output must be a new folder. The raw run archive is not bundled yet.

| Report item | Command | Output |
|---|---|---|
| Collection accounting | `scripts.run_saved_report …` | `tables/cases.csv`, `tables/accounting.csv` (each case counted once) |
| Table 1: correctness by evidence view | `scripts.build_paper_tables …` | `PAPER_TABLES.md`, `metrics.csv` |
| Table 2: dependence metrics and baselines | Same | `metrics.csv`, `same_case_comparisons.csv`, `same_case_baseline_scores.csv` |
| Per-model metric panels (supplement) | `scripts.plot_metrics … --metrics unsupported_positive resolved_accuracy` | `metrics_{tag}.png`, PDF, SVG |
| Figure 1: design | `scripts.build_paper_diagrams --out reports/designs` | `report2_evidence_audit_design.png`, PDF, SVG |
| Figure 2: results | `scripts.build_readme_results` | `figures/results_summary.png`, SVG |

Intervals resample matched blocks, not individual judgments. Keep planned denominators: a missing answer is not an abstention.

`run_saved_report` writes `report_manifest.json` with input and output hashes, the git revision and library versions. Keep it with the tables. The original collection source is archived under `provenance/`.

`build_readme_results` checks the bundled export hashes and regenerates the README table and results figure.
