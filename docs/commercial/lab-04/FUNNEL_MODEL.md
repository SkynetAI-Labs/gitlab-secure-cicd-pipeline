# Hypothetical funnel and capacity assumptions

**Mathematical illustration only—not a benchmark, forecast commitment, campaign result or achieved meeting claim.** Inputs are in [model-inputs.json](model-inputs.json), outputs in [model-results.json](model-results.json), and the standard-library [calculator](calculate_models.py) is reproducible without network or sending capabilities.

## Cohort and denominators

Use one hypothetical 90-day cohort of **100 unique account placeholders**. For arithmetic, all modelled transitions are assumed observable within that window. Real cohorts can cross windows; they must be tracked separately. One initial stakeholder thread and at most one first conversation per account are counted, so message volume and people are not substituted for account denominators.

| Stage | Denominator / assumption | Base mathematical expectation |
| --- | --- | --- |
| Screened accounts | Assumed starting cohort | 100 |
| Research-fit accounts | 60% of screened | 60 |
| Hypothetically eligible accounts | 50% of research-fit; assumes all real-world approval gates could be satisfied | 30 |
| Responding accounts | 20% of eligible accounts | 6 |
| Positive responding accounts | 50% of responding accounts | 3 |
| First-conversation acceptance | 50% of positive responding accounts | 1.5 |
| Held first conversations | 80% of accepted accounts | 1.2 |
| Qualified evaluation accounts | 50% of held-conversation accounts, requiring buyer-validated problem/owner/next step | 0.6 |

No actual account is eligible for contact in this portfolio. The gate assumption is a modelling convenience, not verified permission or intent. Fractions are expectations, not counts of people or meetings. Do not round up or present 1.5 as a booked outcome. No win rate, ARR, revenue, contract value or customer count is derived.

## Sensitivity, not vendor or industry rates

Common fit/eligibility assumptions stay at 60%/50%. Low/Base/High vary the next five stage rates respectively:

| Scenario | Reply / positive / accepted / held / qualified rates | Expected qualified evaluation accounts |
| --- | --- | --- |
| Low | 10% / 25% / 40% / 75% / 40% | 0.09 |
| Base | 20% / 50% / 50% / 80% / 50% | 0.6 |
| High | 30% / 60% / 60% / 90% / 60% | 1.7496 |

Every downstream value is the previous stage multiplied by its rate; no rate can exceed 100% or be negative. Low/High are arbitrary sensitivity examples, not confidence intervals. The model uses exact decimal arithmetic and retains fractions instead of inflating them into asserted outcomes.

## Capacity calculation

```text
Research:       100 accounts × 15 minutes                  = 25 hours
Drafting:        30 eligible accounts × 10 minutes         = 5 hours
Maximum actions:30 accounts × 5 actions × 5 minutes        = 12.5 hours
QA / learning / administration reserve                    = 20 hours
Conversation / preparation reserve                        = 10 hours
Total assumed effort                                     = 72.5 hours
Illustrative available time                              = 80 hours
Illustrative headroom                                    = 7.5 hours
```

This is a bounded account-work pilot allocation, not the total working hours of an account executive over 90 days. Stop rules may reduce actions; they are not used to increase conversion expectations. Reserves are assumptions, not observed effort. Re-evaluate capacity if research depth, channel requirements or conversation effort differ. An over-capacity result must be reported, not hidden by raising conversion assumptions.

Run `python3 docs/commercial/lab-04/calculate_models.py` from the repository root to print the model, or add `--output` to regenerate the checked JSON file. No outbound integrations, account-data collection or outreach automation exist in the calculator.
