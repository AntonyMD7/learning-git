# Secret Hygiene — Upstream Gitleaks Integration

Status: **IN PROGRESS**

Roadmap mapping: `P-049 Secret-Exposure Detection Action`, with reuse by `P-046 Security Hygiene Reviewer` and other public-repository templates.

## Decision: adopt instead of rebuild

Gitleaks is a mature secret-detection engine that scans Git repositories/history for patterns associated with hardcoded credentials and tokens. This repository adopts the maintained Gitleaks Action instead of implementing an ad-hoc regex scanner that would provide weaker coverage and a false sense of security.

The workflow pins **Gitleaks Action v3.0.0** to commit:

```text
e0c47f4f8be36e29cdc102c57e68cb5cbf0e8d1e
```

The v3 action uses the Node 24 runtime. Its upstream documentation states that personal-account repositories do not require a Gitleaks license key; organization-owned repositories have a different license-key requirement, so this workflow must not be copied blindly across ownership models.

## Workflow boundary

`.github/workflows/secret-hygiene.yml`:

- runs for pull requests and pushes to `main`;
- checks out full Git history so removed-but-still-historical leaks can be detected;
- grants only `contents: read` at workflow level;
- uses only GitHub's ephemeral `GITHUB_TOKEN` required by the action;
- disables PR commenting;
- disables SARIF/artifact upload in this minimal integration;
- has a five-minute job timeout;
- makes no repository mutation.

The scanner runs inside GitHub Actions. No custom secret value is passed to the scanner.

## Evidence semantics

A passing Gitleaks scan means the configured engine did not detect a secret pattern in the scanned history at that revision. It does **not** prove that no secret exists: detection rules have false negatives, encoded/novel credential formats may evade pattern matching, and sensitive non-credential data is outside scope.

A finding also does not prove malicious exposure; maintainers must inspect it carefully without copying the suspected secret into public issues or logs.

## Incident rule

If a real secret is found, deleting the text in a later commit is insufficient because the value remains in Git history and may already have been copied. The correct containment sequence is generally:

1. stop publishing or re-sharing the value;
2. revoke/rotate the credential at its authority;
3. determine exposure scope;
4. decide whether history rewriting is warranted;
5. verify the new credential is not committed;
6. record sanitized incident evidence without reproducing the secret.

This repository's public workflow does **not** rotate credentials or rewrite history automatically.

## Beginner interpretation

> The repository automatically checks its Git history for common patterns that look like accidentally committed passwords, tokens or keys. A pass is useful evidence, but it is not a guarantee that every possible secret is absent.

## Privacy and safety

Secret scanners require access to repository content by definition. Therefore this integration is suitable for this public repository, where the scanned content is already public. Before using the same pattern in a private or regulated repository, review data-handling, runner and licensing requirements separately.

## Completion gaps

`P-049` remains **IN PROGRESS**. Completion requires a reusable public template, representative positive/negative fixtures without real credentials, false-positive handling guidance, incident-response integration, multi-repository acceptance, accessibility/multilingual documentation, version/release evidence, known limitations and canonical completion evidence.
