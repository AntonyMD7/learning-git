#!/usr/bin/env python3
"""Plain-language, privacy-minimizing summary of OSV-Scanner JSON output.

This is not a vulnerability scanner. Google OSV-Scanner remains the detection/data
source. This adapter reads an already-created JSON report and emits bounded package,
ecosystem and advisory-group counts without copying advisory bodies or absolute source
paths into the summary.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

VERSION = "0.1.0"


def _basename(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1][:160]


def _clean(value: object, limit: int = 160) -> str:
    return str(value or "UNKNOWN").strip()[:limit] or "UNKNOWN"


def _group_ids(entry: dict[str, Any]) -> list[tuple[str, ...]]:
    groups = entry.get("groups")
    if isinstance(groups, list) and groups:
        normalized: list[tuple[str, ...]] = []
        for group in groups:
            if not isinstance(group, dict):
                continue
            ids = group.get("ids", [])
            if isinstance(ids, list):
                cleaned = tuple(sorted({_clean(v, 80) for v in ids if v}))
                if cleaned:
                    normalized.append(cleaned)
        if normalized:
            return normalized

    vulns = entry.get("vulnerabilities", [])
    normalized = []
    if isinstance(vulns, list):
        for vuln in vulns:
            if isinstance(vuln, dict) and vuln.get("id"):
                normalized.append((_clean(vuln["id"], 80),))
    return normalized


def summarize(report: dict[str, Any]) -> dict[str, object]:
    results = report.get("results", [])
    if not isinstance(results, list):
        raise ValueError("OSV report results must be a list")

    ecosystems: Counter[str] = Counter()
    affected_packages: list[dict[str, object]] = []
    unique_groups: set[tuple[str, ...]] = set()
    source_types: Counter[str] = Counter()

    for result in results:
        if not isinstance(result, dict):
            continue
        source = result.get("source", {})
        if isinstance(source, dict):
            source_types[_clean(source.get("type"), 40)] += 1
            source_name = _basename(source.get("path"))
        else:
            source_name = None

        packages = result.get("packages", [])
        if not isinstance(packages, list):
            continue
        for entry in packages:
            if not isinstance(entry, dict):
                continue
            package = entry.get("package", {})
            if not isinstance(package, dict):
                package = {}
            ecosystem = _clean(package.get("ecosystem"), 80)
            name = _clean(package.get("name"), 160)
            version = _clean(package.get("version"), 80)
            groups = _group_ids(entry)
            if not groups:
                continue
            ecosystems[ecosystem] += 1
            unique_groups.update(groups)
            affected_packages.append(
                {
                    "ecosystem": ecosystem,
                    "package": name,
                    "version": version,
                    "source_file": source_name,
                    "advisory_group_count": len(groups),
                    "advisory_ids": [list(ids) for ids in groups[:20]],
                }
            )

    affected_packages.sort(key=lambda p: (-int(p["advisory_group_count"]), str(p["ecosystem"]), str(p["package"])))
    total_packages = len(affected_packages)
    total_groups = len(unique_groups)

    if total_groups == 0:
        beginner = "OSV-Scanner reported no known vulnerability groups in the supplied report. This is useful evidence, not proof that every dependency is safe."
    else:
        beginner = (
            f"OSV-Scanner reported {total_groups} known vulnerability group(s) affecting "
            f"{total_packages} package record(s). Review the upstream advisory and upgrade/remediation guidance before changing dependencies."
        )

    return {
        "schema_version": "0.1",
        "adapter": {"name": "osv_summary.py", "version": VERSION, "mode": "READ_ONLY_REPORT_TRANSFORM"},
        "summary": {
            "affected_package_records": total_packages,
            "unique_advisory_groups": total_groups,
            "ecosystems": dict(sorted(ecosystems.items())),
            "source_types": dict(sorted(source_types.items())),
        },
        "affected_packages": affected_packages[:200],
        "beginner_explanation": beginner,
        "evidence_semantics": {
            "scanner_source": "OSV-Scanner",
            "scanner_run_performed_by_this_adapter": False,
            "no_findings_means_no_known_vulnerability_groups_in_supplied_report_only": True,
            "automatic_remediation_performed": False,
        },
        "privacy": {
            "absolute_source_paths_returned": False,
            "advisory_bodies_returned": False,
            "environment_values_read": False,
            "credentials_read": False,
            "network_requests_made": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize existing OSV-Scanner JSON without scanning or remediation")
    parser.add_argument("--input", required=True, type=Path, help="Path to OSV-Scanner --format json output")
    args = parser.parse_args()
    report = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(summarize(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
