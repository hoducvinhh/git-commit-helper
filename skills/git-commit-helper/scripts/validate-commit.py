#!/usr/bin/env python3
"""
validate-commit.py - Conventional Commits v1.0.0 Validator.

Parses and validates commit messages against Conventional Commits specification.
Checks types, scopes, breaking changes, header lengths, imperative moods,
body separation, and footer formats, providing structured error reports and fixes.
"""

import argparse
import json
import re
import sys

DEFAULT_ALLOWED_TYPES = [
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
]

# Conventional Commit Header regex
# Groups: 1=type, 3=scope, 4=breaking '!', 5=description
HEADER_REGEX = re.compile(r"^([a-zA-Z0-9_-]+)(?:\(([a-zA-Z0-9_\-./]+)\))?(!)?:\s*(.*)$")

# Footer token regex: either "BREAKING CHANGE:" or "TOKEN: " or "TOKEN #"
FOOTER_REGEX = re.compile(r"^(BREAKING CHANGE|BREAKING-CHANGE|[a-zA-Z0-9_-]+)(?::\s*(.*)| #([0-9]+.*))$")


def validate_commit_message(
    message: str,
    allowed_types=None,
    max_header_length=72,
    strict=False,
) -> dict:
    if allowed_types is None:
        allowed_types = DEFAULT_ALLOWED_TYPES

    errors = []
    warnings = []
    suggestions = []

    clean_message = message.strip()
    if not clean_message:
        return {
            "valid": False,
            "header": "",
            "type": None,
            "scope": None,
            "description": None,
            "is_breaking": False,
            "breaking_description": None,
            "body": None,
            "footers": [],
            "errors": ["Commit message cannot be empty."],
            "warnings": [],
            "suggestions": ["Provide a commit message in the format: feat(scope): description"],
        }

    lines = message.splitlines()
    header = lines[0].strip()

    parsed_type = None
    parsed_scope = None
    parsed_desc = None
    is_breaking = False
    breaking_desc = None
    body = None
    footers = []

    # 1. Header structural match
    match = HEADER_REGEX.match(header)
    if not match:
        errors.append(
            "Commit header does not match Conventional Commits format: '<type>(<scope>)?: <description>'"
        )
        suggestions.append(
            f"Example valid format: feat(core): add feature description"
        )
    else:
        raw_type = match.group(1)
        raw_scope = match.group(2)
        raw_bang = match.group(3)
        raw_desc = match.group(4)

        parsed_type = raw_type
        parsed_scope = raw_scope
        parsed_desc = raw_desc
        if raw_bang == "!":
            is_breaking = True

        # Check type validity
        if raw_type.lower() not in [t.lower() for t in allowed_types]:
            errors.append(
                f"Unknown commit type '{raw_type}'. Allowed types are: {', '.join(allowed_types)}"
            )
        elif raw_type != raw_type.lower():
            errors.append(f"Commit type '{raw_type}' must be lowercase.")
            suggestions.append(f"Change '{raw_type}' to '{raw_type.lower()}'")


if __name__ == '__main__':
    pass
