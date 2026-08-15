from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_beginner_paths_exist() -> None:
    for relative in ["README.md", "START-HERE.md", "exercises/01-first-branch.md"]:
        path = ROOT / relative
        assert path.is_file() and path.stat().st_size > 0, relative


def test_start_here_points_to_first_exercise() -> None:
    text = (ROOT / "START-HERE.md").read_text(encoding="utf-8")
    assert "exercises/01-first-branch.md" in text


def test_readme_teaches_branch_before_push() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "git switch -c" in text
    assert "git push -u origin" in text
    assert text.index("git switch -c") < text.index("git push -u origin")


def test_secret_safety_warning_present() -> None:
    combined = "\n".join(
        (ROOT / name).read_text(encoding="utf-8")
        for name in ["README.md", "START-HERE.md"]
    ).lower()
    assert "api key" in combined
    assert "private key" in combined
    assert ".env" in combined
