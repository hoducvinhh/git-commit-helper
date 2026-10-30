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
                    prefix = path.split("{")[0]
                    clean_path = prefix + clean_path

            is_binary = add_s == "-" and del_s == "-"
            insertions = int(add_s) if not is_binary else 0
            deletions = int(del_s) if not is_binary else 0
            file_stats[clean_path] = {
                "raw_path": path,
                "insertions": insertions,
                "deletions": deletions,
                "is_binary": is_binary,
            }
    return file_stats


def analyze_diff(repo_path=".", is_staged=False, max_diff_lines=500, do_redact=True):
    """Analyzes git diff and returns structured details with stats and redaction."""
    abs_path = os.path.abspath(repo_path)
    if not os.path.exists(abs_path):
        return {
            "is_git_repository": False,
            "error": f"Path does not exist: {abs_path}",
        }

    # Verify git repo
    code, out, _ = run_git_cmd(["rev-parse", "--is-inside-work-tree"], abs_path)
    if code != 0 or out.strip().lower() != "true":
        return {
            "is_git_repository": False,
            "error": "Not a git repository (or any of the parent directories).",
        }

    diff_flag = ["--cached"] if is_staged else []

    # 1. Fetch numstat
    _, numstat_out, _ = run_git_cmd(["diff"] + diff_flag + ["--numstat"], abs_path)
    file_stats = parse_numstat(numstat_out)

    # 2. Fetch full raw diff
    _, raw_diff, _ = run_git_cmd(
        ["diff"] + diff_flag + ["--no-color", "-U3"], abs_path
    )

    any_redacted = False
    files_result = []
    total_insertions = 0
    total_deletions = 0

    # Split diff by "diff --git a/"
    raw_file_chunks = []
    if raw_diff:
        chunks = raw_diff.split("diff --git ")
        for chunk in chunks:
            if chunk.strip():
                raw_file_chunks.append("diff --git " + chunk)

    total_diff_lines = len(raw_diff.splitlines()) if raw_diff else 0
    accumulated_lines = 0
    truncated = False

    for chunk in raw_file_chunks:
        # Extract file paths from "diff --git a/PATH b/PATH"
        lines = chunk.splitlines(keepends=True)
        first_line = lines[0] if lines else ""
        file_path = ""
        m = re.match(r"diff --git a/(.*?) b/(.*)", first_line.strip())
        if m:
            file_path = m.group(2)
        else:
            file_path = "unknown"

        # Determine file status (new file, deleted file, rename, modified)
        status = "modified"
        if "new file mode" in chunk:
            status = "added"
        elif "deleted file mode" in chunk:
            status = "deleted"
        elif "rename from" in chunk or "similarity index" in chunk:
            status = "renamed"

        is_bin = ("Binary files differ" in chunk) or ("GIT binary patch" in chunk)
        stat_info = file_stats.get(file_path, {})
        ins = stat_info.get("insertions", 0)
        dels = stat_info.get("deletions", 0)
        if not is_bin:
            is_bin = stat_info.get("is_binary", False)

        total_insertions += ins
        total_deletions += dels

        # Apply redaction if enabled
        chunk_text = chunk
        if do_redact:
            chunk_text, redacted = redact_secrets(chunk_text)
            if redacted:
                any_redacted = True

        # Check line limits
        chunk_lines = chunk_text.splitlines()


if __name__ == '__main__':
    pass
