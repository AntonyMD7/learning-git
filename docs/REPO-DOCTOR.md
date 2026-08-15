# Repository Doctor — Public Reference v0.1

Roadmap mapping:

- `P-039 GitHub Repo Doctor` — **IN PROGRESS**
- `P-041 Repository Health Auditor` — **IN PROGRESS**
- `P-044 Documentation Quality Assistant` — **IN PROGRESS** baseline
- `P-046 Security Hygiene Reviewer` — **IN PROGRESS** baseline
- `P-047 README Linting Action` — **IN PROGRESS** local-check baseline
- `P-058 Dangerous-Script Detector` — **IN PROGRESS** conservative marker baseline
- `P-059 Read-Only vs Mutation Classifier` — **IN PROGRESS** baseline
- `P-060 Dependency Risk Summarizer` — **ADOPT/INTEGRATE**, not rebuilt here

Related roadmap projects deliberately delegated to mature upstream tools:

- `P-048 Broken-Link Scanner Action` — prefer **Lychee** / an equivalent established link checker;
- `P-049 Secret-Exposure Detection Action` — prefer **Gitleaks** / equivalent established secret scanners;
- dependency vulnerability scanning — prefer **OSV-Scanner** / ecosystem-native scanners;
- GitHub Actions linting — prefer **actionlint**;
- shell analysis — prefer **ShellCheck**;
- general multi-language lint orchestration — evaluate **Super-Linter** before duplicating it.

This is the roadmap's **search-before-build** rule in practice: build a beginner-safe orchestration/explanation gap, but do not write weaker substitutes for mature scanners.

## What `repo_doctor.py` does

The v0.1 tool audits a local repository without executing repository code. It checks for:

- README presence and a minimal substance signal;
- explicit license file;
- security policy;
- contribution guidance;
- beginner `START-HERE` path;
- GitHub Actions workflow presence;
- a small set of potentially dangerous command markers in workflow/script/tool text;
- whether recommended external scanners are already available on `PATH`.

The output has both a short beginner explanation and a structured JSON form.

## What it does not do

It does **not**:

- install dependencies or scanners;
- execute scripts from the target repository;
- follow network links;
- read or print credential values;
- report file contents;
- claim a missing file is automatically a defect;
- claim a matched command marker is automatically a vulnerability;
- rewrite documentation or workflow files.

## Risk-marker semantics

A match such as `rm -rf`, `git reset --hard`, a force push, a privilege-changing command, or a download command is emitted as:

`REVIEW_REQUIRED_NOT_PROOF_OF_VULNERABILITY`

Context matters. A safety document may legitimately contain a dangerous command as an example of what **not** to do. Automated classification therefore stops at review rather than accusing a project of being unsafe.

## Beginner interpretation

The tool should say what needs attention without requiring the user to understand repository internals. Example:

> The read-only repository check finished; no files were changed. Review these project-hygiene areas: license and security policy. Two potentially risky command markers need context review; these are not automatically vulnerabilities.

## Engineer interpretation

`--json` exposes the exact check names, evidence paths, tool-discovery state, risk-marker categories, privacy declarations, mutation declarations and known limitations.

## Security and privacy

The report intentionally excludes file contents, environment values and secret values. Repository-provided commands are never executed. The tool itself performs no network request.

For actual secret detection, use a dedicated scanner designed for that task. Do not attempt to infer secret values with ad-hoc regular expressions in this project.

## Completion gaps

No mapped roadmap item is COMPLETE. A completion-grade Repo Doctor still needs:

- its own public distribution surface/package;
- explicit license decision for that distribution;
- richer repository-type detection;
- safe integrations with upstream scanners;
- SARIF or equivalent interoperable finding export;
- issue/PR presentation modes;
- accessibility and multilingual acceptance;
- real-world evaluation across a diverse corpus of public repositories;
- documented false-positive/false-negative behavior;
- release/tag and canonical completion evidence.
