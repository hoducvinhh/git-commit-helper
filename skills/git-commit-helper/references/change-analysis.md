# Semantic Change Analysis Guide

Semantic change analysis is the cognitive process of examining raw code diffs and determining the underlying developer intent.

---

## 1. Analyzing Diff Statistics

When inspecting output from `analyze-diff.py`:
- **File count & spread**: Are changes localized to a single module (e.g. `src/auth/`) or spread across unrelated packages?
- **Ratio of additions to deletions**:
  - High deletions with low additions: Often a refactoring, cleanup, or deprecation removal.
  - High additions with low deletions: Typically a new feature or added tests.
  - Symmetrical additions and deletions: Refactor, bug fix, or dependency upgrade.

---

## 2. Intent Classification Decision Matrix

Use this decision matrix to determine the primary commit type:

```
Did the public API or behavior change?
├── YES
│   ├── Is it fixing unintended/broken behavior? ──> `fix`
│   ├── Is it adding new capabilities/features? ───> `feat`
│   └── Is it removing existing capabilities? ─────> `feat!` or `refactor!` (BREAKING CHANGE)
└── NO
    ├── Are only docs/comments changed? ───────────> `docs`
    ├── Are only tests added or updated? ──────────> `test`
    ├── Are build scripts or dependencies changed? ─> `build`
    ├── Are CI/CD workflows modified? ─────────────> `ci`
    ├── Is code reorganized without behavior change? > `refactor`
    ├── Is performance improved without API change? ─> `perf`
    ├── Is whitespace or formatting updated? ───────> `style`
    └── Are internal repo configs/tools updated? ────> `chore`
```

---

## 3. Scope Resolution Strategy

1. **Path-Based Scope**:
   - `src/auth/login.py` ➔ scope: `auth`
   - `src/components/Button.tsx` ➔ scope: `components` or `ui`
   - `api/v1/routes.go` ➔ scope: `api`
2. **Feature-Based Scope**:
   - Changes across database migration and model for billing ➔ scope: `billing`
3. **Repository Precedence**:
   - Always run `scripts/summarize-history.py` to match the scope naming conventions previously accepted in the repo.
