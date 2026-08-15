#!/usr/bin/env python3
"""Repository Doctor v0.1.

A local, read-only repository health explainer. It audits public-project hygiene
without executing repository code, opening secret values, rewriting files, or
installing tools. Deep scanners are discovered and recommended, not reimplemented.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
from typing import Any

VERSION = "0.1.0"

DOC_ALTERNATIVES = {
    "readme": ["README.md", "README.rst", "README.txt", "README"],
    "license": ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"],
    "security": ["SECURITY.md", ".github/SECURITY.md"],
    "contributing": ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"],
    "start_here": ["START-HERE.md", "docs/START-HERE.md", "docs/getting-started.md"],
}

RISK_MARKERS = {
    "destructive-delete": ["rm -rf ", "Remove-Item -Recurse -Force"],
    "force-git": ["git push --force", "git reset --hard"],
    "privilege-change": ["sudo ", "chmod 777", "Set-ExecutionPolicy Unrestricted"],
    "remote-shell-pipe": ["curl ", "wget "],
}

TEXT_SUFFIXES = {".md", ".txt", ".yml", ".yaml", ".sh", ".ps1", ".py", ".js", ".ts", ".json", ".toml"}


def first_existing(root: Path, candidates: list[str]) -> str | None:
    for candidate in candidates:
        if (root / candidate).is_file():
            return candidate
    return None


def discover_external_tools() -> dict[str, dict[str, str | bool]]:
    tools = {
        "gitleaks": "secret scanning",
        "lychee": "broken-link checking",
        "osv-scanner": "dependency vulnerability scanning",
        "actionlint": "GitHub Actions workflow linting",
        "shellcheck": "shell script analysis",
    }
    return {
        name: {"available": bool(shutil.which(name)), "purpose": purpose}
        for name, purpose in tools.items()
    }


def workflow_files(root: Path) -> list[Path]:
    folder = root / ".github" / "workflows"
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in {".yml", ".yaml"})


def scan_risk_markers(root: Path, max_files: int = 250) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    candidates: list[Path] = []
    for top in [".github", "scripts", "tools"]:
        base = root / top
        if base.exists():
            candidates.extend(p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
    for path in sorted(candidates)[:max_files]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for category, markers in RISK_MARKERS.items():
            for marker in markers:
                if marker in text:
                    findings.append({
                        "category": category,
                        "path": path.relative_to(root).as_posix(),
                        "marker": marker.strip(),
                        "classification": "REVIEW_REQUIRED_NOT_PROOF_OF_VULNERABILITY",
                    })
    return findings


def audit(root: Path) -> dict[str, Any]:
    root = root.resolve()
    docs = {key: first_existing(root, choices) for key, choices in DOC_ALTERNATIVES.items()}
    workflows = [p.relative_to(root).as_posix() for p in workflow_files(root)]
    readme_path = docs["readme"]
    readme_text = ""
    if readme_path:
        try:
            readme_text = (root / readme_path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass

    checks = {
        "readme": {"status": "PASS" if docs["readme"] else "NOTICE", "evidence": docs["readme"]},
        "license": {"status": "PASS" if docs["license"] else "REVIEW", "evidence": docs["license"]},
        "security_policy": {"status": "PASS" if docs["security"] else "NOTICE", "evidence": docs["security"]},
        "contributing": {"status": "PASS" if docs["contributing"] else "NOTICE", "evidence": docs["contributing"]},
        "beginner_start": {"status": "PASS" if docs["start_here"] else "NOTICE", "evidence": docs["start_here"]},
        "ci": {"status": "PASS" if workflows else "NOTICE", "evidence": workflows},
        "readme_substance": {
            "status": "PASS" if len(readme_text.strip()) >= 500 else "NOTICE",
            "evidence": {"characters": len(readme_text.strip())},
        },
    }
    risks = scan_risk_markers(root)
    return {
        "schema_version": "0.1",
        "tool": {"name": "repo_doctor.py", "version": VERSION, "mode": "READ_ONLY"},
        "checks": checks,
        "risk_markers": risks,
        "external_tools": discover_external_tools(),
        "privacy": {
            "file_contents_in_report": False,
            "environment_values_in_report": False,
            "credentials_read": False,
            "network_requests": False,
        },
        "mutation": {
            "repository_changed": False,
            "dependencies_installed": False,
            "commands_from_repository_executed": False,
        },
        "limitations": [
            "A PASS means the expected surface exists; it does not prove its content is correct.",
            "Risk-marker matches require human/context review and are not vulnerability findings by themselves.",
            "Use mature dedicated scanners for secrets, links, vulnerabilities, licenses, actions and shell analysis.",
        ],
    }


def beginner_summary(report: dict[str, Any]) -> str:
    review = [name for name, data in report["checks"].items() if data["status"] != "PASS"]
    risks = len(report["risk_markers"])
    if not review and not risks:
        return "The basic repository-health checks passed. This is not a security guarantee, and no files were changed."
    parts = ["The read-only repository check finished; no files were changed."]
    if review:
        parts.append("Review these project-hygiene areas: " + ", ".join(review) + ".")
    if risks:
        parts.append(f"{risks} potentially risky command marker(s) need context review; these are not automatically vulnerabilities.")
    return " ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only repository health explainer")
    parser.add_argument("path", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = audit(args.path)
    print(json.dumps(report, indent=2, sort_keys=True) if args.json else beginner_summary(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
