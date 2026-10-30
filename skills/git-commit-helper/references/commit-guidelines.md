# Guidelines for Writing Clear, Atomic Commit Messages

A clean Git history serves as living documentation for developers, automated changelog generators, and debugging tools like `git bisect`.

---

## Principle of Atomic Commits

An atomic commit is a commit that represents a **single, indivisible unit of work**:
1. **Self-Contained**: The repository is in a working, buildable, and test-passing state before and after the commit.
2. **Focused**: Contains changes related to exactly one problem, feature, or refactoring step.
3. **Revertible**: If a regression is discovered, reverting this single commit removes only the problematic change without discarding unrelated improvements.

### Anti-Patterns to Avoid
- **"The Monolith"**: Bundling a database schema migration, an API endpoint, frontend CSS tweaks, and a typo fix in one commit.
- **"WIP commits"**: Committing half-finished syntax errors or broken tests into shared branches.
- **"Catch-all chores"**: A commit titled `chore: fixes and tweaks` modifying 40 files across 10 unrelated modules.

---

## Structure of an Effective Commit Message

```
feat(scope): short imperative summary (≤ 50-72 chars)

Explain the problem or context: Why was this change necessary?
What was broken or missing before this commit?

Explain the solution: What approach did this commit take?
Are there architectural decisions or trade-offs made?

Fixes #104
BREAKING CHANGE: (if applicable) description of migration path
```

---

## The "If Applied" Rule for Imperative Descriptions

To test if a commit message header is written in the imperative mood, complete this sentence:

> *"If applied, this commit will..."*

- :white_check_mark: *"If applied, this commit will **add password hashing algorithm**"* (`feat(auth): add password hashing algorithm`)
- :white_check_mark: *"If applied, this commit will **fix null pointer exception in parser**"* (`fix(parser): fix null pointer exception`)
- :x: *"If applied, this commit will **added password hashing**"* (Past tense - wrong)
- :x: *"If applied, this commit will **adds password hashing**"* (Present indicative - wrong)
- :x: *"If applied, this commit will **fixing null pointer exception**"* (Gerund - wrong)

---

## Summary Checklist Before Committing

- [ ] Does the commit header follow Conventional Commits?
- [ ] Is the header line ≤ 72 characters?
- [ ] Is the description in the imperative mood, lowercase, without trailing period?
- [ ] Is there a blank line between header and body?
- [ ] Are all staged files directly relevant to this single change?
- [ ] Did tests pass on the staged code?
