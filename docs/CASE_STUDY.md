# Commercial case study: evidence-led secure delivery

## Scenario and buyer

This is a portfolio demonstration for a small SaaS or fintech engineering team delivering a Python service. It is not a customer engagement. The economic buyer is a CTO or engineering director; platform engineering owns delivery, security owns risk policy, and procurement needs reviewable evidence of controls.

The problem: manual checks and loosely controlled release steps make it difficult to show which commit was tested, what dependency risk was known at release time, or why a release was blocked. This project turns those checks into repeatable gates and retained evidence.

## Delivered capability

| Buyer concern | Engineering deliverable | Evidence | Commercial implication |
| --- | --- | --- | --- |
| Releases break predictable input cases | Strict API boundary and policy tests | JUnit and branch coverage | Less repeated manual checking; no claim of fewer real incidents |
| Vulnerable or substituted dependencies | Version/hash locks, dependency audit and SBOM | Locked graph, advisory JSON, CycloneDX | Faster component inventory and vendor review |
| Credentials enter the repository | Redacted full-history/tree secret scanning | Scanner exit status and redacted report | Earlier detection; not proof that secrets cannot leak |
| Unsafe images reach the registry | Non-root runtime, smoke checks, HIGH/CRITICAL image gate | Image report and commit-tagged archive | Reviewable release candidate before manual delivery |
| Audit narrative differs from implementation | Documentation tied to source and actual checks | Verification record and pipeline/job links | More credible security questionnaires without claiming certification |

## Illustrative economics, not measured savings

Assume 20 releases/month, 30 minutes of manual verification/release, 10 minutes of review after automation, and £75/hour loaded engineering cost. Gross capacity returned would be `20 × (30−10)/60 = 6.67 hours/month`, or approximately £500/month. If maintenance takes 2 hours/month and runner/storage costs are £40/month, illustrative net capacity value is `£500 − £150 − £40 = £310/month`.

At an assumed 24-hour implementation effort (£1,800 at the same rate), simple payback would be approximately 5.8 months. At only 5 releases/month, gross capacity value falls to £125 and the same monthly overhead exceeds it. This is a decision model, not a quote, ROI guarantee, observed labour saving, or revenue claim. It excludes opportunity cost, onboarding, incident losses, and commercial margin.

## Discovery and success criteria

Before pricing an engagement, establish release frequency, manual effort, current failure rate, runner availability, risk appetite, and evidence retention requirements. Pilot one service and compare at least a month of baseline and pilot data: manual touch time per release, pipeline duration/cost, false-positive triage, failed deployments, and mean recovery time. Treat change failure rate and recovery measures as future production metrics, not results from this lab.

Acceptance: a reproducible test run, a deliberately rejected unsafe fixture, clear ownership of dependency exceptions, an image scan at the release commit, and a reviewed operator release step. Public portfolio evidence should omit credentials and customer-sensitive reports.

## Adoption and limitations

Start with one repository, agree gate policy, protect branches and CI variables, train maintainers, then add signing, provenance verification, scheduled rescans, authenticated runtime access, and production approval integration. This lab does not demonstrate regulatory compliance, penetration-test assurance, customer adoption, or a production deployment. Scanner and runner limitations belong in the sales conversation and verification record.
