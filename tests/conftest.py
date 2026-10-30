"""
conftest.py - Pytest fixtures providing disposable Git repositories for testing.
"""

import os
import shutil
import subprocess
import tempfile
import pytest


def run_git(args, cwd):
    """Executes a git command inside a specific test repository."""
    proc = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\nError: {proc.stderr}")
    return proc.stdout.strip()


@pytest.fixture
def empty_git_repo():
    """Provides a freshly initialized git repository with 0 commits (unborn HEAD)."""
    temp_dir = tempfile.mkdtemp(prefix="git_test_empty_")
    try:
        run_git(["init"], cwd=temp_dir)
        run_git(["config", "user.name", "Test Runner"], cwd=temp_dir)
        run_git(["config", "user.email", "test@example.com"], cwd=temp_dir)
        run_git(["config", "commit.gpgSign", "false"], cwd=temp_dir)
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def populated_git_repo():
    """Provides a git repository with conventional commit history."""
    temp_dir = tempfile.mkdtemp(prefix="git_test_populated_")
    try:
        run_git(["init", "-b", "main"], cwd=temp_dir)
        run_git(["config", "user.name", "Alice Tester"], cwd=temp_dir)
        run_git(["config", "user.email", "alice@example.com"], cwd=temp_dir)
        run_git(["config", "commit.gpgSign", "false"], cwd=temp_dir)

        # Commit 1: feat(core)
        file1 = os.path.join(temp_dir, "core.py")
        with open(file1, "w", encoding="utf-8") as f:
            f.write("print('core initial')\n")
        run_git(["add", "core.py"], cwd=temp_dir)
        run_git(["commit", "-m", "feat(core): initial core implementation"], cwd=temp_dir)

        # Commit 2: fix(core)
        with open(file1, "a", encoding="utf-8") as f:
            f.write("# bugfix line\n")
        run_git(["add", "core.py"], cwd=temp_dir)
        run_git(["commit", "-m", "fix(core): fix syntax error in core"], cwd=temp_dir)

        # Commit 3: docs(readme)
        readme = os.path.join(temp_dir, "README.md")
        with open(readme, "w", encoding="utf-8") as f:
            f.write("# Test Project\n")
        run_git(["add", "README.md"], cwd=temp_dir)
        run_git(["commit", "-m", "docs(readme): add project readme"], cwd=temp_dir)

        # Commit 4: feat(api)!: breaking change
        api_file = os.path.join(temp_dir, "api.py")
        with open(api_file, "w", encoding="utf-8") as f:
            f.write("def api_v2(): pass\n")
        run_git(["add", "api.py"], cwd=temp_dir)
        run_git(["commit", "-m", "feat(api)!: upgrade to v2 api endpoints"], cwd=temp_dir)

        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def dirty_git_repo(populated_git_repo):
    """Provides a git repo with staged, unstaged, untracked, and modified files."""
    repo = populated_git_repo

    # Staged change
    staged_file = os.path.join(repo, "staged.txt")
    with open(staged_file, "w", encoding="utf-8") as f:
        f.write("staged content\n")
    run_git(["add", "staged.txt"], cwd=repo)

    # Unstaged change in existing tracked file
    core_file = os.path.join(repo, "core.py")
    with open(core_file, "a", encoding="utf-8") as f:
        f.write("# unstaged line\n")

    # Untracked file
    untracked_file = os.path.join(repo, "untracked.log")
    with open(untracked_file, "w", encoding="utf-8") as f:
        f.write("temporary log file\n")

    return repo
