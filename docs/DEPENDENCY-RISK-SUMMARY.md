# Dependency Risk Summarizer v0.1

Status: **IN PROGRESS reference implementation**

Roadmap mapping: `P-060 Dependency Risk Summarizer`, with reuse by `P-041 Repository Health Auditor`, `P-046 Security Hygiene Reviewer`, and future update/release assistants.

## Search-before-build: OSV remains the scanner

Google's OSV-Scanner already detects known vulnerabilities across package ecosystems using OSV.dev data and can emit JSON, SARIF and human-readable formats. This project does **not** recreate vulnerability matching, advisory databases or dependency extraction.

Instead, `tools/osv_summary.py` is a small downstream presentation adapter for existing `osv-scanner scan --format json` output. Its job is to make results easier to explain without leaking unnecessary local filesystem details.

## Why a separate summary layer?

Raw scanner results are optimized for engineering detail. Beginner-safe troubleshooting and AI-assisted repository review often need a smaller contract:

- how many affected package records are present;
- how many normalized advisory groups are represented;
- which ecosystems/packages/versions are affected;
- which public advisory IDs belong to each alias group;
- which lockfile/SBOM basename produced the record;
- an explicit reminder that "zero findings" is not a guarantee of safety.

OSV-Scanner groups advisories that alias one another. This adapter prefers those `groups` so one underlying vulnerability published under several IDs is not automatically double-counted.

## Privacy boundary

The adapter does not perform a network scan. It reads only a user-supplied OSV JSON file.

The output intentionally drops:

- absolute source paths (only the source filename is retained);
- full advisory bodies/details;
- environment values;
- credentials;
- arbitrary scanner metadata not required for the summary.

Do not publish raw scanner reports from private repositories without reviewing them: OSV JSON can contain absolute local paths and dependency details.

## Usage

Generate a JSON report using the official scanner, then summarize it locally:

```bash
osv-scanner scan --format json your/project > osv-report.json
python tools/osv_summary.py --input osv-report.json
```

The first command belongs to OSV-Scanner. The second command performs a deterministic local transform only.

## Evidence semantics

A result with no advisory groups means:

> The supplied OSV-Scanner report contains no known vulnerability groups for what it successfully scanned.

It does **not** mean:

> This repository has no security vulnerabilities.

A positive result also does not authorize automatic dependency upgrades. Version changes can introduce breaking behavior, remove platform support or require migrations. Remediation should identify the upstream fix, test the proposed version, preserve rollback and verify the application afterward.

## Completion gaps

`P-060` remains **IN PROGRESS**. Completion requires direct integration with a pinned OSV-Scanner workflow/CLI, representative multi-ecosystem fixtures, severity/fix-availability normalization with stable schema provenance, accessible beginner UI, multilingual review, remediation/runbook integration, version/release evidence, known limitations and canonical completion evidence.
