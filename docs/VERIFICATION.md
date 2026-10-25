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

Publication URLs, exact source commits, hosted pipeline status, and cross-platform banner rendering are recorded after publication. The GitHub destination is awaiting the owner's choice; do not substitute an unrelated existing project.
