# Contributing to git-commit-helper

Thank you for your interest in contributing to `git-commit-helper`! This project provides deterministic tooling and agent instructions to keep version control safe, clean, and conventional.

---

## Code of Conduct

Please be respectful, constructive, and considerate of all contributors and users.

---

## Development Setup

1. **Prerequisites**:
   - Python 3.8+
   - Git 2.25+
   - `pytest`

2. **Clone the repository**:
   ```bash
   git clone https://github.com/hoducvinhh/git-commit-helper.git
   cd git-commit-helper
   ```

3. **Install development dependencies**:
   ```bash
   pip install pytest
   ```

4. **Run the test suite**:
   ```bash
   pytest
   ```

---

## Architectural Guidelines

When submitting pull requests, ensure adherence to our design principles:

1. **Standard Library Only**: Python helper scripts in `skills/git-commit-helper/scripts/` must NOT depend on third-party packages (no `pip install` required in production).
2. **Safe Subprocess Execution**: Always invoke Git via `subprocess.run(["git", ...], shell=False, check=False)`. Never construct raw shell strings.
3. **Structured Output**: Scripts must emit clean, valid JSON to stdout when run from the CLI.
4. **Agent Spec Compatibility**: Skill definitions must follow the Agent Skills Specification (valid YAML frontmatter with `name` and `description`).
5. **Atomic Conventional Commits**: All commits in this repository must adhere to the Conventional Commits specification.

---

## Submitting Pull Requests

1. Fork the repo and create a descriptive feature branch:
   ```bash
   git checkout -b feat/diff-hunk-filtering
   ```
2. Make your changes and add corresponding unit tests under `tests/`.
3. Verify that all tests pass:
   ```bash
   pytest -v
   ```
4. Commit your changes using Conventional Commits format:
   ```bash
   git commit -m "feat(diff): add hunk filtering by line count"
   ```
5. Push to your fork and submit a Pull Request with a clear description of the problem solved.
