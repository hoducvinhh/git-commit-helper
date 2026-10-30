# Conventional Commits v1.0.0 Specification Reference

The Conventional Commits specification is a lightweight convention on top of commit messages. It provides an easy set of rules for creating an explicit commit history, making it easier to write automated tools on top of.

---

## Commit Structure

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Breaking Change Variants
A breaking change can be indicated in two ways:
1. An exclamation mark (`!`) immediately preceding the colon in the header:
   ```
   feat(api)!: remove deprecated v1 authentication endpoint
   ```
2. A `BREAKING CHANGE:` or `BREAKING-CHANGE:` token in the footer:
   ```
   feat(api): remove deprecated v1 authentication endpoint

   BREAKING CHANGE: The /v1/auth endpoint has been removed. Use /v2/auth instead.
   ```

---

## Standard Commit Types

| Type | Semantic Meaning | SemVer Bump |
| :--- | :--- | :--- |
| **`feat`** | Introduces a new user-facing feature or API capability | MINOR (0.x.0) |
| **`fix`** | Patches a bug or fixes erroneous behavior | PATCH (0.0.x) |
| **`docs`** | Documentation-only changes (README, guides, docstrings) | None |
| **`style`** | Changes that do not affect code meaning (white-space, formatting, semicolons) | None |
| **`refactor`** | Code change that neither fixes a bug nor adds a feature | None |
| **`perf`** | Code change that improves runtime performance or resource usage | PATCH |
| **`test`** | Adding missing tests or correcting existing tests | None |
| **`build`** | Changes that affect build systems or external dependencies (npm, pip, cargo) | None |
| **`ci`** | Changes to CI configuration files and scripts (GitHub Actions, GitLab CI) | None |
| **`chore`** | Other changes that don't modify `src` or test files (maintenance, tooling) | None |
| **`revert`** | Reverts a previous commit | Depends |

*Note: Any commit with a breaking change triggers a **MAJOR** version bump (x.0.0).*

---

## Scope Rules

- Scopes must be enclosed in parentheses `()` directly following the type: `feat(parser): add json support`.
- Scopes should be short, concise, and noun-based.
- Scopes should indicate the sub-system or module affected:
  - `auth`, `ui`, `database`, `api`, `cli`, `config`, `deps`.
- When multiple modules are touched, pick the primary module or omit the scope if changes span globally across the repository.

---

## Description Formatting Rules

1. **Imperative Mood**: Use imperative, present tense ("add" not "added" or "adds").
   - Correct: `feat(cli): add --json output flag`
   - Incorrect: `feat(cli): added --json output flag`
2. **Lowercase**: Do not capitalize the first letter of the description.
   - Correct: `fix(auth): prevent token expiration on refresh`
   - Incorrect: `fix(auth): Prevent token expiration on refresh`
3. **No Trailing Period**: Do not end the description with a period or punctuation.
   - Correct: `docs: update installation instructions`
   - Incorrect: `docs: update installation instructions.`
4. **Length**: Keep the entire header line under 72 characters (hard limit 100 characters).

---

## Body Formatting Rules

- Separate the body from the header with a single blank line.
- Use the body to explain the **motivation** behind the change and **how** it contrasts with previous behavior.
- Wrap lines at 72 characters where possible.

---

## Footer Formatting Rules

- Footers follow the git trailer convention: `<token>: <value>` or `<token> #<value>`.
- Examples:
  - `Reviewed-by: Jane Doe <jane@example.com>`
  - `Refs: #123, #456`
  - `Fixes: #789`
  - `BREAKING CHANGE: Environment variable DATABASE_URL is now required.`
