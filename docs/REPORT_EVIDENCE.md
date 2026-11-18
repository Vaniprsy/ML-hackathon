# Report evidence checklist

Maps each section of the required report (see the organisers' *Deliverables* document) to the
files in this repository that hold the underlying results. It contains no analysis: the
explanations in the report must be written by the team from these results.
Regenerate the tables with `python scripts/08_results_summary.py` (output: `reports/results_tables.md`).

| Report section | Evidence in the repo | Still to do |
|---|---|---|
| 2.2 EDA: preprocessing, missing values | `scripts/01_inventory.py`, `reports/inventory_summary.txt`, `reports/inventory_train.csv`, `reports/inventory_student_test.csv` | Write the preprocessing answer |
| 2.2 EDA: trajectory plots, network | `reports/figures/eda_trajectories.png`, `eda_train_distributions.png`, `eda_student_test_distributions.png`, `eda_candidate_miss_rate.png` | State the partition used for each plot (train / student_test) |
| 2.2 / 6 Folium map | `scripts/06_make_maps.py`, `maps/map_student_test_00000000.html` | Serve `maps/` over http and take a screenshot for the PDF |
| 3.1 Model comparison table | `reports/model_comparison.csv`, `reports/cv_folds.csv`, table in `reports/results_tables.md` | The MLP run was interrupted (not in the table); log in `reports/experiment_log_03_train_compare.txt` |
| 3.2 Per-model questions A-C | Configurations in `src/pathsnap/models/zoo.py`; metrics in the CSVs above | Write each model's answers from your own results |
| 3.3 Visualisations | `reports/figures/cv_macro_f1.png`, `student_test_top1_f1.png`, `log_loss.png`, `overfitting_check.png`, `confusion_matrices_student_test.png` | Training-loss plot exists only for models with epoch history (`reports/mlp_loss_curve.csv` is not produced because the MLP run was interrupted) |
| 4 Bayesian optimisation | `scripts/04b_bayes_opt.py`, `reports/bayes_trials.csv`, `bayes_summary.json`, `bayes_untuned_vs_tuned.csv`, `reports/figures/bayes_trials.png`, `untuned_vs_tuned.png`, `configs/hgb_best_params.json` | Answer the six questions in the report |
| 5 HMM and Viterbi | `src/pathsnap/hmm/viterbi.py`, `scripts/04_hmm_eval.py`, `reports/hmm_tuning.csv`, `hmm_comparison.csv`, `reports/figures/hmm_vs_classifier.png`, `configs/hmm_config.json` | Describe cases where the HMM did not help (look at per-trip results) |
| 6 Folium maps | `maps/`, `scripts/06_make_maps.py` | Screenshot of one map (layers: GPS, network, reference, classifier-only, classifier+HMM) |
| 7 API, UI, deployment | `api/main.py`, `ui/index.html`, `run_api.sh`, `run_ui.sh`, `tests/test_api.py`, README "Run the system" | **Screenshots needed**: the working UI, and the API console on the receiving laptop showing successful `POST /predict` lines |

## Final evaluation checklist (Laptop 1 = API, Laptop 2 = UI)

- [ ] Evaluator trips are extracted on Laptop 1 only (never on Laptop 2, never committed)
- [ ] `PATHSNAP_EVAL_PARTITION` points to the evaluator partition folder
- [ ] `curl http://<laptop-1-ip>:8000/health` works from Laptop 2
- [ ] UI lists the 10 trips and each one returns a route
- [ ] API console log is visible to show the evaluator
- [ ] Model, configs and code are the committed versions (no changes after the freeze)
