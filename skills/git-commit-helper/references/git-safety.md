# Git Safety Rules & Forbidden Operations

Version control is the source of truth for software projects. Unchecked or reckless Git actions can cause catastrophic data loss, credential leaks, or corrupted history. The following safety boundaries are absolute and must never be breached by the AI agent.

---

## 1. Strictly Forbidden Autonomous Operations

The AI agent is **never** permitted to run the following commands autonomously without explicit, direct user instructions:

| Forbidden Command | Risk | Policy |
| :--- | :--- | :--- |
| `git push` | Pushing untested code to remote servers or shared branches. | Requires explicit user command to push. |
| `git push --force` / `-f` | Overwriting remote history and destroying collaborators' commits. | **Strictly Forbidden.** |
| `git reset --hard` | Irrevocably destroys uncommitted working tree changes. | **Strictly Forbidden** without explicit prompt confirmation. |
| `git clean -fd` | Deletes all untracked files irreversibly. | Requires user confirmation of exact deleted paths. |
| `git commit --amend` | Rewrites the previous commit hash; dangerous on published commits. | Forbidden on commits that have been pushed upstream. |
| `git rebase` | History rewrite that can produce messy conflict loops. | Forbidden without explicit user guidance. |

---

## 2. Prohibition of Blind Staging (`git add .`)

### The Danger:
Running `git add .` or `git add -A` stages every file in the directory tree indiscriminately. This frequently stages:
- `.env` files containing production API keys and database passwords.
- Temporary debugging scripts and log files (`test.py`, `debug.log`).
- Huge binary assets, virtual environment folders (`node_modules`, `venv`).
- Unrelated work in progress.

### The Rule:
- **Always stage specific files explicitly**:
  ```bash
  git add src/auth.py tests/test_auth.py
  ```
- If the user explicitly asks to stage everything, first run `git status` or `git-status.py` and inspect all untracked files to verify no sensitive or unexpected files exist.

---

## 3. Mandatory Human-in-the-Loop Authorization

Under NO circumstances may an AI agent commit code without presenting the staged files and the commit message to the user first.

The user must have the opportunity to:
1. Review the exact message.
2. Verify the staged file list.
3. Abort or request adjustments.

---

## 4. Subprocess Security & Argument Escaping

All helper scripts in this toolkit execute external commands with:
- `shell=False`
- Commands split into discrete list arguments: `["git", "diff", "--numstat"]`.
- No raw string interpolation or shell piping that could enable command injection.
