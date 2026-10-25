# Buyer-owned cost-model template

Download the [editable workbook](cost-model-template.xlsx) or start from the [CSV input template](cost-model-inputs.csv). The workbook contains a guide, blank Low/Base/High scenario sheets, and an explicitly vendor-neutral Illustration sheet. All figures in Illustration are invented arithmetic examples, not quotes, observations, or platform forecasts.

Use the [original Lab 01 commercial case](../../CASE_STUDY.md) for the existing illustrative £310/month capacity example. It is not evidence of realised savings or GitLab ROI. This template adds the missing like-for-like platform decision structure rather than recycling that example as a sales claim.

## Inputs and evidence

Compare **current baseline**, **retain/improve GitHub**, and **evaluate GitLab** over a common horizon and matched release workload. Licence and security-product prices remain blank pending actual quotes. Low/Base/High describe alternative assumptions, not optimistic results assigned to a vendor.

| Input | Unit / evidence owner |
| --- | --- |
| Common horizon, loaded hourly rate, monthly releases | Months / £ per hour / releases; finance and measured operator records |
| Plan licences and incremental security subscriptions | £/month; current contract and written quote; do not count bundled security twice |
| Runner compute, artifacts/storage, integrations/support | £/month; matched usage, retention and support scope, including customer-managed operating costs |
| Pipeline ownership, security triage, manual release review | Hours/month, hours/month, minutes/release; non-overlapping time records |
| Migration and training | One-time in-house hours; scoped work estimate |
| External implementation or other one-time charges | £; approved quote; do not repeat the same work in in-house hours |
| Overlap / unretireable commitments | Additional £ across the horizon; incremental commitments not already in the monthly totals |

For the first three CSV inputs in each scenario, use the same horizon, hourly rate, and workload across all options. Rename option headings after discovery if the current-platform hypothesis differs.

Input cells are deliberately blank; **unknown is not zero**. Enter zero only when a responsible owner confirms a genuine zero, and record the evidence/status in the notes column. The default 12-month horizon is a planning assumption. Blank scenarios return **Incomplete**, not a fabricated total. Spreadsheet validation prevents negative numeric inputs, but reviewer judgement is still needed for consistency, quotes, and scope. There are no macros, external data links, or vendor price feeds.

## Visible calculations

For each option, let `R` = releases/month, `M` = review minutes/release, `H` = ownership hours/month, `T` = triage hours/month, `L` = loaded £/hour, `N` = horizon months, and `C` = the sum of monthly cash cost categories.

```text
Review hours/month                = R × M / 60
Monthly operating labour value    = (H + T + review hours) × L
Monthly economic operating cost   = C + operating labour value
One-time economic change cost     = (migration hours + training hours) × L
                                    + other one-time charges + incremental overlap commitments
Horizon economic TCO              = N × monthly economic operating cost + one-time economic change cost
Economic difference vs baseline   = baseline economic TCO − option economic TCO
Review capacity returned/month    = baseline review hours − option review hours
Review capacity value/month       = returned hours × L
Horizon cash outlay in this model = N × C + other one-time charges + overlap commitments
```

A positive economic difference is a lower modelled total, not automatically a cash saving. Review capacity is already reflected in the labour calculation: **do not subtract it again**. Negative values are valid warnings of an unfavourable option. The cash-outlay view excludes in-house labour valuation; finance must validate whether any budget can actually be retired. Normalise annual quotes to the same period and keep currency/tax treatment consistent. The template is undiscounted and excludes unquantified incident losses; add material missing costs explicitly before a purchase decision.

## Live demonstration without a vendor claim

Illustration uses the labels **Baseline**, **Option A**, and **Option B**, with a 12-month horizon, £75/hour, and 20 releases/month. It demonstrates a useful caution: Option A has lower economic TCO (£11,800 versus £14,100) but higher modelled cash outlay (£3,100 versus £2,400). Those are invented inputs and formula outputs, not a GitLab/GitHub comparison. Option B is another arbitrary sensitivity example. Do not transfer any example numbers into a buyer recommendation.

Complete all three real scenarios with evidence, retain the current-platform option, and use the [pilot scorecard](PILOT_SCORECARD.md) to determine whether benefits materialise. No blanket cheaper-platform conclusion, price quote, discount, purchase recommendation, or ROI guarantee is provided.
