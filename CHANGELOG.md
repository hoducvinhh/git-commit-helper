# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-30

### Added
- Initial release of `git-commit-helper` agent skill.
- Deterministic helper scripts in standard library Python:
  - `git-status.py`: Discovers repository status, branches, HEAD commits, unborn states, and in-flight operations (merge, rebase, cherry-pick).
  - `analyze-diff.py`: Structured diff analysis with statistics, truncation guards, and automated secret/token redaction.
  - `validate-commit.py`: Strict Conventional Commits v1.0.0 validator with descriptive errors and actionable suggestions.
  - `summarize-history.py`: Git commit log parser analyzing conventions, scopes, and types across recent commits.
- Agent Skill definition (`skills/git-commit-helper/SKILL.md`) compliant with Agent Skills Specification.
- 8 comprehensive reference documents:
  - `conventional-commits.md`: Conventional Commits v1.0.0 reference.
  - `commit-guidelines.md`: Writing atomic, clear commit messages.
  - `git-workflow.md`: 9-step agent execution procedure.
  - `git-safety.md`: Strict rules and forbidden operations.
  - `change-analysis.md`: Semantic diff analysis rules.
  - `breaking-change-detection.md`: Heuristics for detecting breaking changes.
  - `commit-grouping.md`: Strategies for splitting unrelated changes.
  - `pull-request-guidelines.md`: PR structure and body generation.
- Templates for commit previews and pull requests (`assets/`).
- Automated test suite covering all helper scripts with pytest.
- Continuous Integration workflow via GitHub Actions (`validate.yml`).
