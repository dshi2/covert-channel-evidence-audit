# Reproducing this paper

The README gives installation and complete command examples. Analysis and plotting run offline from saved records. Inputs must be stable, model-specific folders; output must be a fresh directory outside the input. The raw dataset is not yet bundled in this code release.

## Table and figure map

Manuscript numbering can change during layout; the content and source columns identify each artifact.

| Paper item | Command / source | Output / assembly |
|---|---|---|
| §4.1: collection accounting (prose) | F2 report commands plus original-cap snapshot and attempt/launch records | `tables/cases.csv`, `tables/accounting.csv`; count each case once, not once per question. Budgets, failures and original-cap/recovery history require explicit reconciliation, not just a final count. |
| Table 1: correctness by evidence view | `scripts.build_f2_paper_tables …` | `PAPER_TABLES.md` correctness section and `metrics.csv`; preserve planned denominators and block-based intervals. |
| Table 2: primary dependence metrics and same-case baselines | Same F2 table command | `metrics.csv`, `same_case_comparisons.csv`, `same_case_baseline_scores.csv`; select the `dependent` question and named metrics/views. Raw numerator/denominator and mean within-block rate are distinct quantities. |
| Supplementary per-model metric panels | `scripts.plot_f2_metrics … --metrics unsupported_positive resolved_accuracy` | `f2_metrics_{tag}.png/.pdf/.svg`; use matching `summary.csv`, show applicable denominators, and keep all-metric sheets in the supplement. |
| Figure 1: experimental design | `python -m scripts.build_paper_diagrams --out reports/designs` | `report2_evidence_audit_design.png`, PDF and SVG; select this paper’s design. |

| Figure 2: unsupported positive and negative dependence judgments | `python -m scripts.build_readme_results` | `figures/results_summary.png` and `.svg`, from bundled `metrics.csv`; preserves within-block means and intervals. |

## Verification and provenance

`run_saved_report.py` records input/output hashes, git revision, dirty-tree status and Python/library versions in `report_manifest.json`. Keep the manifest alongside tables and plots. Original collection source is archived under `provenance/`; the reporting release has its own commit. Auxiliary audit and table scripts have their own manifests with different fields; the diagram generator does not emit a manifest.

The review notebook displays a short, explicit selection of figures. All generated diagnostic plots remain in the report folder; they need not all appear in the paper. A plot generated from scripted fixtures validates the pipeline, not the empirical result.

A complete paper reproduction additionally requires the frozen journals and reconciliation against the reported numbers. Passing unit tests does not establish that this final rebuild has occurred.

## README results

`python -m scripts.build_readme_results` verifies the bundled export hashes, regenerates `results/README_TABLE.md`, replaces the marked README table and creates `figures/results_summary.png` and SVG. No API calls are made. This is an export-to-figure check, separate from the raw-journal reporting commands.
