# Operations and release runbook

## Verification

Install the locked CI toolchain in a Python 3.14 virtual environment and run `sh scripts/verify.sh`. It runs lint, format, tests with a 95% branch-inclusive coverage floor, Bandit, runtime/tooling advisory audits, SBOM generation, and wheel/source packaging. Gitleaks and container scans are separate container commands in `.gitlab-ci.yml`.

For lock updates, use pip-tools 7.6.2 on Python 3.14:

```bash
pip-compile --generate-hashes --strip-extras -o requirements.lock requirements.in
pip-compile --allow-unsafe --generate-hashes --strip-extras -o requirements-ci.lock requirements-ci.in
```

Review dependency diffs, re-audit, and rerun the tests. `requirements.in` and `pyproject.toml` must describe the same runtime dependency policy. CI installs lock files with `--require-hashes`. Builds use the locked installed build backend with `--no-isolation`.

## Runner prerequisites

Use an isolated Docker executor with TLS-enabled Docker-in-Docker, privileged service support, and a shared `/certs/client` volume. Compatible GitLab hosted Linux runners support this; account verification, compute minutes, and image/artifact limits may still prevent jobs. Validate those prerequisites without weakening host security. The application container itself runs without privileges.

Registry publishing requires the existing project's registry, a protected default branch, a successful full pipeline, and an operator choosing the manual `publish_image` job while the one-day image artifact is still available. Rerun the pipeline if that archive expires. Do not print environment variables or registry credentials.

## Release and recovery

1. Review source changes and scanner evidence at an exact commit SHA.
2. Run the full pipeline and inspect all required job results.
3. Optionally publish the scanned image via the manual job. It tags the commit SHA and does not deploy.
4. Record the registry digest externally before a downstream deployment. Signing and provenance attestations are future work.
5. Roll back a downstream environment to its previously approved digest; there is no environment to roll back in this lab.

The GitHub repository is a source mirror. Publishing there does not verify GitLab runners or constitute a deployment. Never force-push or use `git push --mirror` against an existing repository. Fetch and review divergent history before any update.

## Resolved hosted-CI prerequisite: account identity verification

GitLab previously rejected pipeline creation with `Identity verification is required in order to run CI jobs`, before creating any jobs. The owner completed identity verification in GitLab, then [pipeline 2985809359](https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline/-/pipelines/2985809359) passed on `main`. All seven required jobs succeeded without application or pipeline configuration changes. Hosted Docker-in-Docker, container smoke checks, and image scanning are now exercised successfully. The optional registry job remains manual.

If another account encounters the same error, sign in to GitLab, select **Verify my account** in the alert banner, complete only the checks requested in GitLab's own UI, and start a new pipeline. Never share identity details, payment information, one-time codes, or credentials in chat. See [GitLab's official troubleshooting instructions](https://docs.gitlab.com/ci/debugging/#error-identity-verification-is-required-in-order-to-run-ci-jobs). No account or host security setting was weakened to bypass verification.
