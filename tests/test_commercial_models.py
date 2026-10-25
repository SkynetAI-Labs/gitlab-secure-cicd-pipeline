"""Regression checks for the fictional commercial model, not sales outcomes."""

import csv
import importlib.util
import json
from copy import deepcopy
from decimal import Decimal
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "docs" / "commercial" / "lab-04"
SPEC = importlib.util.spec_from_file_location("commercial_models", LAB / "calculate_models.py")
model = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(model)


@pytest.fixture
def inputs():
    return json.loads((LAB / "model-inputs.json").read_text(encoding="utf-8"))


@pytest.fixture
def account():
    return {
        "account_alias": "Synthetic regression fixture",
        "evidence_class": "Fictional test input",
        **{f"C{i}": "0" for i in range(1, 6)},
        "problem_confirmed": "Yes",
        "mandatory_fit": "Yes",
        "outreach_approval": "Yes",
    }


def test_committed_model_results_are_reproducible():
    saved = json.loads((LAB / "model-results.json").read_text(encoding="utf-8"))
    assert model.build(LAB) == saved


def test_funnel_uses_conditional_account_denominators(inputs):
    result = model.calculate_funnel(inputs["funnel"], inputs["capacity"])
    assert [s["expected_accounts"]["qualified"] for s in result["scenarios"]] == [
        "0.09",
        "0.6",
        "1.7496",
    ]
    for scenario in result["scenarios"]:
        stages = list(scenario["expected_accounts"].values())
        assert all(Decimal(b) <= Decimal(a) for a, b in zip(stages, stages[1:], strict=False))


def test_capacity_accounts_for_every_work_category(inputs):
    result = model.calculate_funnel(inputs["funnel"], inputs["capacity"])["capacity"]
    assert result["maximum_hypothetical_actions"] == "150"
    assert result["total_hours"] == "72.5"
    assert result["available_hours"] == "80"
    assert result["headroom_hours"] == "7.5"
    assert result["within_assumed_capacity"] is True
    reduced = deepcopy(inputs["capacity"])
    reduced["available_hours"] = "70"
    overloaded = model.calculate_funnel(inputs["funnel"], reduced)["capacity"]
    assert overloaded["headroom_hours"] == "-2.5"
    assert overloaded["within_assumed_capacity"] is False


def test_blank_score_is_not_a_confirmed_zero(account, inputs):
    result = model.score_account(account, inputs["prioritisation"])
    assert result["score_status"] == "Complete"
    assert result["score_out_of_100"] == "0.00"
    account["C1"] = ""
    result = model.score_account(account, inputs["prioritisation"])
    assert result["score_status"] == "Incomplete"
    assert result["score_out_of_100"] is None
    assert result["disposition"] == "Research/clarification only"


@pytest.mark.parametrize(
    "field,value,expected",
    [
        ("mandatory_fit", "No", "Exclude"),
        ("problem_confirmed", "No", "Defer"),
        ("outreach_approval", "No", "Research/clarification only"),
        ("problem_confirmed", "Unknown", "Research/clarification only"),
    ],
)
def test_gates_override_a_high_score(account, inputs, field, value, expected):
    account.update({f"C{i}": str(inputs["prioritisation"]["rating_max"]) for i in range(1, 6)})
    account[field] = value
    result = model.score_account(account, inputs["prioritisation"])
    assert result["score_out_of_100"] == "100.00"
    assert result["disposition"] == expected
    assert result["contact_authorised"] is False


def test_complete_score_never_authorises_contact(account, inputs):
    result = model.score_account(account, inputs["prioritisation"])
    assert result["disposition"] == "Human review only; not authority to contact"
    assert result["contact_authorised"] is False


@pytest.mark.parametrize("bad", [-1, True, "NaN", "Infinity", "wrong", 1.01])
def test_invalid_rates_rejected(bad):
    with pytest.raises(ValueError):
        model.rate(bad, "rate")


@pytest.mark.parametrize("bad", [-1, True, "NaN", "Infinity", "wrong", 1.1])
def test_invalid_whole_counts_rejected(bad):
    with pytest.raises(ValueError):
        model.whole(bad, "count")


def test_scoring_configuration_requires_distinct_criteria_and_total_weight(inputs):
    config = deepcopy(inputs["prioritisation"])
    config["criteria"][0]["weight"] += 1
    with pytest.raises(ValueError):
        model.validate_scoring(config)
    config = deepcopy(inputs["prioritisation"])
    config["criteria"][0]["id"] = config["criteria"][1]["id"]
    with pytest.raises(ValueError):
        model.validate_scoring(config)


def test_invalid_rating_and_gate_rejected(account, inputs):
    account["C1"] = str(inputs["prioritisation"]["rating_max"] + 1)
    with pytest.raises(ValueError):
        model.score_account(account, inputs["prioritisation"])
    account["C1"] = "0"
    account["mandatory_fit"] = "Maybe"
    with pytest.raises(ValueError):
        model.score_account(account, inputs["prioritisation"])


def test_duplicate_scenario_ids_rejected(inputs):
    config = deepcopy(inputs["funnel"])
    config["scenarios"][1]["id"] = config["scenarios"][0]["id"]
    with pytest.raises(ValueError):
        model.calculate_funnel(config, inputs["capacity"])


def test_all_fictional_examples_and_blank_templates_remain_unsent(inputs):
    for filename in ["fictional-accounts.csv", "prioritisation-template.csv"]:
        with (LAB / filename).open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            result = model.score_account(row, inputs["prioritisation"])
            assert result["contact_authorised"] is False
            if filename == "prioritisation-template.csv":
                assert result["score_status"] == "Incomplete"
