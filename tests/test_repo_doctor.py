from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from repo_doctor import audit, beginner_summary


def test_this_repository_has_expected_learning_surfaces() -> None:
    report = audit(ROOT)
    assert report["checks"]["readme"]["status"] == "PASS"
    assert report["checks"]["beginner_start"]["status"] == "PASS"
    assert report["checks"]["ci"]["status"] == "PASS"


def test_repo_doctor_declares_read_only_boundary() -> None:
    report = audit(ROOT)
    assert report["tool"]["mode"] == "READ_ONLY"
    assert all(value is False for value in report["mutation"].values())
    assert all(value is False for value in report["privacy"].values())


def test_missing_license_is_review_not_fake_pass() -> None:
    report = audit(ROOT)
    # learning-git intentionally has no license decision yet.
    assert report["checks"]["license"]["status"] == "REVIEW"


def test_risk_marker_is_review_not_vulnerability_claim(tmp_path: Path) -> None:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "danger.sh").write_text("rm -rf /example\n", encoding="utf-8")
    report = audit(tmp_path)
    finding = next(item for item in report["risk_markers"] if item["category"] == "destructive-delete")
    assert finding["classification"] == "REVIEW_REQUIRED_NOT_PROOF_OF_VULNERABILITY"


def test_beginner_summary_explicitly_says_no_files_changed() -> None:
    text = beginner_summary(audit(ROOT)).lower()
    assert "no files were changed" in text
