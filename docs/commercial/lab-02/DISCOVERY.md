# Account hypothesis and discovery cards

Use the [Lab 01 SaaS/fintech scenario](../../CASE_STUDY.md) as context. This is a hypothetical engineering organisation with several repositories and a possible release-evidence problem. Headcount, stack, pain, budget, and purchase timing are unqualified. No real employees, customer conversations, or validated personas are represented.

## Stakeholder map to validate

| Proposed role | What to learn | Evidence or commitment |
| --- | --- | --- |
| CTO / VP Engineering: potential economic buyer | Priority, budget ownership, business consequence, timing | Agreed problem and funding path; no assumed executive sponsorship |
| Platform lead: potential technical champion | Current pipeline ownership, standardisation effort, operator capacity | One representative service and a named pilot owner |
| AppSec lead: security stakeholder | Mandatory controls, triage, exceptions, evidence needs | Written acceptance policy and exception owner |
| Procurement / finance | Existing commitments, renewal dates, commercial constraints | Complete quotes and like-for-like cost horizon |
| Service team / developers | What works today, disruption tolerance, training needs | User acceptance criteria and unacceptable changes |

## Eight conversation cards

| Card | Ask in the buyer's words | Follow-up / evidence | Qualification consequence |
| --- | --- | --- | --- |
| 1 · Concrete pain | “Walk me through the last release that needed extra manual checking.” | Which step, who performed it, and what happened? Ask to inspect a redacted example. | If no repeated problem emerges, do not create urgency. |
| 2 · Traceability | “What evidence can you retrieve for that exact commit and image?” | Time a retrieval; identify missing links, expiry, and reviewer needs. | Establish a measurable evidence gap rather than a generic security concern. |
| 3 · Baseline | “How many releases and minutes of manual review occur per month?” | How was it measured? Separate review, scanner triage, and operator maintenance. | Keep estimates labelled; avoid counting the same time twice. |
| 4 · Governance | “Which checks block delivery, and who can approve an exception?” | Ask for policy, severity thresholds, ownership, and expiry. | No pilot without an accountable policy owner. |
| 5 · Existing value | “What works well in GitHub or GitLab that must be preserved?” | Capture integrations, developer experience, and controls they trust. | Make retention of the current platform a valid outcome. |
| 6 · Commercial reality | “Which licences, integrations, and renewals are already committed?” | Validate decision-maker, funding, remaining commitments, and exit terms. | Unknown budget or no retireable cost weakens a migration case. |
| 7 · Change constraints | “What would make a migration unacceptable?” | Probe OS/network needs, downtime, data location, retraining, and rollback. | A non-negotiable unmet requirement can qualify the opportunity out. |
| 8 · Decision process | “Who will judge a pilot, using which baseline and decision date?” | Confirm sponsor, scorecard sign-off, review meeting, and next action. | A pilot without owners or criteria is discovery, not a qualified evaluation. |

## Thirty-minute meeting plan

Spend five minutes confirming context and what already works, ten on a concrete release/evidence example, ten on baseline/constraints/stakeholders, and five agreeing whether a further evaluation is justified. Summarise the buyer's words and unknowns; do not fill gaps with invented facts.

**Qualify in:** a repeated measurable problem, accountable owner, relevant requirements, and willingness to test. **Defer:** missing baseline, absent sponsor, or no decision process. **Qualify out:** current controls satisfy the need and change costs outweigh plausible benefits, or a hard requirement cannot be met.

## Blank call record

Date / participants / current platform: **not collected**. Problem and example: **unvalidated**. Baseline and measurement method: **unknown**. Economic buyer and champion: **unconfirmed**. Funding / renewals / decision date: **unknown**. Constraints / mandatory controls: **unconfirmed**. Next action / owner / agreed date: **not agreed**.

Store only buyer-approved, redacted notes. This portfolio contains no prospect data and no outreach record. Use [objection cards](OBJECTIONS.md) and the [pilot plan](PILOT_SCORECARD.md) only if discovery supports them.
