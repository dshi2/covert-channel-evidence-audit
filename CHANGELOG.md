# Change log

## 2026-10-26: documentation maintenance

- Updated the report-to-script map to reflect the final table numbering and prose accounting.
- Identified the generator for the combined results figure separately from supplementary diagnostic panels.
- Clarified bundled-export reproduction versus raw-journal analysis and new paid collection.
- Aligned the README title with the final evidence-sufficiency report.

- Matched the citation titles to the reports, set the minimum Python version to 3.12 removed figure-drafting notes and added the MIT License.
- Removed the pricing-study files from the collection snapshot and the source file list; the remaining snapshot files are unchanged.

No experiment settings, saved results, statistical definitions or submitted PDFs were changed.

Previous repository state: `e8ceb7b9976dd77b9497218d687e232b01605f84`, retained as `pre-maintenance-2026-10-26`.

- Renamed public protocol, control and notebook paths to descriptive experiment names; updated notebook-test paths and added a repository map. Legacy runtime identifiers remain compatible.

- Removed code, configurations, tests and a review notebook used only by the pricing study, and renamed `build_f2_paper_tables.py` and `plot_f2_metrics.py` to `build_paper_tables.py` and `plot_metrics.py`. The README table and bundled exports regenerate unchanged.

- Organized `paper/` around the final exported PDF and its checksum; moved historical planning to `provenance/protocols/` and scripted controls to `results/controls/`.
