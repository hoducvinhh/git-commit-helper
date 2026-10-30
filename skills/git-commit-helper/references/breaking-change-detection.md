# Breaking Change Detection Heuristics

A breaking change is any modification that breaks backward compatibility for consumers of an API, library, service, CLI, or database schema.

---

## 1. Breaking Change Indicators by Domain

### A. Public APIs & Libraries
- **Function/Method Signature Alterations**:
  - Removing a parameter or reordering positional parameters.
  - Adding a required parameter without a default value.
  - Changing parameter types or return types.
  - Removing public classes, methods, functions, or exports.
  - Renaming public exports.

### B. REST & GraphQL APIs
- Removing an endpoint route (e.g., removing `DELETE /api/users/:id`).
- Changing HTTP status codes for existing endpoints.
- Making previously optional request payload fields required.
- Removing or renaming fields in JSON responses.
- Modifying authentication/authorization schemes.

### C. Database Schemas
- Dropping a table or column.
- Renaming columns without backwards-compatible views/aliases.
- Adding non-null constraints to existing columns without defaults.
- Changing primary/foreign key relationships.

### D. CLI Tools & Configuration
- Removing CLI flags or arguments.
- Changing the default value of existing flags.
- Changing exit codes or stdout output format (e.g., breaking JSON parsers).
- Renaming configuration keys in `.yaml`, `.json`, or `.toml` configs.

---

## 2. Formatting Breaking Changes in Conventional Commits

When a breaking change is identified, it MUST be signaled in the commit message:

### Option A: Header Exclamation (`!`)
```
feat(api)!: require api key for all endpoints
```

### Option B: Header Exclamation + Footer Explanation (Best Practice)
```
feat(api)!: require api key for all endpoints

All public endpoints now enforce API key validation in the Authorization header.

BREAKING CHANGE: Requests without 'Authorization: Bearer <token>' will now return HTTP 401 Unauthorized instead of 200.
```

---

## 3. Agent Verification Checklist

When analyzing a diff:
- [ ] Are any public exports or method signatures deleted or modified?
- [ ] Does any changed signature break existing caller code in `tests/`?
- [ ] If breaking, is the exclamation mark `!` included in the header?
- [ ] Is there a detailed `BREAKING CHANGE:` footer with migration advice?
