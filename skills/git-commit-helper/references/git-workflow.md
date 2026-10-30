# 9-Step Agent Git Workflow

This guide details the operational procedure for AI coding agents when managing Git version control workflows.

---

## Detailed Step-by-Step Procedure

### Step 1: Discover Repository State
Run:
```bash
python scripts/git-status.py
```
- Parse the resulting JSON.
- Verify `is_git_repository` is `true`.
- Check `is_unborn`. If true, acknowledge this is the initial commit for the repo.
- Check `in_progress_state`. If in `merge`, `rebase`, `cherry-pick`, or `revert`, inform the user immediately before taking standard commit actions.

### Step 2: Summarize History Conventions
Run:
```bash
python scripts/summarize-history.py --limit 30
```
- Inspect `types_distribution` and `scopes_distribution`.
- Adopt the repository's prevailing scope naming convention (e.g. `auth` vs `security`, `cli` vs `terminal`).
- Determine if the repository follows strict conventional commit formatting.

### Step 3: Analyze Diffs
Run:
```bash
# If changes are already staged:
python scripts/analyze-diff.py --staged

# If changes are unstaged:
python scripts/analyze-diff.py
```
- Review the modified files and line counts.
- Identify the core intent of the code modifications.

### Step 4: Detect Sensitive Data & Stray Files
Check the output of `analyze-diff.py` and `git-status.py`:
- `has_secrets_redacted`: If true, secrets were detected in the diff. Warn the user and abort committing until secrets are removed.
- Look at `untracked` files for `.env`, credentials, debug dumps, or build artifacts.

### Step 5: Group Changes into Logical Commits
- If the diff touches multiple distinct concerns (e.g., refactoring existing code + adding a new feature + fixing unrelated typo), plan multiple atomic commits.
- Specify the exact list of files belonging to each commit.

### Step 6: Formulate Commit Message
- Choose type and scope based on Step 2 and Step 3.
- Write a clean imperative description.
- Add body and breaking change notes if appropriate.

### Step 7: Validate Commit Message Programmatically
Run:
```bash
python scripts/validate-commit.py --message "feat(scope): your proposed commit message"
```
- Ensure `valid: true`. If `false`, correct the message using `suggestions` from the validator output.

### Step 8: Mandatory Human Authorization
Format the proposal using `assets/commit-template.md`:
- List of files to be committed.
- Validated commit message.
- Breaking change notices (if any).
- **Prompt the user: "Would you like me to proceed with this commit?"**

### Step 9: Execute Commit Safely
Upon receiving explicit user approval:
```bash
git add file1 file2
git commit -m "feat(scope): your proposed commit message"
```
- Verify status with `python scripts/git-status.py`.
- Report the newly created commit hash and branch to the user.
