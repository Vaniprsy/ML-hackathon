"""API tests. They need the trip data and the exported model
(artifacts/model.joblib), so they are skipped when either is missing."""
import pytest

from pathsnap import config

DATA_OK = (config.DATA_DIR / "student_test").exists()
MODEL_OK = (config.ARTIFACTS_DIR / "model.joblib").exists()

pytestmark = pytest.mark.skipif(not (DATA_OK and MODEL_OK),
                                reason="needs PATHSNAP_DATA_DIR data and artifacts/model.joblib")

EXPECTED_KEYS = {"trip_id", "n_obs", "gps_points", "predicted_route", "predicted_arcs",
                 "metrics", "elapsed_s"}


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_trips_lists_ten_ids(client):
    ids = client.get("/trips").json()["trips"]
    assert len(ids) == 10 and all(i.isdigit() for i in ids)


def test_unknown_trip_is_404(client):
    assert client.post("/predict", json={"trip_id": "99999999"}).status_code == 404


def test_path_traversal_is_rejected(client):
    r = client.post("/predict", json={"trip_id": "../train/00000001"})
    assert r.status_code == 404


def test_predict_response_shape_and_no_reference_route(client):
    trip = client.get("/trips").json()["trips"][0]
    r = client.post("/predict", json={"trip_id": trip})
    assert r.status_code == 200
    j = r.json()
    assert set(j) == EXPECTED_KEYS                       # no reference route / labels returned
    assert len(j["predicted_arcs"]) == j["n_obs"] == len(j["gps_points"])
    assert len(j["predicted_route"]) > 0
    assert 0.0 <= j["metrics"]["hmm_top1_all"] <= 1.0


def test_cors_allows_private_network_preflight(client):
    r = client.options("/predict", headers={
        "Origin": "http://192.168.0.20:8080",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Private-Network": "true",
        "Access-Control-Request-Headers": "content-type"})
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-private-network") == "true"


def test_prediction_pipeline_rejects_reference_labels():
    from pathsnap.pipeline import PathSnapPipeline
    from pathsnap.preprocess.io import list_trips, load_trip
    tid = list_trips("student_test")[0]
    with pytest.raises(AssertionError):
        PathSnapPipeline().predict(load_trip(tid, "student_test", with_route=True))
