# Commit Grouping and Change Splitting

When an AI agent or developer works continuously on a codebase, working directory changes often accumulate across multiple disparate concerns. Committing all of them together creates an unreadable, non-revertible monolithic commit.

---

## 1. When to Split Commits

Split changes into separate commits whenever you identify:

1. **Unrelated Features & Fixes**: A bug fix in authentication should never be committed alongside a new profile avatar feature.
2. **Refactoring vs. Behavioral Changes**: Refactoring code structure should be committed before or after adding new behavior, never combined.
3. **Format / Style Churn**: Linting, auto-formatting, or renaming variables across multiple files should be isolated into a `style:` or `refactor:` commit.
4. **Dependency & Build Updates**: Upgrading package lockfiles or CI configs should be separate from feature code.
5. **Documentation vs. Code**: Major documentation additions or architectural docs can stand alone as `docs:`.

---

## 2. Recommended Grouping Strategy

When multiple files are modified, group them into an ordered commit plan:

### Example Scenario:
Modified files:
- `package.json` (version bump & new dependency)
- `src/utils/format.ts` (fixed regex bug)
- `tests/format.test.ts` (test for regex bug)
- `src/auth/oauth.ts` (new OAuth provider feature)
- `tests/oauth.test.ts` (tests for OAuth)
- `README.md` (documentation for OAuth)

### Logical 3-Commit Split:
1. **Commit 1 (Bug Fix)**:
   - Files: `src/utils/format.ts`, `tests/format.test.ts`
   - Message: `fix(utils): prevent regex denial of service on format`
2. **Commit 2 (Dependency Update)**:
   - Files: `package.json`, `package-lock.json`
   - Message: `build(deps): add oauth client library`
3. **Commit 3 (Feature & Docs)**:
   - Files: `src/auth/oauth.ts`, `tests/oauth.test.ts`, `README.md`
   - Message: `feat(auth): add google oauth provider support`

---

## 3. How to Execute Multi-Commit Splits

For each planned commit:
1. Stage only the specific files for that commit:
   ```bash
   git add src/utils/format.ts tests/format.test.ts
   ```
2. Commit with the validated message:
   ```bash
   git commit -m "fix(utils): prevent regex denial of service on format"
   ```
3. Repeat for the next group until the working directory is clean.
