"""
test_summarize_history.py - Unit tests for summarize-history.py.
"""

import importlib.util
import os
import sys
import pytest

# Dynamically import summarize-history.py
SCRIPT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "skills",
        "git-commit-helper",
        "scripts",
        "summarize-history.py",
    )
)
spec = importlib.util.spec_from_file_location("summarize_history_mod", SCRIPT_PATH)
summarize_history_mod = importlib.util.module_from_spec(spec)
sys.modules["summarize_history_mod"] = summarize_history_mod
spec.loader.exec_module(summarize_history_mod)


def test_non_git_repo(tmp_path):
    """Test history summary on a non-git directory."""
    result = summarize_history_mod.summarize_history(str(tmp_path))
    assert result["is_git_repository"] is False
    assert "error" in result


def test_empty_unborn_repo(empty_git_repo):
    """Test history summary on a repo with 0 commits."""
    result = summarize_history_mod.summarize_history(empty_git_repo)
    assert result["is_git_repository"] is True
    assert result["is_unborn"] is True
    assert result["total_commits"] == 0
    assert result["conventional_count"] == 0
    assert result["conventional_rate"] == 0.0


def test_populated_repo_summary(populated_git_repo):
    """Test history analysis on a populated repo."""
    result = summarize_history_mod.summarize_history(populated_git_repo, limit=10)
    assert result["is_git_repository"] is True
    assert result["is_unborn"] is False
    assert result["total_commits"] == 4
    assert result["conventional_count"] == 4
    assert result["conventional_rate"] == 1.0
    assert result["breaking_count"] == 1

    # Verify type counts
    assert result["types_distribution"].get("feat") == 2
    assert result["types_distribution"].get("fix") == 1
    assert result["types_distribution"].get("docs") == 1

    # Verify scope counts
    assert result["scopes_distribution"].get("core") == 2
    assert result["scopes_distribution"].get("api") == 1
    assert result["scopes_distribution"].get("readme") == 1

    # Verify author
    assert result["authors_distribution"].get("Alice Tester") == 4

    # Verify commits list
    assert len(result["commits"]) == 4
    latest = result["commits"][0]
    assert latest["type"] == "feat"
    assert latest["scope"] == "api"
    assert latest["is_breaking"] is True


def test_limit_commits(populated_git_repo):
    """Test limit argument constraints."""
    result = summarize_history_mod.summarize_history(populated_git_repo, limit=2)
    assert result["total_commits"] == 2
    assert len(result["commits"]) == 2
