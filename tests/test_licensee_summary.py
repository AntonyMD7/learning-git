from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from licensee_summary import summarize


def test_detected_license_is_bounded_to_identifier_and_basename() -> None:
    report = {
        "licenses": [{"spdx_id": "MIT", "title": "MIT License", "body": "do not copy"}],
        "matched_files": [{"path": "/home/private/project/LICENSE", "content": "do not copy"}],
    }
    result = summarize(report, detector_exit_code=0)
    assert result["detected"] is True
    assert result["license_ids"] == ["MIT"]
    assert result["matched_files"] == ["LICENSE"]
    rendered = repr(result)
    assert "/home/private/project" not in rendered
    assert "do not copy" not in rendered


def test_no_detection_is_not_permission_claim() -> None:
    result = summarize({"licenses": [], "matched_files": []}, detector_exit_code=1)
    assert result["detected"] is False
    assert "do not assume permission" in result["beginner_explanation"].lower()
    assert result["evidence_semantics"]["copyright_permission_claim"] is False


def test_multiple_license_identifiers_are_deduplicated() -> None:
    report = {
        "licenses": [{"spdx_id": "MIT"}, {"spdx-id": "Apache-2.0"}, {"spdx_id": "MIT"}],
        "matched_files": [{"filename": "LICENSE"}, {"filename": "NOTICE"}],
    }
    result = summarize(report)
    assert result["license_ids"] == ["Apache-2.0", "MIT"]
    assert result["matched_files"] == ["LICENSE", "NOTICE"]


def test_nested_meta_spdx_id_is_supported() -> None:
    result = summarize(
        {"licenses": [{"meta": {"spdx-id": "BSD-3-Clause"}}], "matched_files": []}
    )
    assert result["license_ids"] == ["BSD-3-Clause"]


def test_windows_matched_path_is_reduced_to_basename() -> None:
    result = summarize(
        {
            "licenses": [{"spdx_id": "MIT"}],
            "matched_files": [{"path": r"C:\Users\Person\repo\LICENSE.md"}],
        }
    )
    assert result["matched_files"] == ["LICENSE.md"]
