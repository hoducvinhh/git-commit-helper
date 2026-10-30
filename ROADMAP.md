# git-commit-helper Roadmap

This roadmap outlines the planned evolution of `git-commit-helper` across four iterative phases.

---

## Phase 1: MVP Foundation (Current)
- [x] Full project scaffold and governance documents (`README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `pyproject.toml`).
- [x] Core Python deterministic helper scripts:
  - `git-status.py`: Repo status, branch, HEAD, unborn branch handling, merge/rebase states.
  - `analyze-diff.py`: Staged/unstaged diff inspection, line truncation, secret redaction.
  - `validate-commit.py`: Conventional Commits v1.0.0 validation and suggestions.
  - `summarize-history.py`: Commit log extraction and convention analysis.
- [x] Agent skill specification (`skills/git-commit-helper/SKILL.md`).
- [x] Reference documentation (8 comprehensive guides).
- [x] Commit and PR preview templates (`assets/`).
- [x] Complete pytest test suite with disposable Git repository fixtures.
- [x] GitHub Actions CI workflow for multi-platform validation.

---

## Phase 2: Enhanced Semantic Intelligence
- [ ] Language-specific AST diff parsing (e.g., function signature changes in Python, TypeScript, Go).
- [ ] Multi-stage interactive commit builder with interactive prompt integration.
- [ ] Pre-commit hook generator (`.pre-commit-config.yaml` and `.git/hooks/commit-msg` integration).
- [ ] Automatic co-author detection from branch pairing metadata.

---

## Phase 3: Advanced Workflows & Monorepos
- [ ] Monorepo scope detection (inferring scope from modified directory roots).
- [ ] Interactive stash and branch switching helpers.
- [ ] Changelog generator based on conventional commits between Git tags.
- [ ] Merge conflict resolution assistant with safety guards.

---

## Phase 4: Integrations & IDE Plugins
- [ ] Antigravity CLI plugin bundle packaging.
- [ ] VS Code / JetBrains extension adapters.
- [ ] Direct Forge integration (GitHub CLI `gh`, GitLab CLI `glab`) for seamless PR submission.
