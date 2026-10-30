# Pull Request Guidelines & Description Generation

A well-crafted Pull Request (PR) description provides reviewers with clear context, rationale, architectural decisions, and verification steps.

---

## 1. Core Principles of a Good PR

1. **Title Follows Conventional Commits**:
   - The PR title should summarize the overarching change using conventional commit format:
     `feat(auth): implement oauth2 authorization code flow`
2. **Context First**:
   - Clearly explain **why** this change is being made. Link relevant issue tickets (`Closes #42`).
3. **Summary of Changes**:
   - Provide a bulleted breakdown of what was modified, added, or deleted.
4. **Testing & Verification**:
   - Detail how reviewers can verify the changes, including unit tests, manual commands, and screenshots for visual changes.
5. **Breaking Changes**:
   - Highlight any breaking changes and describe upgrade paths.

---

## 2. PR Body Generation Workflow for Agents

When generating a PR description:
1. Run `scripts/summarize-history.py` over the feature branch commits relative to base branch (e.g. `main` or `master`).
2. Run `scripts/analyze-diff.py` to get full diff statistics.
3. Populate the Pull Request template located in `assets/pr-template.md`.
4. Present the drafted PR title and body to the user for review.
