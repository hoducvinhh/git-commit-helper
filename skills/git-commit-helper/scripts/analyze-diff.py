#!/usr/bin/env python3
"""
analyze-diff.py - Structured Git diff parser with truncation and secret redaction.

Parses staged or unstaged diffs, extracts diff statistics, identifies binary and
renamed files, enforces max line limits to prevent LLM context overflow, and
redacts sensitive credentials/tokens from diff hunks.
"""

import argparse
import json
import os
import re
import subprocess
import sys

# Regex patterns for detecting and redacting sensitive credentials
SECRET_PATTERNS = [
    # AWS Access Key ID
    (re.compile(r"\b(AKIA[0-9A-Z]{16})\b"), "[REDACTED_AWS_KEY]"),
    # GitHub Personal Access Token
    (re.compile(r"\b(gh[pousr]_[A-Za-z0-9_]{36,255})\b"), "[REDACTED_GITHUB_TOKEN]"),
    # Slack Token
    (re.compile(r"\b(xox[baprs]-[0-9A-Za-z-]{10,})\b"), "[REDACTED_SLACK_TOKEN]"),
    # Private Key Headers
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY_START]"),
    (re.compile(r"-----END [A-Z ]*PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY_END]"),
    # Generic Bearer Tokens
    (re.compile(r"(?i)\b(Bearer\s+)[A-Za-z0-9_\-\.]{20,}\b"), r"\1[REDACTED_BEARER_TOKEN]"),
    # Generic password / secret / api-key assignments in quotes
    (
        re.compile(
            r"""(?i)\b(api[_-]?key|secret|password|passwd|auth[_-]?token|access[_-]?token)\s*([:=])\s*(['"])(?:(?!\3).){8,}\3"""
        ),
        r"\1\2\3[REDACTED_SECRET]\3",
    ),
]


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


def redact_secrets(text: str) -> tuple[str, bool]:
    """Applies secret patterns to redact sensitive credentials. Returns (redacted_text, was_redacted)."""
    redacted = False
    result = text
    for pattern, replacement in SECRET_PATTERNS:
        new_result, count = pattern.subn(replacement, result)
        if count > 0:
            redacted = True
            result = new_result
    return result, redacted


def parse_numstat(numstat_output: str) -> dict:
    """Parses `git diff --numstat` output into per-file insertions, deletions, and binary status."""
    file_stats = {}
    for line in numstat_output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            add_s, del_s, path = parts[0], parts[1], parts[2]
            # Handle renames in numstat: "old => new" or "prefix/{old => new}/suffix"
            clean_path = path
            if "=>" in path:
                # If path contains rename notation
                clean_path = path.split("=>")[-1].strip().rstrip("}").strip()
                if "{" in path and "}" in path:


if __name__ == '__main__':
    pass
