# Result tables (generated from reports/*.csv; do not edit by hand)

## 3.1 Model comparison (CV = 5-fold GroupKFold on 80 train trips; test = 10 student-test trips)

| model | family | config | cv_macro_f1_mean | cv_macro_f1_std | cv_top1_mean | test_top1_all | test_macro_f1 | test_log_loss | test_route_continuity | train_fit_top1 | train_time_s | inference_s_per_1k_candidates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| logreg | Linear | C=1.0, L2, scaled | 0.8632 | 0.0225 | 0.7353 | 0.8283 | 0.8886 | 0.1267 | 0.9108 | 0.7364 | 1.5542 | 0.0001 |
| gaussian_nb | Probabilistic | var_smoothing=1e-9 | 0.7636 | 0.0144 | 0.7175 | 0.7946 | 0.7731 | 0.4684 | 0.9068 | 0.7196 | 0.2805 | 0.0001 |
| decision_tree | Tree | max_depth=12, min_samples_leaf=50 | 0.8703 | 0.0359 | 0.7415 | 0.8406 | 0.9027 | 0.1027 | 0.9167 | 0.7639 | 11.4608 | 0.0000 |
| random_forest | Ensemble (bagging) | n_estimators=60, max_depth=14, min_samples_leaf=30 | 0.8893 | 0.0118 | 0.7439 | 0.8397 | 0.9053 | 0.0956 | 0.9188 | 0.7668 | 31.3245 | 0.0005 |
| hist_gb | Boosting | max_iter=200, lr=0.1, max_leaf_nodes=31 | 0.8880 | 0.0125 | 0.7460 | 0.8385 | 0.9029 | 0.0980 | 0.9173 | 0.7710 | 4.9785 | 0.0008 |
| mlp | Neural network | hidden=(64,32), adam, max_iter=25, scaled | 0.8821 | 0.0138 | 0.7388 | 0.8348 | 0.8981 | 0.1017 | 0.9167 | 0.7660 | 47.3149 | 0.0002 |

## 4. Bayesian optimisation

Trials: 12 (budget 600 s), sampler Optuna TPE, objective: mean candidate-level macro-F1, CV: GroupKFold(5) by trip, 80 train trips

Best params: `{"learning_rate": 0.021146536167031597, "max_iter": 400, "max_leaf_nodes": 109, "min_samples_leaf": 39, "l2_regularization": 0.0008111941985431928}`


| model | cv_macro_f1 | cv_top1_all | cv_log_loss | test_top1_all | test_macro_f1 | test_log_loss | test_route_continuity | train_time_s | inference_s_per_1k_candidates |
|---|---|---|---|---|---|---|---|---|---|
| untuned | 0.8880 | 0.7467 | 0.1219 | 0.8385 | 0.9029 | 0.0980 | 0.9173 | 5.0167 | 0.0008 |
| tuned_bayes | 0.8914 | 0.7481 | 0.1156 | 0.8409 | 0.9046 | 0.0945 | 0.9206 | 25.5127 | 0.0038 |

### All trials

| number | value | params_l2_regularization | params_learning_rate | params_max_iter | params_max_leaf_nodes | params_min_samples_leaf | duration |
|---|---|---|---|---|---|---|---|
| 0 | 0.8882 | 0.0001 | 0.1000 | 200 | 31 | 20 | 0 days 00:00:20.635468 |
| 1 | 0.8894 | 0.0006 | 0.0551 | 400 | 97 | 136 | 0 days 00:01:33.392167 |
| 2 | 0.8849 | 0.3470 | 0.0305 | 100 | 112 | 137 | 0 days 00:00:31.299258 |
| 3 | 0.8914 | 0.0008 | 0.0211 | 400 | 109 | 39 | 0 days 00:01:56.638134 |
| 4 | 0.8899 | 0.0029 | 0.0329 | 200 | 74 | 79 | 0 days 00:00:54.536668 |
| 5 | 0.8880 | 0.0191 | 0.1049 | 100 | 48 | 64 | 0 days 00:00:23.597662 |
| 6 | 0.8893 | 0.0002 | 0.1677 | 150 | 73 | 133 | 0 days 00:00:22.648975 |
| 7 | 0.8905 | 6.7322 | 0.1036 | 150 | 22 | 424 | 0 days 00:00:30.831842 |
| 8 | 0.8889 | 0.0159 | 0.1786 | 200 | 26 | 180 | 0 days 00:00:19.523117 |
| 9 | 0.8908 | 0.0020 | 0.0278 | 250 | 18 | 373 | 0 days 00:00:46.932015 |
| 10 | 0.8903 | 0.0002 | 0.0258 | 350 | 116 | 20 | 0 days 00:01:36.360623 |
| 11 | 0.8902 | 0.0020 | 0.0432 | 350 | 17 | 54 | 0 days 00:00:54.891019 |

## 5. HMM vs classifier-only

| partition | method | top1_all | top1_covered | route_continuity | decode_s |
|---|---|---|---|---|---|
| train_oof_80_trips | classifier_only | 0.7481 | 0.8311 | 0.9182 | nan |
| train_oof_80_trips | classifier+HMM | 0.7955 | 0.8838 | 0.9790 | 2.5307 |
| student_test_10_trips | classifier_only | 0.8409 | 0.8424 | 0.9206 | nan |
| student_test_10_trips | classifier+HMM | 0.8741 | 0.8756 | 0.9802 | 0.2401 |

### Decoder grid (top 8 by top1_all, tuning trips only)

| beta | lam | w | top1_all | top1_covered | route_continuity |
|---|---|---|---|---|---|
| 10.0000 | 8.0000 | 0.5000 | 0.8118 | 0.8705 | 0.9749 |
| 20.0000 | 4.0000 | 1.0000 | 0.8117 | 0.8704 | 0.9617 |
| 6.0000 | 8.0000 | 1.0000 | 0.8111 | 0.8698 | 0.9718 |
| 10.0000 | 8.0000 | 1.0000 | 0.8107 | 0.8694 | 0.9722 |
| 20.0000 | 4.0000 | 0.5000 | 0.8107 | 0.8694 | 0.9722 |
| 6.0000 | 16.0000 | 1.0000 | 0.8106 | 0.8693 | 0.9749 |
| 10.0000 | 4.0000 | 0.5000 | 0.8106 | 0.8692 | 0.9710 |
| 10.0000 | 4.0000 | 1.0000 | 0.8105 | 0.8692 | 0.9620 |

## Candidate miss rate, train

median 0.0000, max 0.8140, trips above 5%: 5

## Candidate miss rate, student_test

median 0.0000, max 0.0071, trips above 5%: 0
