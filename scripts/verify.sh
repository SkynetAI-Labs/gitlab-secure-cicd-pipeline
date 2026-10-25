#!/bin/sh
set -eu
mkdir -p reports
ruff check src tests scripts
ruff format --check src tests scripts
pytest
bandit -r src -f json -o reports/bandit.json -q
pip-audit --require-hashes -r requirements.lock --format json --output reports/dependency-audit.json
pip-audit --require-hashes -r requirements-ci.lock --format json --output reports/tooling-audit.json
pip-audit --require-hashes -r requirements.lock --format cyclonedx-json --output reports/sbom.cdx.json
python -m build --no-isolation
sha256sum dist/* > reports/SHA256SUMS
