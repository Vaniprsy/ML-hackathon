#!/usr/bin/env bash
# Laptop 1: start the PathSnap API on all network interfaces, port 8000.
#   PATHSNAP_DATA_DIR       folder containing the trip partitions (train/, student_test/, ...)
#   PATHSNAP_EVAL_PARTITION partition served to the UI (default: student_test)
set -euo pipefail
cd "$(dirname "$0")"
export PATHSNAP_DATA_DIR="${PATHSNAP_DATA_DIR:-$(pwd)/../Student folder}"
export PATHSNAP_EVAL_PARTITION="${PATHSNAP_EVAL_PARTITION:-student_test}"
PY=./.venv/bin/uvicorn
command -v "$PY" >/dev/null 2>&1 || PY=uvicorn
echo "Data dir : $PATHSNAP_DATA_DIR"
echo "Partition: $PATHSNAP_EVAL_PARTITION"
echo "Your LAN address(es) for the UI (use http://<address>:8000):"
hostname -I 2>/dev/null || true
exec "$PY" api.main:app --host 0.0.0.0 --port 8000
