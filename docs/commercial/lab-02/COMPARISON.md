# Balanced competitive evaluation

Desk research checked 25 October 2026. This is a requirements-led discussion, not a platform ranking or equivalent hosted benchmark. IDs map to the [dated source register](SOURCE_REGISTER.md).

| Decision dimension | GitLab: documented capability | GitHub: documented capability | Discovery question and evidence to request |
| --- | --- | --- | --- |
| Pipeline model | Root `.gitlab-ci.yml` expresses stages, jobs, and execution conditions. [S1](https://docs.gitlab.com/ci/) | YAML files in `.github/workflows` express event-triggered jobs and steps. [S2](https://docs.github.com/en/actions/get-started/understand-github-actions) | Which repeated maintenance or approval task is painful? Inspect one current pipeline and its owner; syntax alone is not value. |
| Execution | Jobs run on runners, including hosted and customer-managed options. [S1](https://docs.gitlab.com/ci/) | Hosted Linux/Windows/macOS and self-hosted runners are documented. [S2](https://docs.github.com/en/actions/get-started/understand-github-actions) | What OS, isolation, network access, capacity, and operating responsibility are required? Record specifications and costs for both pilot options. |
| Security | Documented capabilities cover code, dependencies, images, and runtime; feature-specific entitlements differ. [S3](https://docs.gitlab.com/user/application_security/) | Dependency tools, Code Security, and Secret Protection provide credible integrated options with visibility/plan differences. [S4](https://docs.github.com/en/code-security/getting-started/github-security-features) | Which controls, findings workflow, exception ownership, and retention are mandatory? Complete the checklist below. |
| Commercial assessment | Request a current quote scoped to the required configuration and entitlements. | Plans, subscriptions, and metered usage can all affect the bill. [S5](https://docs.github.com/en/billing/get-started/how-billing-works) | What is already committed, what can actually be retired, and when? Compare a common horizon with migration/training costs. |
| Change and adoption | **Fit hypothesis:** a common delivery/evidence workflow may reduce a specific coordination burden. | **Fit hypothesis:** retaining an established GitHub workflow may avoid disruption and duplicate tooling. | Which hypothesis survives a measured pilot? Establish ownership, switching risk, and an explicit retain-current-platform option. |

The fit hypotheses are analysis. Neither vendor documentation nor Lab 01 demonstrates a buyer-specific productivity, security, or financial advantage.

## Entitlement checklist: feature-level, not tier-level slogans

These are selected checks, not an exhaustive procurement matrix. **Buyer confirmation remains pending in every row.** No paid feature in this table was exercised by this portfolio.

| Required feature to confirm | Dated documentary check | Buyer validation before a pilot |
| --- | --- | --- |
| GitLab basic versus advanced SAST | Basic open-source analyzer/report capabilities span Free/Premium/Ultimate; advanced cross-file analysis and the richer management/MR features in the feature table require Ultimate. [S6](https://docs.gitlab.com/user/application_security/sast/#features) | AppSec: supported language/analyzer, desired UI, hosting/version, and written entitlement |
| GitLab dependency scanning product | The dependency-scanning page identifies Ultimate. [S7](https://docs.gitlab.com/user/application_security/dependency_scanning/) | AppSec/procurement: required SBOM workflow and quoted entitlement; distinguish it from external pip-audit |
| GitLab container scanner artifacts versus UI | Basic scanning/report artifacts span the listed tiers; richer security/MR presentation in the feature table requires Ultimate. [S8](https://docs.gitlab.com/user/application_security/container_scanning/#features) | Platform/AppSec: exact artifact, presentation, remediation, and retention requirements |
| GitLab vulnerability-management report | The consolidated vulnerability report identifies Ultimate. [S9](https://docs.gitlab.com/user/application_security/vulnerability_report/) | AppSec: verify workflow in an authorised evaluation; generic CLI JSON is insufficient evidence |
| GitHub baseline dependency tooling | Dependency graph and Dependabot capabilities are described among features available across plans, subject to repository/feature details. [S4](https://docs.github.com/en/code-security/getting-started/github-security-features) | Platform: supported ecosystem, visibility, enablement, and current configuration |
| GitHub paid code/secret security | Private/internal use of the relevant advanced products requires the appropriate purchase and eligible plan; some public-repository features are free. [S10](https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security) | Procurement/AppSec: account plan, repository visibility, exact feature and purchased product; do not assume public availability transfers to private repositories |

Do not infer “GitHub has no integrated security”, “all GitLab security is free”, or “GitLab is always cheaper”. Lab 01 ran **external CLI tools inside GitLab CI**. It did not establish paid-product equivalence, a native security-dashboard integration, or that either platform detects every vulnerability.

## Decision logic

Recommend GitLab when measured outcomes, required capabilities, acceptable migration risk, and a complete commercial assessment support it. Retain GitHub when it meets the requirements and the incremental case for switching is weak. Choose a bounded further evaluation when material evidence is missing; do not convert unknowns into a recommendation. Use the [pilot scorecard](PILOT_SCORECARD.md) and [cost model](COST_MODEL.md).
