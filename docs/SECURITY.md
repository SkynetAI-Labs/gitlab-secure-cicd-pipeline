# Threat model and security boundaries

## Assets and trust boundaries

Assets: source history, CI job credentials, dependency locks, build artifacts, registry images, and evidence. Untrusted input crosses HTTP, dependency registries, merge requests, and scanner databases. The API is a demonstration policy evaluator; client assertions are not authenticated scan evidence.

| Threat | Implemented control | Remaining limit |
| --- | --- | --- |
| Malformed or excessive input | Exact schema, strict types, bounded counts, 4 KiB body limit, generic protocol errors | Gateway rate limiting and TLS remain deployment responsibilities |
| Secret committed to source | Full-history and tree Gitleaks scans with redaction | A scanner cannot detect every secret; rotate exposed credentials rather than relying on deletion |
| Unsafe Python implementation | Bandit and negative-control detection test | Static analysis is incomplete; review remains necessary |
| Vulnerable dependencies | Hash-locked runtime/tooling dependencies, pip-audit gates, Trivy image gate | Advisory feeds can lag; rerun scans and update locks/base images regularly |
| Dependency substitution | SHA-256 package hashes and pinned Python base digest | Hashes verify approved bytes, not maintainer integrity; scanner images also require review |
| Container compromise | Numeric non-root UID, no capabilities, read-only runtime test, tmpfs, no-new-privileges | Kernel isolation and runner security are external dependencies |
| Unverified release | Staged gates, commit-tagged image, manual publication on protected default branch | No signing or attestation verification yet; no production deployment configured |
| Pipeline credential theft | No secrets in files/logs; registry password uses stdin and ephemeral CI credentials | Pipeline editors can exfiltrate secrets; restrict protected runners, branches, and variables |

Medium/low application findings are permitted by the demonstration API. The CI dependency audit blocks every known vulnerability returned by pip-audit; image scanning blocks HIGH/CRITICAL, including unfixed findings. These are separate policies, explicitly documented rather than silently conflated.

## Handling findings

A failed scanner or advisory-service outage blocks progress. Do not introduce `allow_failure`, `--exit-code 0`, broad suppressions, or ignore-unfixed flags to make the build green. Review the advisory and update dependencies or the base digest. Any exception needs an owner, scope, rationale, expiry, and compensating control documented in review. None are pre-approved.

CI report retention is 7 days for redacted secret reports, 14 days for other verification evidence, and 1 day for the intermediate image archive. Download required evidence before expiry. Native JSON scanner outputs are generic artifacts; the project does not claim GitLab Ultimate vulnerability-dashboard integration.

## Out of scope

Production authentication, scanner evidence signatures, distributed rate limiting, cloud deployment, penetration testing of third-party targets, compliance certification, and incident response automation. No external target is attacked. Synthetic negative-control data is generated in a temporary directory and removed after testing.
