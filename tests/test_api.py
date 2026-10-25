import pytest

from release_gate import MAX_FINDINGS, create_app, evaluate


@pytest.fixture
def summary():
    return dict(critical=0, high=0, medium=3, low=4, tests_passed=True, secrets_found=False)


@pytest.fixture
def client():
    return create_app().test_client()


def test_clean_summary_allowed(summary):
    assert evaluate(summary) == {"decision": "allow", "reasons": []}


@pytest.mark.parametrize(
    "field,value,reason",
    [
        ("critical", 1, "critical_findings"),
        ("high", 1, "high_findings"),
        ("tests_passed", False, "tests_failed"),
        ("secrets_found", True, "secrets_detected"),
    ],
)
def test_each_blocker(summary, field, value, reason):
    summary[field] = value
    assert evaluate(summary) == {"decision": "block", "reasons": [reason]}


def test_combined_blockers(summary):
    summary.update(critical=2, high=3, tests_passed=False, secrets_found=True)
    assert len(evaluate(summary)["reasons"]) == 4


@pytest.mark.parametrize("payload", [None, [], "data", {}, {"extra": 1}])
def test_invalid_shape(payload):
    with pytest.raises(ValueError):
        evaluate(payload)


@pytest.mark.parametrize("field", ["critical", "high", "medium", "low"])
@pytest.mark.parametrize("value", [-1, MAX_FINDINGS + 1, True, 1.2, "0", None])
def test_invalid_counts(summary, field, value):
    summary[field] = value
    with pytest.raises(ValueError):
        evaluate(summary)


@pytest.mark.parametrize("field", ["tests_passed", "secrets_found"])
@pytest.mark.parametrize("value", [0, 1, "true", None])
def test_invalid_booleans(summary, field, value):
    summary[field] = value
    with pytest.raises(ValueError):
        evaluate(summary)


def test_missing_and_extra_fields(summary):
    summary["extra"] = "untrusted"
    with pytest.raises(ValueError):
        evaluate(summary)
    del summary["extra"]
    del summary["low"]
    with pytest.raises(ValueError):
        evaluate(summary)


def test_maximum_counts(summary):
    summary.update(medium=MAX_FINDINGS, low=MAX_FINDINGS)
    assert evaluate(summary)["decision"] == "allow"


def test_health_and_headers(client):
    response = client.get("/healthz")
    assert response.json == {"status": "ok"}
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["Content-Security-Policy"].startswith("default-src 'none'")


def test_http_evaluation(client, summary):
    assert client.post("/evaluate", json=summary).json["decision"] == "allow"
    summary["high"] = 1
    assert client.post("/evaluate", json=summary).json["decision"] == "block"


def test_invalid_summary_is_400(client):
    response = client.post("/evaluate", json={"secret": "do-not-echo"})
    assert response.status_code == 400
    assert b"do-not-echo" not in response.data


def test_malformed_json(client):
    assert client.post("/evaluate", data="{", content_type="application/json").status_code == 400


def test_wrong_content_type(client):
    assert client.post("/evaluate", data="{}").status_code == 415


def test_oversized_body(client):
    response = client.post(
        "/evaluate", data='"' + "x" * 5000 + '"', content_type="application/json"
    )
    assert response.status_code == 413


def test_unknown_route_and_wrong_method(client):
    assert client.get("/unknown").status_code == 404
    assert client.get("/evaluate").status_code == 405
