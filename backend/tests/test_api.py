import io
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.data_gen.generators import generate_id_card

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "models_loaded" in data

def test_models_list_and_activate():
    # List models
    res = client.get("/v1/models")
    assert res.status_code == 200
    models = res.json()
    assert len(models) >= 4
    
    # Activate version
    act_res = client.post("/v1/models/forgery/activate", json={"version": "v1.0.0-vit-baseline-phase1"})
    assert act_res.status_code == 200
    assert act_res.json()["active_version"] == "v1.0.0-vit-baseline-phase1"

def test_robustness_report():
    res = client.get("/v1/eval/robustness-report")
    assert res.status_code == 200
    data = res.json()
    assert "metrics_a" in data
    assert "metrics_b" in data
    assert data["metrics_b"]["auroc"] > data["metrics_a"]["auroc"]

def test_analyze_document_sync():
    img, meta = generate_id_card(seed=99)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/v1/documents/analyze",
        files={"file": ("test_id.png", buf.getvalue(), "image/png")},
        data={"document_type_hint": "id_card"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["document_type"] == "id_card"
    assert "risk_score" in data
    assert "fields" in data
    assert len(data["fields"]) > 0

def test_analyze_document_async():
    img, meta = generate_id_card(seed=100)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/v1/documents/analyze/async",
        files={"file": ("test_async.png", buf.getvalue(), "image/png")},
        data={"document_type_hint": "id_card"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "queued"
