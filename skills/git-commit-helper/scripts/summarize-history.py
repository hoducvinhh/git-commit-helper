#!/usr/bin/env python3
"""
summarize-history.py - Analyze Git commit history conventions, scopes, and types.

Extracts recent commits, analyzes compliance with Conventional Commits, identifies
top types and scopes used in the repository, and provides a structured history summary.
"""

import argparse
import json
import os
import re
import subprocess
import sys

HEADER_REGEX = re.compile(r"^([a-zA-Z0-9_-]+)(?:\(([a-zA-Z0-9_\-./]+)\))?(!)?:\s*(.*)$")


def run_git_cmd(args, repo_path="."):
    """Safely executes a git command using subprocess without shell."""
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


def summarize_history(repo_path=".", limit=50, branch=None):
    """Analyzes commit history and extracts conventional commit patterns."""
    abs_path = os.path.abspath(repo_path)
    if not os.path.exists(abs_path):
        return {
            "is_git_repository": False,
            "error": f"Path does not exist: {abs_path}",
        }

    # Verify git repository
    code, out, _ = run_git_cmd(["rev-parse", "--is-inside-work-tree"], abs_path)
    if code != 0 or out.strip().lower() != "true":
        return {
            "is_git_repository": False,
            "error": "Not a git repository (or any of the parent directories).",
        }

    # Check unborn status
    code_head, _, _ = run_git_cmd(["rev-parse", "HEAD"], abs_path)
    if code_head != 0:
        return {
            "is_git_repository": True,
            "is_unborn": True,
            "total_commits": 0,
            "conventional_count": 0,
            "conventional_rate": 0.0,
            "types_distribution": {},
            "scopes_distribution": {},
            "breaking_count": 0,
            "commits": [],
        }

    # Format: hash %x1f author_name %x1f author_email %x1f date_iso %x1f subject %x1e
    # %x1f = Unit Separator, %x1e = Record Separator
    cmd = [
        "log",
        f"--max-count={limit}",
        "--format=%H%x1f%an%x1f%ae%x1f%ad%x1f%s%x1e",
        "--date=short",
    ]
    if branch:
        cmd.append(branch)

    code_log, out_log, _ = run_git_cmd(cmd, abs_path)
    if code_log != 0 or not out_log.strip():
        return {
            "is_git_repository": True,
            "is_unborn": False,
            "total_commits": 0,
            "conventional_count": 0,
            "conventional_rate": 0.0,
            "types_distribution": {},
            "scopes_distribution": {},
            "breaking_count": 0,
            "commits": [],
        }

    records = out_log.strip().split("\x1e")
    commits = []
    types_count = {}
    scopes_count = {}
    authors_count = {}
    conventional_count = 0
    breaking_count = 0

    for rec in records:
        rec = rec.strip()
        if not rec:
            continue
        fields = rec.split("\x1f")
        if len(fields) < 5:
            continue

        c_hash = fields[0]
        c_author = fields[1]
        c_email = fields[2]
        c_date = fields[3]
        c_subject = fields[4]

        authors_count[c_author] = authors_count.get(c_author, 0) + 1

        match = HEADER_REGEX.match(c_subject)
        is_conv = False
        c_type = None
        c_scope = None
        is_breaking = False

        if match:
            is_conv = True
            conventional_count += 1
            c_type = match.group(1).lower()
            c_scope = match.group(2)
            if match.group(3) == "!":
                is_breaking = True
                breaking_count += 1

            types_count[c_type] = types_count.get(c_type, 0) + 1
            if c_scope:
                scopes_count[c_scope] = scopes_count.get(c_scope, 0) + 1


if __name__ == '__main__':
    pass
