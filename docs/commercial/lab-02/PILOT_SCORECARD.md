# Pilot scorecard and mutual evaluation plan

**Draft proposal only. No buyer pilot or equivalent GitLab/GitHub benchmark has been run.** Agree this document with the buyer before collecting results. Link back to the [comparison](COMPARISON.md), [discovery](DISCOVERY.md), and [cost model](COST_MODEL.md).

## Scope and owners

One representative, buyer-approved **non-production** service; current workflow versus the proposed GitLab configuration. The retained-GitHub option may include agreed improvements rather than an artificially weak baseline. Use equivalent control objectives and record implementation differences, account entitlements, application revision, runner specifications, regions, and network conditions. Do not compare Lab 01 with the different GitHub Lab 03 application as a benchmark.

Proposed roles: platform lead owns execution; AppSec owns control acceptance; service team owns usability; finance/procurement validates costs; economic buyer owns the decision. Actual people, budget, calendar dates, and authority remain **unconfirmed**. Stop if authorisation, safe isolation, or mandatory entitlements are absent.

## Scorecard to agree before starting

| Dimension | Baseline / method | Draft acceptance target, not an agreed result | Owner | Result |
| --- | --- | --- | --- | --- |
| Mandatory controls | Inventory exact required gates, severity policy, exceptions | Every mandatory control demonstrated; one safe synthetic rejection per required failure class | AppSec | Not measured |
| Evidence retrieval | Time a reviewer locating commit, image identity, tests, and scans | Complete agreed evidence within 5 minutes; buyer must confirm threshold | Platform + reviewer | Not measured |
| Manual touch time | Minutes/release from operator records, excluding separately logged triage | At least 20% reduction with no omitted controls; buyer must validate materiality | Service team | Not measured |
| Pipeline duration | Median and p95 wall-clock time; include queue time separately | No worse than 10% above an accepted baseline unless a documented trade-off is approved | Platform | Not measured |
| Runner and storage cost | Usage/billing exports at matched retention and workload | Within buyer-approved budget; no default monetary ceiling invented | Finance | Not measured |
| Triage and maintenance | Minutes/week; classify true findings, false positives, ownership tasks | No increase above an agreed ceiling; record the ceiling before testing | AppSec + platform | Not measured |
| Adoption and disruption | Maintainer walkthrough, integration checklist, exception/rollback exercise | Named maintainers complete the workflow and confirm all non-negotiables | Service team | Not measured |
| Commercial completeness | Quotes, committed costs, migration/training and support estimate | All material inputs confirmed; incomplete TCO cannot justify purchase | Procurement | Not measured |

Targets above are starting points for discussion, not industry standards or buyer commitments. A mandatory safety/security requirement is a veto; do not conceal a failure inside a weighted average.

## Measurement and evidence plan

1. **Discovery and sign-off:** validate the problem, decision-maker, scope, metrics, thresholds, budget, and a decision date. No validated buyer is assumed.
2. **Baseline:** observe a representative period (proposed: two weeks). If release volume is too low, extend it rather than inventing a reliable average.
3. **Comparable trials:** propose at least ten matched workflow runs per option across representative changes; report cold/warm caches, queue time, failures and sample size. Ten is a pilot starting point, not statistical proof. Use equal control objectives, retention and service revisions; document unavoidable differences.
4. **Evidence pack:** retain source revisions, CI configuration, runner/image digests, job links, reports, timestamps, operator time logs, quotes, and the completed cost model. Use redacted, authorised records and an agreed retention/access policy.
5. **Review:** separate technical outcomes, operational burden, and commercial implications. Report inconclusive metrics honestly. Production change-failure rate or recovery claims require representative production data; this non-production pilot cannot establish them.

## Explicit decision rules

**Recommend GitLab** only if mandatory criteria pass, buyer-prioritised improvements are evidenced, full cost/change risk is acceptable, and the accountable buyer approves the case. **Retain GitHub** when it meets the need and switching lacks a justified incremental benefit. **Extend narrowly** when a named missing fact could change the decision; specify its owner, budget, and deadline. **Stop/defer** when there is no validated pain, sponsor, safe scope, or economic case.

Suggested close: “Would it be useful to agree one service, the evidence you need, and a decision meeting? If your current setup meets those criteria more economically, my recommendation would be to keep it.” No meeting, outreach, purchase, or deployment has been arranged.
