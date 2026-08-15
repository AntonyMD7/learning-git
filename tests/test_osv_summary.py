from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from osv_summary import summarize


def sample_report():
    return {
        "results": [
            {
                "source": {"path": "/home/example/private/path/go.mod", "type": "lockfile"},
                "packages": [
                    {
                        "package": {"name": "example/pkg", "version": "1.0.0", "ecosystem": "Go"},
                        "vulnerabilities": [
                            {"id": "GHSA-aaaa-bbbb-cccc", "details": "must not be copied"},
                            {"id": "GO-2026-0001", "details": "must not be copied"},
                        ],
                        "groups": [{"ids": ["GHSA-aaaa-bbbb-cccc", "GO-2026-0001"]}],
                    }
                ],
            }
        ]
    }


def test_aliases_are_counted_as_one_group() -> None:
    result = summarize(sample_report())
    assert result["summary"]["affected_package_records"] == 1
    assert result["summary"]["unique_advisory_groups"] == 1
    assert result["affected_packages"][0]["advisory_group_count"] == 1


def test_absolute_path_and_advisory_body_are_not_returned() -> None:
    result = summarize(sample_report())
    rendered = repr(result)
    assert "/home/example/private/path" not in rendered
    assert "must not be copied" not in rendered
    assert result["affected_packages"][0]["source_file"] == "go.mod"
    assert result["privacy"]["absolute_source_paths_returned"] is False
    assert result["privacy"]["advisory_bodies_returned"] is False


def test_no_findings_is_not_safe_claim() -> None:
    result = summarize({"results": []})
    assert result["summary"]["unique_advisory_groups"] == 0
    assert "not proof" in result["beginner_explanation"].lower()
    assert result["evidence_semantics"]["no_findings_means_no_known_vulnerability_groups_in_supplied_report_only"] is True


def test_falls_back_to_vulnerability_ids_when_groups_missing() -> None:
    report = sample_report()
    del report["results"][0]["packages"][0]["groups"]
    result = summarize(report)
    assert result["summary"]["unique_advisory_groups"] == 2


def test_windows_paths_are_reduced_to_basename() -> None:
    report = sample_report()
    report["results"][0]["source"]["path"] = r"C:\Users\Person\project\package-lock.json"
    result = summarize(report)
    assert result["affected_packages"][0]["source_file"] == "package-lock.json"
