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




if __name__ == '__main__':
    pass
