# Upstream Repository Hygiene Integrations

Status: **IN PROGRESS**

Roadmap mapping: `P-048 Broken-Link Scanner Action`, with architectural reuse by `P-039`, `P-041`, `P-044`, and later repository-maintenance projects.

## Decision: adopt instead of rebuild

The public roadmap requires search-before-build. Broken-link scanning already has a mature open-source implementation in [Lychee](https://github.com/lycheeverse/lychee) and a maintained [Lychee GitHub Action](https://github.com/lycheeverse/lychee-action). This repository therefore adopts that engine instead of creating a weaker bespoke HTTP crawler.

The integration uses [Lychee Action v2.9.0](https://github.com/lycheeverse/lychee-action/releases/tag/v2.9.0) pinned to commit:

```text
e7477775783ea5526144ba13e8db5eec57747ce8
```

The pinned release provides Lychee 0.24.x-era support and its upstream documentation recommends fixed-version/SHA pinning for stronger workflow supply-chain control.

## Workflow boundary

`.github/workflows/link-health.yml`:

- runs on pull requests and pushes to `main`;
- has read-only repository contents permission;
- scans Markdown documents;
- fails when broken links are found;
- has a five-minute job timeout;
- does not receive a custom credential or personal access token;
- does not modify repository contents.

The check necessarily makes outbound HTTP requests to links present in public Markdown. Therefore it is appropriate for this **public** learning repository but should not automatically be copied into repositories whose documentation contains confidential or private endpoints.

## Evidence semantics

A passing Lychee job means only that the links checked in that run satisfied the configured HTTP/link rules. It does not prove that linked content is trustworthy, safe, accurate, licensed correctly, or semantically unchanged.

A failed external request can also reflect rate limiting or temporary remote downtime rather than a permanently broken link. Maintainers should inspect the evidence before editing or removing a reference.

## Beginner interpretation

> The project automatically checks whether links in its documentation still open. If the check fails, a maintainer reviews the failing link before changing the documentation.

## Security and privacy review

- no repository write permission;
- no custom secrets supplied;
- third-party action pinned to a reviewed release commit;
- public Markdown only in this repository;
- bounded timeout and retry count;
- no automatic link rewriting or content replacement.

## Completion gaps

`P-048` remains **IN PROGRESS**, not COMPLETE. Portfolio completion still requires a reusable/documented distribution path for other public repositories, representative real-world acceptance, handling guidance for transient/rate-limited sites, accessibility/multilingual documentation, version/release evidence, known limitations and a canonical completion record.
