"""
test_git_status.py - Unit tests for git-status.py.
"""

import importlib.util
import os
import sys
import pytest

# Dynamically import git-status.py
SCRIPT_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "skills",
        "git-commit-helper",
        "scripts",
        "git-status.py",
    )
)
spec = importlib.util.spec_from_file_location("git_status", SCRIPT_PATH)
git_status = importlib.util.module_from_spec(spec)
sys.modules["git_status"] = git_status
spec.loader.exec_module(git_status)


def test_non_git_directory(tmp_path):
    """Test git-status on a regular non-git directory."""
    result = git_status.detect_git_status(str(tmp_path))
    assert result["is_git_repository"] is False
    assert "error" in result


def test_empty_unborn_repo(empty_git_repo):
    """Test git-status on a fresh repo with no commits."""
    result = git_status.detect_git_status(empty_git_repo)
    assert result["is_git_repository"] is True
    assert result["is_unborn"] is True
    assert result["head"] is None
    assert result["is_clean"] is True
    assert result["summary"]["staged_count"] == 0
    assert result["summary"]["unstaged_count"] == 0


def test_populated_clean_repo(populated_git_repo):
    """Test git-status on a repo with commits and a clean working tree."""
    result = git_status.detect_git_status(populated_git_repo)
    assert result["is_git_repository"] is True
    assert result["is_unborn"] is False
    assert result["head"] is not None
    assert len(result["head"]) >= 40
    assert result["is_clean"] is True
    assert result["in_progress_state"] is None


def test_dirty_repo_categorization(dirty_git_repo):
    """Test git-status categorizing staged, unstaged, and untracked files."""
    result = git_status.detect_git_status(dirty_git_repo)
    assert result["is_git_repository"] is True
    assert result["is_clean"] is False

    # Staged file check
    staged_paths = [item["path"] for item in result["staged"]]
    assert "staged.txt" in staged_paths
    staged_item = next(item for item in result["staged"] if item["path"] == "staged.txt")
    assert staged_item["status"] == "added"

    # Unstaged file check
    unstaged_paths = [item["path"] for item in result["unstaged"]]
    assert "core.py" in unstaged_paths
    unstaged_item = next(item for item in result["unstaged"] if item["path"] == "core.py")
    assert unstaged_item["status"] == "modified"

    # Untracked file check
    assert "untracked.log" in result["untracked"]

    # Summary check
    assert result["summary"]["staged_count"] == 1
    assert result["summary"]["unstaged_count"] == 1
    assert result["summary"]["untracked_count"] == 1


def test_in_progress_merge_state(populated_git_repo):
    """Test detection of merge in-progress state."""
    git_dir = os.path.join(populated_git_repo, ".git")
    merge_head = os.path.join(git_dir, "MERGE_HEAD")
    with open(merge_head, "w", encoding="utf-8") as f:
        f.write("0123456789abcdef0123456789abcdef01234567\n")

    result = git_status.detect_git_status(populated_git_repo)
    assert result["in_progress_state"] == "merge"


def test_in_progress_rebase_state(populated_git_repo):
    """Test detection of rebase in-progress state."""
    git_dir = os.path.join(populated_git_repo, ".git")
    rebase_dir = os.path.join(git_dir, "rebase-merge")
    os.makedirs(rebase_dir, exist_ok=True)

    result = git_status.detect_git_status(populated_git_repo)
    assert result["in_progress_state"] == "rebase"
