# License Compliance Checker — Licensee Adapter v0.1

Status: **IN PROGRESS upstream-adoption implementation**

Canonical roadmap mapping: `P-056 License Compliance Checker`, with reuse by `P-039 GitHub Repo Doctor`, `P-041 Repository Health Auditor`, and public-project release gates.

> **Canonical-ID correction:** an earlier draft of this branch called this work `P-050 Open-Source License Checker`. The master roadmap defines `P-050` as **Evidence Validation Action** and `P-056` as **License Compliance Checker**. This document preserves the master roadmap's stable IDs and uses `P-056`.

## Search-before-build: Licensee remains the detector

The maintained [`licensee/licensee`](https://github.com/licensee/licensee) project already detects project licenses by matching license files and package metadata against known licenses. This repository therefore adopts Licensee rather than building another text-similarity license detector.

The CI integration pins the released Licensee gem to **v10.1.0**. Upstream documents `licensee detect [PATH] --json` as machine-readable output for programmatic consumers.

`tools/licensee_summary.py` is only a presentation/privacy adapter. It extracts detected public license identifiers and matched-file basenames while dropping license text and absolute paths.

## Advisory mode is deliberate

This repository does not yet have an owner-ratified open-source license. The roadmap completion contract requires an explicit license decision, but software should not choose a legal license on the owner's behalf.

Therefore `.github/workflows/license-hygiene.yml` captures Licensee's result and reports it **without automatically failing solely because no license is detected**. This allows the checker itself to be tested while preserving the unresolved license decision as a visible release/completion gate.

A future reusable policy layer may choose to enforce `license detected == true` for repositories whose owners have already established that requirement.

## Evidence semantics

A detected SPDX/license identifier means Licensee found evidence it recognizes in the project. It does **not** prove:

- that every file in the repository is covered by that license;
- that vendored/dependency code uses the same license;
- that the chosen license is suitable for the project;
- that attribution/notice obligations have been satisfied;
- that use, redistribution, patents or trademarks are legally permitted in a specific situation.

No detected license is even more important to interpret carefully: absence of a detected license is **not permission** to copy, modify or redistribute code.

This project provides technical repository-hygiene information, not legal advice.

## Privacy and workflow boundary

The public workflow:

- checks out the public repository with `contents: read` permission;
- installs exactly Licensee gem v10.1.0 into an ephemeral runner-local gem directory rather than mutating system Ruby locations;
- scans the local checkout rather than a private remote;
- supplies no custom credential or repository token to Licensee;
- stores the raw report only in the ephemeral runner `/tmp` directory;
- publishes no raw license file content or absolute path;
- performs no repository mutation.

## Beginner interpretation

If the summary says a license was detected:

> "The repository contains license information that Licensee recognizes. Read that license and the project's notices before reusing the code."

If it says no license was detected:

> "No recognized project license was found. Do not assume the code is free to reuse. The project owner still needs to make an explicit licensing decision."

## Completion gaps

`P-056` remains **IN PROGRESS**, not COMPLETE. Completion requires an owner-approved reusable enforcement policy, positive/negative/multiple-license fixtures against real Licensee JSON, explicit handling of package/dependency licenses and notices, wider repository acceptance, accessibility/multilingual documentation, version/release evidence, known limitations and a canonical completion record.
