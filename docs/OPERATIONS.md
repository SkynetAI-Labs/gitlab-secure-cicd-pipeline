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

## Current hosted-CI blocker: account identity verification

GitLab static CI lint passes, but pipeline simulation returns `Identity verification is required in order to run CI jobs`. Published pipeline [2985772695](https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline/-/pipelines/2985772695) failed before creating any jobs; it has no YAML errors. This establishes an account-level pipeline-creation blocker; hosted job behavior has not yet been exercised.

Sign in to GitLab as `SkynetAI-Labs`, open the project/pipeline, and select **Verify my account** in the alert. Complete only the email, phone, or payment-method verification GitLab requests in its own UI. Do not send identity details, one-time codes, payment information, or credentials through chat. After verification, create a new pipeline for `main` from **Build > Pipelines > New pipeline** and inspect all required jobs. See [GitLab's official troubleshooting instructions](https://docs.gitlab.com/ci/debugging/#error-identity-verification-is-required-in-order-to-run-ci-jobs). No account/security settings have been weakened to bypass this requirement.
