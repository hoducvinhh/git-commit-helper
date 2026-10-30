# Security Policy

## Supported Versions

The following versions of `git-commit-helper` are currently receiving security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

Security of developer tools and version control systems is paramount. If you discover a security vulnerability in `git-commit-helper`, please report it responsibly:

1. **Do not open public GitHub issues for security vulnerabilities.**
2. Send an email to the security team or open a GitHub Private Security Advisory.
3. Include the following details:
   - Type of vulnerability (e.g., command injection, unredacted secret leak, path traversal).
   - Step-by-step instructions or proof-of-concept repository.
   - Affected script or component.
   - Operating system and Python / Git versions used.

We will acknowledge receipt within 48 hours and provide a patch timeline.

## Architectural Security Guarantees

`git-commit-helper` adheres to the following core security invariants:

1. **Zero Shell Execution**: All external commands invoked by helper scripts are executed using `subprocess.run([...], shell=False)` with explicit arguments passed as separate list tokens.
2. **Read-Only Determinism**: The Python scripts (`git-status.py`, `analyze-diff.py`, `validate-commit.py`, `summarize-history.py`) perform **no write or mutating operations** on git repositories or disk files.
3. **Automated Secret Redaction**: The diff analyzer proactively detects API keys, bearer tokens, private keys, and credential assignments in diff hunks, redacting them with `[REDACTED_SECRET]` before outputting JSON to AI context.
4. **Mandatory User Authorization**: The skill instructions explicitly prohibit AI agents from executing `git commit` or `git push` without presenting the proposed changes and receiving affirmative user approval.
