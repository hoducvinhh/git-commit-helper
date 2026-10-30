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


if __name__ == '__main__':
    pass
