# Git Commit Helper - Implementation Plan

Project Name: **git-commit-helper**  
Project Type: **Open Source Agent Skill**  
Specification: **1.0 (Agent Skills Specification compatible)**  
Target Phase: **Phase 1: MVP Foundation**

---

## 1. Executive Summary & Goals

`git-commit-helper` is an open-source Agent Skill that turns AI coding assistants into an intelligent, disciplined, and safe Git Workflow Partner.

It enables agents to:
1. Discover and inspect Git repository states (root, branch, HEAD, staged, unstaged, untracked, rebase/merge states).
2. Deeply analyze code diffs, file modifications, additions, and deletions.
3. Understand the semantic intent of changes (feat, fix, docs, refactor, perf, test, build, ci, chore).
4. Recommend logical commit splitting for unrelated changes.
5. Identify potential breaking changes and format breaking change notices.
6. Validate commit messages against Conventional Commits v1.0.0.
7. Generate comprehensive Pull Request descriptions.
8. Strictly prevent risky, accidental, or destructive Git operations (e.g. no automatic push, no history rewriting, no `git add .` by default, mandatory user authorization before commit).

---

## 2. System Architecture & Component Design

The skill follows a strict **Decoupled Architecture**:
- **Deterministic Layer (Python Helper Scripts)**: Read-only CLI tools running standard library Python. They safely collect raw Git data, format diffs with truncation and secret redaction, validate commit conventions, and extract commit history summaries into structured JSON.
- **Cognitive Layer (AI Agent + SKILL.md + References)**: The AI coding agent handles semantic code comprehension, change grouping, commit message generation, interactive questioning, and asking for user authorization.
- **Safety Boundary**: The helper scripts have ZERO write/mutation operations on git. The agent executes commits ONLY after explicit user confirmation of the staged files and the commit message.

```
git-commit-helper/
│
├── README.md                           # Project overview, installation, usage
├── LICENSE                             # MIT License
├── CONTRIBUTING.md                     # Community contribution guidelines
├── CHANGELOG.md                        # Milestone release history
├── SECURITY.md                         # Security policy & secret protection rules
├── ROADMAP.md                          # Implementation roadmap across Phases 1-4
├── pyproject.toml                      # Test configuration (pytest)
├── PLAN.md                             # This plan document
│
├── skills/
│   └── git-commit-helper/
│       ├── SKILL.md                    # Core Agent Skill definition & frontmatter
│       │
│       ├── references/
│       │   ├── conventional-commits.md # Conventional Commits specification & types
│       │   ├── commit-guidelines.md    # Writing clear, atomic commit messages
│       │   ├── git-workflow.md         # 9-step agent workflow breakdown
│       │   ├── git-safety.md           # Safety rules & forbidden operations
│       │   ├── change-analysis.md      # Semantic diff analysis guide
│       │   ├── breaking-change-detection.md # Heuristics for breaking API/schema changes
│       │   ├── commit-grouping.md      # Rules for splitting unrelated changes
│       │   └── pull-request-guidelines.md   # PR description generation template & guide
│       │
│       ├── scripts/
│       │   ├── git-status.py           # JSON Git status & state detector
│       │   ├── analyze-diff.py         # JSON diff parser with limit & secret redaction
│       │   ├── validate-commit.py      # Conventional commit validator & corrector
│       │   └── summarize-history.py    # Git history analyzer & convention extractor
│       │
│       └── assets/
│           ├── commit-template.md      # Commit preview template
│           └── pr-template.md          # Pull Request template
│
├── tests/
│   ├── conftest.py                     # Git test repository fixtures generator
│   ├── test_git_status.py              # Status script unit tests
│   ├── test_analyze_diff.py            # Diff script unit tests
│   ├── test_validate_commit.py         # Validator unit tests
│   └── test_summarize_history.py       # History summary unit tests
│
└── .github/
    └── workflows/
        └── validate.yml                # Multi-platform CI test runner
```

---

## 3. Analysis of Ambiguities & Technical Risks

| Ambiguity / Risk | Description | Mitigating Strategy |
| :--- | :--- | :--- |
| **Unborn Git Repositories** | Fresh `git init` repos have no HEAD or commits. Running `git rev-parse HEAD` fails. | `git-status.py` handles unborn branches gracefully, reporting `head: null` and `is_initial_commit: true`. |
| **Context Window Overflow** | Enormous diffs (lockfiles, minified bundles) can overflow LLM token limits. | `analyze-diff.py` implements configurable line limits (`--max-diff-lines`), byte limits per file, and diffstat rollups. |
| **Secret & Token Leakage** | Staged or working files might contain accidental API keys or passwords. | `analyze-diff.py` filters diff hunks against regex patterns for secrets and tokens, substituting with `[REDACTED_SECRET]`. |
| **Subprocess Injection** | Shell-based commands on Windows/Linux can be vulnerable to path injection. | Every script strictly uses `subprocess.run([...], shell=False)` with arguments passed as separate list items. |
| **Zero Runtime Dependencies** | Installing pip packages can break or fail on restricted machines. | All scripts use Python 3.8+ standard library only (`subprocess`, `json`, `argparse`, `sys`, `re`, `pathlib`). |

---

## 4. Phase 1 (MVP Foundation) Implementation Steps

### Step 1: Governance & Repository Foundations
- Create `LICENSE` (MIT).
- Create `README.md` with complete documentation, badges, and quickstart examples.
- Create `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `CHANGELOG.md`.
- Create `.gitignore` and `pyproject.toml`.

### Step 2: Deterministic Python Helper Scripts
1. **`git-status.py`**:
   - Detects repo root, current branch, HEAD commit hash.
   - Detects merge, rebase, cherry-pick, revert states.
   - Categorizes files: staged (added, modified, deleted, renamed), unstaged, untracked.
   - Outputs machine-readable JSON.
2. **`analyze-diff.py`**:
   - Fetches staged (`--staged`) or unstaged diffs.
   - Summarizes diff statistics (additions, deletions, modified files).
   - Identifies binary files and renamed files.
   - Supports line limit and secret redaction.
3. **`validate-commit.py`**:
   - Validates `<type>(<scope>)?: <description>` format.
   - Checks allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
   - Validates breaking change exclamation mark (`!`) or `BREAKING CHANGE:` footer.
   - Returns structured JSON `{ "valid": bool, "errors": [], "warnings": [], "suggestions": [] }`.
4. **`summarize-history.py`**:
   - Analyzes recent commits (`--limit N`).
   - Computes frequencies of types and scopes to infer repository conventions.

### Step 3: Core Skill Definition & References
- Create `skills/git-commit-helper/SKILL.md` compliant with the Agent Skills specification.
- Create all 8 reference markdown files in `skills/git-commit-helper/references/`.
- Create templates in `skills/git-commit-helper/assets/`.

### Step 4: Test Infrastructure & Automated Verification
- Create fixture generator in `tests/conftest.py` setting up disposable Git repositories.
- Write unit tests for all 4 scripts with 100% core path coverage.
- Add GitHub Actions CI workflow in `.github/workflows/validate.yml`.

---

## 5. Phase 1 Acceptance Criteria

- [ ] Repository structure strictly matches Section 7 of the specification.
- [ ] `SKILL.md` follows the Agent Skills specification with valid YAML frontmatter.
- [ ] `git-status.py` correctly discovers repo root, branch, HEAD, staged/unstaged/untracked files, and rebase/merge states.
- [ ] `analyze-diff.py` extracts diff statistics, truncates oversized diffs, and redacts sensitive patterns.
- [ ] `validate-commit.py` validates Conventional Commits, identifies format violations, and outputs constructive suggestions.
- [ ] `summarize-history.py` extracts scopes, types, and convention patterns from git history.
- [ ] All Python scripts run on Python 3.8+ standard library without external dependencies.
- [ ] All unit tests pass cleanly with `pytest`.
- [ ] Git safety rules (no automatic push, no history rewrite, mandatory user approval) are fully codified in skill instructions.

