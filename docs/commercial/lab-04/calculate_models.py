"""Reproduce fictional portfolio scoring and funnel math. No network or sending APIs."""

import argparse
import csv
import json
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path


def number(value, field):
    if isinstance(value, bool):
        raise ValueError(f"{field}: numeric input required")
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"{field}: numeric input required") from error
    if not result.is_finite():
        raise ValueError(f"{field}: finite input required")
    return result


def nonnegative(value, field):
    result = number(value, field)
    if result < 0:
        raise ValueError(f"{field}: nonnegative input required")
    return result


def rate(value, field):
    result = nonnegative(value, field)
    if result > 1:
        raise ValueError(f"{field}: rate must not exceed 1")
    return result


def whole(value, field, minimum=0):
    result = nonnegative(value, field)
    if result != result.to_integral_value() or result < minimum:
        raise ValueError(f"{field}: whole number at or above {minimum} required")
    return result


def display(value):
    return format(value.normalize(), "f")


def validate_scoring(config):
    criteria = config["criteria"]
    if len(criteria) != 5 or {c["id"] for c in criteria} != {f"C{i}" for i in range(1, 6)}:
        raise ValueError("Five distinct scoring criteria C1–C5 required")
    weights = [nonnegative(c["weight"], "criterion weight") for c in criteria]
    if sum(weights) != 100:
        raise ValueError("Scoring weights must total 100")
    whole(config["rating_max"], "rating_max", minimum=1)


def score_account(row, config):
    validate_scoring(config)
    maximum = number(config["rating_max"], "rating_max")
    total = Decimal(0)
    complete = True
    for criterion in config["criteria"]:
        raw = row.get(criterion["id"], "")
        if raw is None or str(raw).strip() == "":
            complete = False
            continue
        rating = whole(raw, criterion["id"])
        if rating > maximum:
            raise ValueError("Rating exceeds configured maximum")
        total += number(criterion["weight"], "weight") * rating / maximum
    gates = {}
    for field in ["problem_confirmed", "mandatory_fit", "outreach_approval"]:
        value = row.get(field, "") or "Unknown"
        if value not in {"Yes", "No", "Unknown"}:
            raise ValueError("Gate must be Yes, No or Unknown")
        gates[field] = value
    if gates["mandatory_fit"] == "No":
        disposition = "Exclude"
    elif gates["problem_confirmed"] == "No":
        disposition = "Defer"
    elif not complete or any(v != "Yes" for v in gates.values()):
        disposition = "Research/clarification only"
    else:
        disposition = "Human review only; not authority to contact"
    return {
        "account_alias": row["account_alias"],
        "evidence_class": row["evidence_class"],
        "score_status": "Complete" if complete else "Incomplete",
        "score_out_of_100": (
            format(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), "f")
            if complete else None
        ),
        "gates": gates,
        "disposition": disposition,
        "contact_authorised": False,
    }


def calculate_funnel(config, capacity):
    whole(config["horizon_days"], "horizon_days", minimum=1)
    screened = whole(config["screened_accounts"], "screened_accounts", minimum=1)
    fit = screened * rate(config["research_fit_rate"], "research_fit_rate")
    eligible = fit * rate(config["eligibility_rate"], "eligibility_rate")
    scenarios = []
    names = set()
    for scenario in config["scenarios"]:
        if scenario["id"] in names:
            raise ValueError("Scenario IDs must be distinct")
        names.add(scenario["id"])
        stages = {"screened": screened, "research_fit": fit, "hypothetically_eligible": eligible}
        current = eligible
        for name in ["reply", "positive", "accepted", "held", "qualified"]:
            current *= rate(scenario["rates"][name], name)
            stages[name] = current
        scenarios.append({"scenario": scenario["id"], "expected_accounts": {
            name: display(value) for name, value in stages.items()
        }})
    max_actions = eligible * whole(capacity["max_actions_per_account"], "max_actions")
    effort = {
        "research_hours": screened * nonnegative(capacity["research_minutes_per_account"], "research_minutes") / 60,
        "drafting_hours": eligible * nonnegative(capacity["draft_minutes_per_eligible_account"], "draft_minutes") / 60,
        "maximum_action_hours": max_actions * nonnegative(capacity["minutes_per_action"], "action_minutes") / 60,
        "qa_learning_admin_hours": nonnegative(capacity["qa_learning_admin_hours"], "qa_hours"),
        "conversation_preparation_reserve_hours": nonnegative(capacity["conversation_preparation_reserve_hours"], "reserve_hours"),
    }
    total = sum(effort.values())
    available = nonnegative(capacity["available_hours"], "available_hours")
    return {
        "horizon_days": config["horizon_days"],
        "unit": "Hypothetical account-level expectations; fractions are not achieved meetings",
        "scenarios": scenarios,
        "capacity": {
            **{key: display(value) for key, value in effort.items()},
            "maximum_hypothetical_actions": display(max_actions),
            "total_hours": display(total),
            "available_hours": display(available),
            "headroom_hours": display(available - total),
            "within_assumed_capacity": total <= available,
        },
    }


def build(root):
    inputs = json.loads((root / "model-inputs.json").read_text())
    accounts = list(csv.DictReader((root / "fictional-accounts.csv").open()))
    templates = list(csv.DictReader((root / "prioritisation-template.csv").open()))
    return {
        "evidence_type": "Fictional inputs and mathematical expectations, not campaign results",
        "execution_status": "Not executed; no real accounts contacted or messages sent",
        "fictional_account_scores": [score_account(row, inputs["prioritisation"]) for row in accounts],
        "blank_template_scores": [score_account(row, inputs["prioritisation"]) for row in templates],
        "funnel_and_capacity": calculate_funnel(inputs["funnel"], inputs["capacity"]),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", action="store_true", help="Write model-results.json beside this script")
    arguments = parser.parse_args()
    directory = Path(__file__).resolve().parent
    rendered = json.dumps(build(directory), indent=2) + "\n"
    if arguments.output:
        (directory / "model-results.json").write_text(rendered)
        print("Regenerated fictional model-results.json; no network or outreach performed")
    else:
        print(rendered, end="")
