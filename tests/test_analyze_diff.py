"""
test_analyze_diff.py - Unit tests for analyze-diff.py.
"""

import importlib.util
import os
import sys
import pytest

# Dynamically import analyze-diff.py
SCRIPT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "skills",
        "git-commit-helper",
        "scripts",
        "analyze-diff.py",
    )
)
spec = importlib.util.spec_from_file_location("analyze_diff_mod", SCRIPT_PATH)
analyze_diff_mod = importlib.util.module_from_spec(spec)
sys.modules["analyze_diff_mod"] = analyze_diff_mod
spec.loader.exec_module(analyze_diff_mod)


def test_non_git_repo(tmp_path):
    """Test analyze-diff on a non-git directory."""
    result = analyze_diff_mod.analyze_diff(str(tmp_path))
    assert result["is_git_repository"] is False
    assert "error" in result


def test_clean_repo_empty_diff(populated_git_repo):
    """Test diff on a clean repository."""
    result = analyze_diff_mod.analyze_diff(populated_git_repo, is_staged=False)
    assert result["is_git_repository"] is True
    assert result["stats"]["files_changed"] == 0
    assert len(result["files"]) == 0
    assert result["truncated"] is False


def test_staged_diff(dirty_git_repo):
    """Test staged diff on a repository with staged files."""
    result = analyze_diff_mod.analyze_diff(dirty_git_repo, is_staged=True)
    assert result["is_git_repository"] is True
    assert result["is_staged"] is True
    assert result["stats"]["files_changed"] == 1
    file_entry = result["files"][0]
    assert file_entry["path"] == "staged.txt"
    assert file_entry["status"] == "added"
    assert file_entry["insertions"] >= 1
    assert "staged content" in file_entry["diff"]


def test_unstaged_diff(dirty_git_repo):
    """Test unstaged diff on a repository with unstaged modifications."""
    result = analyze_diff_mod.analyze_diff(dirty_git_repo, is_staged=False)
    assert result["is_git_repository"] is True
    assert result["is_staged"] is False
    assert result["stats"]["files_changed"] == 1
    file_entry = result["files"][0]
    assert file_entry["path"] == "core.py"
    assert file_entry["status"] == "modified"
    assert "unstaged line" in file_entry["diff"]


def test_secret_redaction(populated_git_repo):
    """Test that sensitive credentials in diff are automatically redacted."""
    core_file = os.path.join(populated_git_repo, "core.py")
    with open(core_file, "a", encoding="utf-8") as f:
        f.write('AWS_KEY = "AKIAIOSFODNN7EXAMPLE"\n')
        f.write('password = "supersecretpassword123"\n')

    # Run unstaged diff
    result = analyze_diff_mod.analyze_diff(populated_git_repo, is_staged=False, do_redact=True)
    assert result["has_secrets_redacted"] is True
    diff_text = result["files"][0]["diff"]
    assert "AKIAIOSFODNN7EXAMPLE" not in diff_text
    assert "[REDACTED_AWS_KEY]" in diff_text
    assert "supersecretpassword123" not in diff_text
    assert "[REDACTED_SECRET]" in diff_text


def test_max_diff_lines_truncation(populated_git_repo):
    """Test that diffs exceeding max_diff_lines are truncated."""
    core_file = os.path.join(populated_git_repo, "core.py")
    with open(core_file, "a", encoding="utf-8") as f:
        for i in range(100):
            f.write(f"Line number {i} with content\n")

    result = analyze_diff_mod.analyze_diff(
        populated_git_repo,
        is_staged=False,
        max_diff_lines=15,
    )
    assert result["truncated"] is True
    assert result["total_diff_lines"] > 15
    assert result["shown_diff_lines"] <= 15


def test_redact_secrets_direct():
    """Unit test secret redaction regex patterns directly."""
    # GitHub PAT
    gh_token = "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    text, redacted = analyze_diff_mod.redact_secrets(f"export GITHUB_TOKEN={gh_token}")
    assert redacted is True
    assert gh_token not in text
    assert "[REDACTED_GITHUB_TOKEN]" in text

    # Slack token
    slack_token = "xoxb-123456789012-1234567890123-456789abcdef"
    text, redacted = analyze_diff_mod.redact_secrets(f"SLACK_KEY = '{slack_token}'")
    assert redacted is True
    assert slack_token not in text

    # Bearer token
    bearer = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.e30.t-IDcSemACt8x4iTMC6Y5GmStSfMmMT2qnY"
    text, redacted = analyze_diff_mod.redact_secrets(f"Authorization: {bearer}")
    assert redacted is True
    assert "[REDACTED_BEARER_TOKEN]" in text
