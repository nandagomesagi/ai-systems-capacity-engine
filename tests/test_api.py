from fastapi.testclient import TestClient

from ai_capacity_engine.api import app


client = TestClient(app)


def test_health_and_default_scenario():
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    scenario = client.get("/api/default-scenario")
    assert scenario.status_code == 200
    assert scenario.json()["location"] == "Northern Virginia"


def test_unknown_domains_withhold_final_capacity():
    response = client.post(
        "/api/evaluate",
        json={
            "target_capacity_mw": 5000,
            "target_date": "2030-12-31",
            "domain_assumptions": {"power": 4200},
        },
    )
    assert response.status_code == 200
    payload = response.json()

    assert payload["deployable_capacity_mw"] is None
    assert payload["provisional_capacity_mw"] == 4200
    assert payload["binding_constraint"] is None
    assert payload["provisional_binding_constraint"] == "power"
    assert "grid" in payload["unknown_domains"]
    assert payload["complete"] is False


def test_all_domains_assumed_produce_conditional_result():
    response = client.post(
        "/api/evaluate",
        json={
            "target_capacity_mw": 5000,
            "target_date": "2030-12-31",
            "domain_assumptions": {
                "power": 4200,
                "grid": 3100,
                "water": 4700,
                "cooling": 4500,
                "network": 5000,
                "permits": 3900,
            },
        },
    )
    assert response.status_code == 200
    payload = response.json()

    assert payload["deployable_capacity_mw"] == 3100
    assert payload["binding_constraint"] == "grid"
    assert payload["architecture_gaps_mw"]["grid"] == 1900
    assert payload["unknown_domains"] == []
    assert payload["complete"] is True
    assert all(
        item["epistemic_state"] == "ASSUMED" for item in payload["scenario_domains"]
    )


def test_unknown_domain_name_is_rejected():
    response = client.post(
        "/api/evaluate",
        json={
            "target_capacity_mw": 5000,
            "target_date": "2030-12-31",
            "domain_assumptions": {"imaginary": 100},
        },
    )
    assert response.status_code == 422
    assert "Unknown domain assumptions" in response.json()["detail"]


def test_firehouse_dependency_trace_is_evidence_aware():
    response = client.get("/api/dependencies/firehouse-grid-delivery/trace")
    assert response.status_code == 200
    payload = response.json()

    assert payload["project_id"] == "loudoun-firehouse-230kv"
    assert payload["target_node"] == "firehouse-data-center-load"
    assert set(payload["ordered_dependencies"]) == {
        "firehouse-230kv-delivery",
        "firehouse-substation",
        "transmission-interconnection",
    }
    assert payload["evidence_refs"] == ["ev-pjm-firehouse-load-request-2026"]


def test_firehouse_critical_path_withholds_unknown_duration():
    response = client.get("/api/dependencies/firehouse-grid-delivery/critical-path")
    assert response.status_code == 200
    payload = response.json()

    assert payload["total_lead_time_days"] is None
    assert payload["complete"] is False
    assert set(payload["unknown_lead_time_nodes"]) == {
        "firehouse-230kv-delivery",
        "firehouse-substation",
        "transmission-interconnection",
    }
