#!/usr/bin/env python3
"""Bounded summary adapter for Licensee JSON output.

Licensee remains the license-detection engine. This adapter performs no legal
interpretation and does not classify a detected license as suitable for a project.
It strips matched-file paths to basenames and emits only public license identifiers
plus explicit evidence limitations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

VERSION = "0.1.0"


def _basename(value: object) -> str | None:
    if not isinstance(value, str) or not value:
        return None
    return value.replace("\\", "/").rstrip("/").rsplit("/", 1)[-1][:160]


def _license_id(item: object) -> str | None:
    if not isinstance(item, dict):
        return None
    for key in ("spdx_id", "spdx-id", "key", "id"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()[:100]
    meta = item.get("meta")
    if isinstance(meta, dict):
        for key in ("spdx-id", "spdx_id", "key"):
            value = meta.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()[:100]
    return None


def _matched_name(item: object) -> str | None:
    if not isinstance(item, dict):
        return None
    for key in ("filename", "path", "name"):
        name = _basename(item.get(key))
        if name:
            return name
    return None


def summarize(report: dict[str, Any], *, detector_exit_code: int | None = None) -> dict[str, object]:
    licenses_raw = report.get("licenses", [])
    matched_raw = report.get("matched_files", [])
    if not isinstance(licenses_raw, list) or not isinstance(matched_raw, list):
        raise ValueError("Licensee JSON must contain licenses and matched_files arrays")

    license_ids = sorted({license_id for item in licenses_raw if (license_id := _license_id(item))})
    matched_files = sorted({name for item in matched_raw if (name := _matched_name(item))})
    detected = bool(license_ids)

    if detected:
        explanation = (
            "Licensee detected license identifier(s) in the supplied project report. "
            "Detection is not legal advice and does not prove that all files or dependencies share the same license."
        )
    else:
        explanation = (
            "Licensee did not identify a project license in the supplied report. "
            "Do not assume permission to reuse or redistribute code merely because no license was detected."
        )

    return {
        "schema_version": "0.1",
        "adapter": {"name": "licensee_summary.py", "version": VERSION, "mode": "READ_ONLY_REPORT_TRANSFORM"},
        "detected": detected,
        "license_ids": license_ids,
        "matched_files": matched_files,
        "detector_exit_code": detector_exit_code,
        "beginner_explanation": explanation,
        "evidence_semantics": {
            "detector_source": "Licensee",
            "legal_advice": False,
            "license_suitability_decision": False,
            "dependency_license_coverage_claim": False,
            "copyright_permission_claim": False,
        },
        "privacy": {
            "absolute_paths_returned": False,
            "license_file_content_returned": False,
            "environment_values_read": False,
            "credentials_read": False,
            "network_requests_made_by_adapter": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize existing Licensee JSON without legal interpretation")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--detector-exit-code", type=int)
    args = parser.parse_args()
    report = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(summarize(report, detector_exit_code=args.detector_exit_code), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
