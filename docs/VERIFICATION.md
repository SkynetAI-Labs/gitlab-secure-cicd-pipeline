# Verification record

Local verification on 25 October 2026. Machine-readable results and verified source-file SHA-256 hashes are in [verification-summary.json](evidence/verification-summary.json). Raw local reports are retained under ignored `reports/`; CI is configured to retain corresponding artifacts when it can run.

| Check | Observed result |
| --- | --- |
| Ruff lint and formatting | Passed for application, tests, and verification scripts |
| API and policy tests | 52 passed; 100% statement and branch coverage; 95% minimum enforced |
| Bandit application scan | No findings |
| Runtime and CI dependency audits | No known vulnerabilities returned by pip-audit at verification time |
| Dependency installation | SHA-256-locked CI/runtime dependencies installed successfully |
| Gitleaks full Git history and current tree | No findings; redacted reporting enabled |
| Negative controls | Synthetic token and unsafe subprocess each rejected with exit code 1; temporary fixtures removed |
| Package build | Wheel and source distribution built; SHA-256 checksums and CycloneDX SBOM generated |
| Container build and runtime | Passed; numeric UID 10001, read-only filesystem, all capabilities dropped, no-new-privileges |
| Container black-box tests | Health, allow/block decisions, and invalid input passed |
| Trivy image scan | Final Alpine runtime: zero HIGH/CRITICAL findings with no suppressions and no ignore-unfixed flag |
| GitLab static CI lint | Valid, no errors or warnings |
| GitLab hosted pipeline | Not verified: account identity verification required by GitLab before CI jobs can run |

The initial Debian image was correctly rejected with 48 HIGH findings across OS packages and bundled Python packaging components. It was replaced with the official digest-pinned Alpine base, and pip/ensurepip were removed from the runtime image. The hardened image passed the unchanged gate; this was remediation, not an exception.

The build network inside Docker could not resolve PyPI locally. A one-off `docker build --network host` succeeded; no resolver, firewall, daemon configuration, or host security setting was changed. CI uses its runner's normal build network.

Trivy warned that third-party SBOM metadata can affect detection. Scans reflect their database and package-detection coverage at a point in time, not a guarantee of security. No production deployment, regulatory certification, external penetration test, or realised commercial saving is claimed.

## Reproduce

Run `sh scripts/verify.sh` in a Python 3.14 environment installed from `requirements-ci.lock`. With Gitleaks v8.30.1 on PATH, run `python scripts/test_controls.py` and the Gitleaks commands from `.gitlab-ci.yml`. Build the container, run `scripts/smoke.py` against it, and run the pinned Trivy image command from CI. Reports are generated locally; do not commit sensitive scan artifacts.

## Publication verification

The verified implementation was published at commit `7e036848013fd5192ad25f6996b2638443ee6b9f`. Subsequent commits document publication and verification; the tested implementation is identified by the source-file hashes in the evidence summary.

- [GitLab canonical project](https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline).
- [Separate GitHub mirror](https://github.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline). HTTP 404 was confirmed before creating this public repository; it was checked as empty and writable before the first push. Lab 03 was not changed.
- Both public README pages returned HTTP 200 in Chromium. Their relative-path banner loaded at its expected natural dimensions of 1800 × 640 pixels, rendered at 763 × 271 on GitLab and 838 × 298 on GitHub in the verification viewport. The banner uses the exact requested title and the label “Independent Portfolio Project”. See [rendering evidence](evidence/readme-rendering.json). Cropped browser screenshots are retained locally under ignored `reports/`.
- [GitLab pipeline 2985772695](https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline/-/pipelines/2985772695) failed before creating jobs; static CI lint reports no YAML errors. A fresh pipeline simulation returned `Identity verification is required in order to run CI jobs`. This is an account-level blocker, so no hosted job success is claimed.

The owner must complete **Verify my account** in GitLab's alert banner and then start a new `main` pipeline. Follow only the identity checks requested in GitLab itself. See [operations](OPERATIONS.md#current-hosted-ci-blocker-account-identity-verification) and [GitLab's official instructions](https://docs.gitlab.com/ci/debugging/#error-identity-verification-is-required-in-order-to-run-ci-jobs). Runner-specific behavior can only be verified after that blocker clears. No registry image was pushed and no production deployment was performed.
