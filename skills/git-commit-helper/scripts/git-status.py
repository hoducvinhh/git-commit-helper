#!/usr/bin/env python3
"""
git-status.py - Structured Git repository state detector.

Inspects repository root, branch, HEAD, unborn status, remote tracking status,
in-progress operations (merge, rebase, cherry-pick), and categorized files
(staged, unstaged, untracked, conflicted). Outputs structured JSON.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_git_cmd(args, repo_path=None):
    """Executes a git command safely with shell=False."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as e:
        return -1, "", str(e)


def detect_git_status(repo_path="."):
    """Detects comprehensive Git status and returns a dictionary."""
    abs_path = os.path.abspath(repo_path)
    if not os.path.exists(abs_path):
        return {
            "is_git_repository": False,
            "error": f"Path does not exist: {abs_path}",
        }

    # 1. Check if inside git repo
    code, out, _ = run_git_cmd(["rev-parse", "--is-inside-work-tree"], abs_path)
    if code != 0 or out.strip().lower() != "true":
        return {
            "is_git_repository": False,
            "error": "Not a git repository (or any of the parent directories).",
        }

    # 2. Get repository root
    _, repo_root, _ = run_git_cmd(["rev-parse", "--show-toplevel"], abs_path)
    repo_root = repo_root.strip() if repo_root.strip() else abs_path

    # 3. Get git dir (handles .git, submodules, worktrees)
    _, git_dir_raw, _ = run_git_cmd(["rev-parse", "--git-dir"], repo_root)
    git_dir = os.path.abspath(os.path.join(repo_root, git_dir_raw.strip())) if git_dir_raw.strip() else None

    # 4. Check unborn branch (empty repo with no commits)
    code_head, head_hash, _ = run_git_cmd(["rev-parse", "HEAD"], repo_root)
    is_unborn = (code_head != 0)
    head_commit = head_hash.strip() if not is_unborn else None

    # 5. Get current branch
    _, branch, _ = run_git_cmd(["branch", "--show-current"], repo_root)
    branch = branch.strip()
    if not branch:
        # Might be detached HEAD or unborn branch
        _, ref_name, _ = run_git_cmd(["rev-parse", "--abbrev-ref", "HEAD"], repo_root)
        branch = ref_name.strip() if ref_name.strip() else "HEAD (detached)"

    # 6. Detect in-progress states
    in_progress = None
    if git_dir and os.path.exists(git_dir):
        if os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
            in_progress = "merge"
        elif (
            os.path.exists(os.path.join(git_dir, "rebase-merge"))
            or os.path.exists(os.path.join(git_dir, "rebase-apply"))
        ):
            in_progress = "rebase"
        elif os.path.exists(os.path.join(git_dir, "CHERRY_PICK_HEAD")):
            in_progress = "cherry-pick"
        elif os.path.exists(os.path.join(git_dir, "REVERT_HEAD")):
            in_progress = "revert"
        elif os.path.exists(os.path.join(git_dir, "BISECT_LOG")):
            in_progress = "bisect"

    # 7. Check upstream branch and ahead/behind counts
    upstream = None
    ahead = 0
    behind = 0
    if not is_unborn:
        code_up, up_branch, _ = run_git_cmd(
            ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], repo_root
        )
        if code_up == 0 and up_branch.strip():
            upstream = up_branch.strip()
            code_counts, counts, _ = run_git_cmd(
                ["rev-list", "--left-right", "--count", "HEAD...@{u}"], repo_root
            )
            if code_counts == 0 and counts.strip():
                parts = counts.strip().split()
                if len(parts) == 2:
                    try:
                        ahead = int(parts[0])
                        behind = int(parts[1])
                    except ValueError:
                        pass

    # 8. Parse status porcelain
    # porcelain=v1 with -z uses NUL as record separator
    code_st, out_st, _ = run_git_cmd(["status", "--porcelain=v1", "-z", "-u"], repo_root)
    


if __name__ == '__main__':
    pass
