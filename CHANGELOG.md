# Change log

All changes below were made after the submission deadline (26 October 2026, 11:59 UTC). The submitted version is tagged `pre-maintenance-2026-10-26` (commit `e8ceb7b`). None of them changes experiment settings, saved results, statistical definitions or the report.

## 26 October 2026

- Organised `paper/` around the final report PDF and its checksum; moved the pre-collection protocol to `provenance/protocols/` and the scripted control results to `results/controls/`.
- Removed the code, configs, tests and review notebook used only by the pricing study, including from the collection snapshot and the source file list. Renamed two report scripts to `build_paper_tables.py` and `plot_metrics.py`.
- Rewrote the README and the reproduction guide, matched the guide to the report's tables and figures, and added figure captions and a statement of what is new.
- Matched the citation title to the report, set the minimum Python version to 3.12, removed figure-drafting notes and added the MIT License.
