# PathSnap: ML map-matching with HMM/Viterbi route reconstruction

Noisy 1 Hz GPS points are matched to a road network. A classifier scores every
(GPS observation, nearby road arc) candidate; an HMM decoded with Viterbi then picks a
connected route. A FastAPI backend (Laptop 1) serves the pipeline and a browser UI
(Laptop 2) lets the evaluator pick a trip and see the predicted route and accuracy.

## Repository layout

| Folder | Contents |
|---|---|
| `src/pathsnap/preprocess/` | raw readers, geometry helpers, candidate generation + labels |
| `src/pathsnap/features/` | feature definitions (see `models/zoo.py::FEATURES`; features are produced in `preprocess/candidates.py`) |
| `src/pathsnap/models/` | model zoo, metrics (`evaluate.py`) |
| `src/pathsnap/hmm/` | HMM + Viterbi decoder (`viterbi.py`) |
| `src/pathsnap/pipeline.py` | inference pipeline used by the API |
| `scripts/` | numbered scripts, run in order (see below) |
| `api/` | FastAPI backend |
| `ui/` | evaluator UI (single static page) |
| `configs/` | tuned hyperparameters and HMM configuration |
| `artifacts/` | exported model (`model.joblib`) and metadata |
| `reports/` | inventory, experiment logs, result CSVs, figures |
| `maps/` | interactive Folium maps |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Raw data is **not** committed. Point the code at the folder that contains `train/` and
`student_test/` (each trip folder holds `.track .nodes .arcs .route`):

```bash
export PATHSNAP_DATA_DIR="/path/to/Student folder"   # default: ../Student folder
```

## Reproduce the experiments

```bash
python scripts/01_inventory.py          # dataset inventory + data-quality checks -> reports/inventory_*.csv
python scripts/02_build_candidates.py   # candidates, features, labels, candidate miss rate
python scripts/03_train_compare.py      # >=5 models, 5-fold GroupKFold CV, student-test scores
python scripts/04b_bayes_opt.py 25 600  # Bayesian optimisation (Optuna TPE) of the chosen model
python scripts/05_export_model.py       # fit final model on the 80 training trips -> artifacts/
python scripts/04_hmm_eval.py <model>   # tune HMM parameters (train OOF only) + classifier vs HMM
python scripts/06_make_maps.py student_test 00000000   # Folium maps -> maps/
python scripts/07_plots.py              # figures -> reports/figures/
python scripts/08_results_summary.py    # tables -> reports/results_tables.md
```

Seeds are fixed (`RANDOM_SEED = 42` in `src/pathsnap/config.py`). Every result quoted in
the report comes from the CSV/JSON files in `reports/`.

## Run the system (two laptops)

Both laptops must be on the **same network**. College Wi-Fi often blocks device-to-device
traffic ("client isolation"); if it does, use a phone hotspot or an ethernet cable.

### Laptop 1 - API + model

Linux / macOS:

```bash
export PATHSNAP_DATA_DIR="/path/to/Student folder"   # folder containing train/ and student_test/
export PATHSNAP_EVAL_PARTITION=student_test           # partition served to the UI
./run_api.sh                                          # prints this laptop's LAN address
```

Windows (CMD):

```bat
set PATHSNAP_DATA_DIR=C:\path\to\Student folder
set PATHSNAP_EVAL_PARTITION=student_test
.venv\Scripts\uvicorn api.main:app --host 0.0.0.0 --port 8000
ipconfig
```

Find the IPv4 address (Linux: `hostname -I`, Windows: `ipconfig`) and allow port 8000 through
the firewall (Linux: `sudo ufw allow 8000/tcp`; Windows: allow an inbound rule for TCP 8000 or
accept the Python prompt). Every request is logged in this console.

### Laptop 2 - UI

Do **not** double-click `ui/index.html`. Serve it over http:

```bash
./run_ui.sh                      # or:  cd ui && python3 -m http.server 8080
```

Windows: `cd ui` then `python -m http.server 8080`. Open `http://localhost:8080`, enter
`http://<laptop-1-address>:8000` as the API address, click **Load trips**, choose a trip, click
**Run prediction**. Check the connection first from laptop 2 with
`curl http://<laptop-1-address>:8000/health` (or open that URL in the browser).

Ground truth (`.route`) is read only inside the server-side scoring step, never by the
prediction pipeline and never sent to the UI.

### Viewing the Folium maps

Serve them over http as well: `cd maps && python3 -m http.server 8090`, then open
`http://localhost:8090/map_student_test_00000000.html`.

### Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Map tiles all say **"Access blocked"** | The HTML was opened as a file (`file://`). OpenStreetMap blocks tile requests without a Referer. Serve the page over http as above. |
| **"Cannot reach the API"** / `Failed to fetch` | Wrong address, different network, or firewall. Check with `curl http://<ip>:8000/health` from laptop 2; start the API with `--host 0.0.0.0` (not 127.0.0.1); allow port 8000; try a phone hotspot. |
| Browser console shows `ERR_BLOCKED_BY_CLIENT` | A browser extension (ad/privacy blocker), security software or browser policy blocked the request. Disable it for the page, or use a private window / another browser. |
| Page loads but the map area is empty | The Leaflet files come from `unpkg.com`; a network that blocks it hides the map. Use another network. |
| API fails to start with a data-path error | Set `PATHSNAP_DATA_DIR` to the folder containing `train/` and `student_test/`. |

## Notes on the data

- Trips come from many places worldwide, so each trip is projected to metres with its own
  local azimuthal-equidistant projection (not one global UTM zone).
- Reference route labels: each GPS point's reference arc is the nearest arc of that trip's
  `.route` (the route has no per-point timestamps). This is an assumption, see the report.
- A few training trips have road networks that do not cover the whole track
  (e.g. trip 00000054); these show up as a high candidate miss rate in
  `reports/candidate_stats_train.csv`.
