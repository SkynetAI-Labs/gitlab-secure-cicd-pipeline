"""Release-risk demonstration API. No deployment authority is granted by this service."""

from flask import Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider
from werkzeug.exceptions import HTTPException

COUNTERS = ("critical", "high", "medium", "low")
FIELDS = frozenset((*COUNTERS, "tests_passed", "secrets_found"))
MAX_FINDINGS = 1_000_000


def unique_json_object(pairs):
    """Reject ambiguous JSON objects before any release decision is evaluated."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON fields are not permitted")
        result[key] = value
    return result


class StrictJSONProvider(DefaultJSONProvider):
    def loads(self, value, **kwargs):
        kwargs["object_pairs_hook"] = unique_json_object
        return super().loads(value, **kwargs)


def evaluate(payload: object) -> dict:
    """Validate an untrusted scan summary and apply an explicit fail-closed policy."""
    if not isinstance(payload, dict) or set(payload) != FIELDS:
        raise ValueError("Exactly the documented six fields are required")
    for field in COUNTERS:
        value = payload[field]
        if type(value) is not int or not 0 <= value <= MAX_FINDINGS:
            raise ValueError("Finding counts must be integers between 0 and 1000000")
    for field in ("tests_passed", "secrets_found"):
        if type(payload[field]) is not bool:
            raise ValueError("Test and secret indicators must be JSON booleans")
    reasons = []
    if not payload["tests_passed"]:
        reasons.append("tests_failed")
    if payload["secrets_found"]:
        reasons.append("secrets_detected")
    if payload["critical"]:
        reasons.append("critical_findings")
    if payload["high"]:
        reasons.append("high_findings")
    return {"decision": "block" if reasons else "allow", "reasons": reasons}


def create_app() -> Flask:
    app = Flask(__name__)
    app.json = StrictJSONProvider(app)
    app.config.update(MAX_CONTENT_LENGTH=4096, DEBUG=False, TESTING=False)

    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.name), error.code

    @app.get("/healthz")
    def health():
        return jsonify(status="ok")

    @app.post("/evaluate")
    def evaluate_request():
        if not request.is_json:
            return jsonify(error="Content-Type must be application/json"), 415
        try:
            result = evaluate(request.get_json())
        except ValueError as error:
            return jsonify(error=str(error)), 400
        return jsonify(result)

    return app
