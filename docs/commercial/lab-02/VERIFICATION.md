# Lab 02 verification and presentation readiness

Scope: the Lab 02 presentation and evaluation toolkit. Lab 01's source, CI, locks, evidence, case study, and original banner are preserved. Only portfolio navigation is added to the main README; the setup handover receives an appended continuation record.

## Content and local checks

- Read the continuation brief, setup handover, Lab 01 verification, and existing documentation before authoring. Reused the original scenario and linked the existing economic example rather than presenting it as new buyer evidence.
- Checked the ten selected primary-source pages and their specific feature/tier distinctions. Retrieval dates and claim limits are in [SOURCE_REGISTER.md](SOURCE_REGISTER.md). Documentary availability is kept separate from executed tests.
- Reviewed the competitive comparison, discovery/objection cards, pilot decision rules, and hiring-team walkthrough for unsupported security, pricing, customer, or commercial-result claims.
- Authored Lab 02's banner from the established SVG visual system; retained its exact title, portfolio label, purple/black/white palette, editable SVG, and portable 1800 × 640 PNG.
- Inspected spreadsheet formulas, input validation, empty-input safeguards, cached example outputs, and an independent arithmetic calculation. The Low/Base/High sheets are blank; incomplete options do not produce numeric totals. Inspected 45 blank CSV input rows. Confirmed no workbook macros or external data relationships.
- Reviewed local links/anchors, external source reachability, the scoped diff, Lab 01 preservation, and redacted secret scans before publication. Machine-readable outcomes are recorded in [verification.json](verification.json).

## Completed publication checks

- Published Lab 02 to the existing [GitLab project README](https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline/-/blob/main/docs/commercial/lab-02/README.md) and [GitHub mirror README](https://github.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline/blob/main/docs/commercial/lab-02/README.md). No remote repository was created and GitHub Lab 03 was not touched.
- Chromium followed the new main-README navigation to Lab 02 on both platforms. Both root pages returned HTTP 200, the original Lab 01 banner remained present, and the exact new title and workbook link rendered.
- Both Lab 02 banners loaded at their expected natural dimensions of **1800 × 640**. At a 1440 × 1000 browser viewport, GitLab displayed the banner at 765 × 272 and GitHub at 1012 × 360. Cropped screenshots were visually reviewed and retained locally under ignored `reports/`.
- Downloaded the published banner PNG and workbook from both platforms and compared SHA-256 hashes with the verified local files: all four matched.
- [Pipeline 2986537496](https://gitlab.com/SkynetAI-Labs/gitlab-secure-cicd-pipeline/-/pipelines/2986537496) passed for publication commit `f3a9d7b1badaa80aa73e3c48ae8ac7f77485f7cd`, with all seven required jobs successful. Hosted JUnit/Cobertura artifacts confirm **52 passing tests**, no failures/errors/skips, and **100% line and branch coverage**. The hosted image report contains **zero HIGH/CRITICAL findings**. Optional registry publication remained manual; no deployment was performed.
- Compared every existing Lab 01 file with successful baseline commit `6a6f51c7c26bb6bd5471a900b71b7e44148d8b67`: its 24 other tracked files remain byte-for-byte unchanged. Main README changes are confined to lab navigation; the original handover is preserved with appended continuation notes. Lab 01's CI configuration, application, tests, locks, evidence, case study, and assets were not replaced.

The machine-readable record includes browser results, source-link status, download hashes, preserved-file hashes, workbook checks, and hosted evidence. Subsequent verification-record-only commits do not change Lab 01's implementation. Final publication also confirms both remote `main` branches match and the checkout is clean.

## Remaining evaluation gaps

No buyer discovery, procurement quote, paid GitLab/GitHub security-product trial, controlled cross-platform benchmark, or customer pilot was conducted. Scorecard thresholds are proposals. Workbook formulas and example caches were inspected and arithmetic checked independently; live recalculation in Microsoft Excel or LibreOffice was not performed. A buyer should review and recalculate the workbook in their chosen spreadsheet application before use.

This is an independent portfolio presentation, not a customer result or GitLab endorsement. No recruiter or prospect was contacted, no hiring contact was named, and no deployment or optional registry publication was performed.
