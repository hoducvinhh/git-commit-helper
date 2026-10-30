---
name: git-commit-helper
description: >-
  Intelligent Git workflow partner that inspects repository states, analyzes code diffs,
  validates Conventional Commits, detects breaking changes, and enforces Git safety boundaries.
---

# Git Commit Helper Skill

`git-commit-helper` transforms the AI assistant into an intelligent, disciplined, and safe Git workflow partner. It provides deterministic inspection tools and semantic analysis protocols to produce clean, atomic, and standardized Conventional Commits and Pull Requests.

---

## When to Use This Skill

Activate this skill whenever:
- Preparing commits or reviewing staged/unstaged changes.
- Writing or formatting commit messages according to Conventional Commits v1.0.0.
- Deciding how to split large, mixed, or multi-concern changes into atomic commits.
- Validating commit messages or pre-commit message checks.
- Summarizing repository commit conventions and recent commit history.
- Drafting Pull Request titles, descriptions, and changelog entries.
- Investigating Git repository state, branches, detached HEADs, or merge/rebase status.

---

## Deterministic Python Helper Scripts

This skill includes zero-dependency Python 3.8+ scripts located in `scripts/`:

| Script | Purpose | Common Invocation |
| :--- | :--- | :--- |
| `scripts/git-status.py` | Discovers repo root, branch, HEAD, unborn status, staged/unstaged files, and in-flight states (merge/rebase). | `python scripts/git-status.py [--repo-path PATH]` |
| `scripts/analyze-diff.py` | Structured diff parser with stats, truncation limits, and automated secret/credential redaction. | `python scripts/analyze-diff.py [--staged] [--max-diff-lines 500]` |
| `scripts/validate-commit.py` | Validates Conventional Commits v1.0.0 format, types, scopes, breaking changes, and grammar. | `python scripts/validate-commit.py --message "feat(api): ..."` |
| `scripts/summarize-history.py` | Analyzes recent commits to deduce repository-specific conventions, top types, and common scopes. | `python scripts/summarize-history.py [--limit 50]` |

---

## 9-Step Agent Workflow

When assisting a user with Git commits, follow this rigorous 9-step process:

```
[1. Discover State] ──> [2. Summarize History] ──> [3. Analyze Diffs]
          │
          ▼
[4. Detect Secrets] ──> [5. Group Changes] ────> [6. Formulate Commits]
          │
          ▼
[7. Validate Message] ─> [8. Human Authorization] ─> [9. Execute Commit]
```

### 1. Discover State
Execute `scripts/git-status.py` to identify:
- Is this a git repository?
- What is the current branch or HEAD commit?
- Is the branch unborn (brand new repo with 0 commits)?
- Are there in-progress operations (`merge`, `rebase`, `cherry-pick`, `revert`)?
- What files are staged, unstaged, untracked, or conflicted?

### 2. Summarize History Conventions
Execute `scripts/summarize-history.py --limit 30` to identify:
- Established commit conventions and patterns in this specific repository.
- Common scopes previously used (e.g., `auth`, `ui`, `core`, `db`).
- Compliance rate with Conventional Commits.

### 3. Analyze Diffs
Execute `scripts/analyze-diff.py` (with `--staged` if files are already staged, or without `--staged` if reviewing working directory changes):
- Review insertions, deletions, modified files, and binary files.
- Determine the semantic intent of the changes (feature, bugfix, refactor, documentation, test, etc.).

### 4. Detect Secrets and Stray Files
Carefully review the diff and file list for accidental secrets or stray files:
- Verify that no credentials, API keys, passwords, or `.env` files are included.
- Check for temporary files, build artifacts, or log files (`*.log`, `__pycache__`, `.DS_Store`).
- Alert the user immediately if any sensitive data is discovered.

### 5. Group Changes into Atomic Commits
Evaluate whether the diff represents a single logical change or multiple unrelated concerns:
- Consult [Commit Grouping Guidelines](references/commit-grouping.md).
- If unrelated changes exist (e.g., a bug fix mixed with a new feature and formatting changes), recommend splitting them into distinct, atomic commits.
- Propose an ordered commit plan to the user.

### 6. Formulate Commit Message
Craft a Conventional Commit message following [Conventional Commits v1.0.0](references/conventional-commits.md) and [Commit Guidelines](references/commit-guidelines.md):
- Choose the correct type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- Select an appropriate scope matching repository conventions.
- Write a concise, imperative description in lowercase without a trailing period.
- Check for breaking changes following [Breaking Change Detection](references/breaking-change-detection.md). Add `!` to the header and `BREAKING CHANGE: ...` in the footer if applicable.

### 7. Validate Commit Message
Run `scripts/validate-commit.py --message "..."` to programmatically ensure:
- The message conforms strictly to Conventional Commits specification.
- Header length is within limits (≤ 72 characters recommended).
- Proper blank line spacing before body and footers.

### 8. Request Human Authorization (Mandatory Safety Gate)
Present the proposed commit preview to the user using the [Commit Preview Template](assets/commit-template.md):
- Display staged files.
- Display proposed commit message (type, scope, description, body, breaking change notices).
- **Explicitly request user confirmation before running `git commit`.**

### 9. Execute Commit Safely
Once the user explicitly confirms:
- Stage only the approved files (e.g., `git add file1 file2`, never blind `git add .` unless requested).
- Execute the commit: `git commit -m "..."`.
- Run `scripts/git-status.py` to verify the commit succeeded.

---

## Safety Invariants & Forbidden Operations

Agents MUST adhere to these strict constraints at all times (see [Git Safety Guide](references/git-safety.md)):

1. **NO Autonomous Pushing**: NEVER run `git push` unless the user explicitly requests a push.
2. **NO History Rewriting**: NEVER run `git commit --amend`, `git rebase`, `git reset --hard`, or force pushes unless explicitly commanded by the user with full understanding of consequences.
3. **NO Blind Staging**: NEVER run `git add .` or `git add -A` when untracked files or potential secrets might be staged. Stage specific files explicitly.
4. **NO Silent Commits**: NEVER commit code silently in the background without user knowledge and approval.

---

## Detailed References

- [Conventional Commits Specification](references/conventional-commits.md) - Standard types, scopes, and grammar rules.
- [Writing Clear Commit Messages](references/commit-guidelines.md) - Imperative mood, atomic commits, and structure.
- [Git Safety & Security Rules](references/git-safety.md) - Forbidden commands and credential safety.
- [Semantic Change Analysis](references/change-analysis.md) - Classifying diffs by intent.
- [Breaking Change Detection](references/breaking-change-detection.md) - Heuristics for API, ABI, and schema breaking changes.
- [Commit Grouping Strategies](references/commit-grouping.md) - Techniques for splitting multi-concern diffs.
- [Pull Request Guidelines](references/pull-request-guidelines.md) - PR generation templates and standards.
- [9-Step Git Workflow Details](references/git-workflow.md) - In-depth breakdown of each workflow stage.

---

## Asset Templates

- [Commit Preview Template](assets/commit-template.md) - Standard format for presenting commits for human review.
- [Pull Request Template](assets/pr-template.md) - Standard format for generating PR descriptions.
