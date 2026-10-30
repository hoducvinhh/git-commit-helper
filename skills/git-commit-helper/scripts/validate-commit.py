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

        # Check scope validity
        if raw_scope is not None:
            if not raw_scope.strip():
                errors.append("Scope cannot be empty if parentheses '()' are present.")
            elif raw_scope != raw_scope.strip():
                errors.append("Scope cannot contain leading or trailing whitespace.")

        # Check description
        if not raw_desc or not raw_desc.strip():
            errors.append("Commit description cannot be empty.")
        else:
            desc_trimmed = raw_desc.strip()
            # Check trailing period
            if desc_trimmed.endswith("."):
                errors.append("Commit description must not end with a period '.'.")
                clean_desc = desc_trimmed.rstrip(".")
                reconstructed_scope = f"({raw_scope})" if raw_scope else ""
                reconstructed_bang = "!" if raw_bang else ""
                suggestions.append(
                    f"Remove period: '{raw_type}{reconstructed_scope}{reconstructed_bang}: {clean_desc}'"
                )

            # Check lowercase starting letter
            if desc_trimmed[0].isupper():
                warnings.append(
                    f"Description starts with an uppercase letter '{desc_trimmed[0]}'. Conventional Commits prefers lowercase imperative mood."
                )
                suggested_desc = desc_trimmed[0].lower() + desc_trimmed[1:]
                reconstructed_scope = f"({raw_scope})" if raw_scope else ""
                reconstructed_bang = "!" if raw_bang else ""
                suggestions.append(
                    f"Use lowercase: '{raw_type}{reconstructed_scope}{reconstructed_bang}: {suggested_desc}'"
                )

    # 2. Header Length Check
    if len(header) > max_header_length:
        warnings.append(
            f"Commit header length ({len(header)}) exceeds recommended maximum ({max_header_length} chars)."
        )
    if len(header) > 100:
        errors.append(
            f"Commit header length ({len(header)}) exceeds hard limit of 100 characters."
        )

    # 3. Body & Footer checks (if multiline)
    if len(lines) > 1:
        # Check blank line after header
        if lines[1].strip() != "":
            errors.append("Second line of commit message must be blank (separating header from body).")

        # Parse subsequent sections
        body_lines = []
        footer_lines = []
        in_footer_section = False

        for i, line in enumerate(lines[2:], start=3):
            # Check for footer match
            footer_match = FOOTER_REGEX.match(line)
            if footer_match:
                in_footer_section = True
                token = footer_match.group(1)
                value = (footer_match.group(2) or footer_match.group(3) or "").strip()
                footers.append({"token": token, "value": value})
                if token in ("BREAKING CHANGE", "BREAKING-CHANGE"):
                    is_breaking = True
                    breaking_desc = value
            elif in_footer_section:
                # Continuation line of footer or another footer


if __name__ == '__main__':
    pass
