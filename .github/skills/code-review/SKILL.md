---
name: code-review
description: >
  Review code for bugs, security vulnerabilities, performance issues, and style
  problems. Provide actionable feedback with severity levels and fix suggestions.
  Use when the user asks to review, audit, or check code quality, or wants a
  second pair of eyes on a pull request, diff, or code change.
license: MIT
metadata:
  author: welcome
  version: "1.0"
---

# Code Review

## When to use this skill

Use this skill when the user needs to:
- Review code for correctness, bugs, or logic errors
- Audit code for security vulnerabilities
- Check for performance issues or anti-patterns
- Review a pull request or diff
- Get feedback on code style and maintainability
- Validate error handling and edge cases

## Review Process

Follow this checklist for every review. Check categories in order of severity.

### 1. Security (Critical)

- [ ] **SQL injection**: All queries use parameterized statements, never string concatenation
- [ ] **XSS**: User input is escaped/sanitized before rendering in HTML
- [ ] **Authentication**: Every endpoint that needs auth has it; tokens are validated properly
- [ ] **Authorization**: Users can only access their own resources; IDOR checks are in place
- [ ] **Secrets**: No hardcoded passwords, API keys, or tokens in source code
- [ ] **Input validation**: All external input is validated at system boundaries
- [ ] **Error messages**: Errors don't leak internal details (stack traces, DB schemas, file paths)
- [ ] **Dependencies**: No known vulnerable versions (check CVEs for major deps)

### 2. Correctness (High)

- [ ] **Logic errors**: Conditions, loops, and branches produce correct results for all inputs
- [ ] **Edge cases**: Empty inputs, null values, boundary conditions, zero-length collections
- [ ] **Off-by-one**: Array indices, loop bounds, pagination offsets
- [ ] **Race conditions**: Shared state in concurrent code is properly synchronized
- [ ] **Error handling**: Errors are caught at the right level; resources are cleaned up (files, connections)
- [ ] **Type safety**: No implicit type coercions that could cause silent failures

### 3. Performance (Medium)

- [ ] **N+1 queries**: Database queries inside loops; should be batched or joined
- [ ] **Unnecessary computation**: Work done inside loops that could be hoisted out
- [ ] **Memory**: Large datasets loaded entirely into memory when streaming would work
- [ ] **Caching**: Repeated expensive computations that could be cached
- [ ] **Algorithmic complexity**: O(n²) or worse where O(n log n) or O(n) is possible

### 4. Maintainability (Low)

- [ ] **Naming**: Variables and functions have clear, descriptive names
- [ ] **Dead code**: Unused imports, unreachable branches, commented-out code
- [ ] **Duplication**: Repeated logic that should be extracted into a function
- [ ] **Complexity**: Functions doing too many things; deeply nested conditionals
- [ ] **Consistency**: Follows the project's existing patterns and conventions

## Output Format

For each finding, use this structure:

```markdown
### [SEVERITY] Brief title

**File**: `path/to/file.py` line 42-48
**Category**: Security | Correctness | Performance | Maintainability

**Problem**: Clear description of what's wrong and why it matters.

**Suggestion**:
```python
# Before (problematic)
query = f"SELECT * FROM users WHERE id = {user_id}"

# After (fixed)
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
```
```

Severity levels:
- **CRITICAL**: Security vulnerability or data loss risk. Must fix before merge.
- **HIGH**: Bug that will cause incorrect behavior. Should fix before merge.
- **MEDIUM**: Performance issue or code smell. Fix soon.
- **LOW**: Style or maintainability suggestion. Nice to have.

## Review Summary Template

After reviewing all code, provide a summary:

```markdown
## Review Summary

**Overall**: APPROVE / REQUEST CHANGES / NEEDS DISCUSSION

**Findings**: X critical, Y high, Z medium, W low

### Critical/High Items (must address)
1. [Brief description + location]

### Medium Items (should address)
1. [Brief description + location]

### Low Items (optional)
1. [Brief description + location]

### Positive Observations
- [Good patterns or practices noticed]
```

## Language-Specific Checks

### Python
- Mutable default arguments (`def f(items=[])` — use `None` instead)
- Bare `except:` clauses (catch specific exceptions)
- `==` vs `is` for None checks (use `is None`)
- f-strings with user input in SQL/shell commands

### JavaScript/TypeScript
- `==` vs `===` (prefer strict equality)
- Missing `await` on async functions
- Prototype pollution via unchecked object spread
- `innerHTML` with user content (use `textContent`)

### Go
- Unchecked errors (`err` assigned but not checked)
- Goroutine leaks (unbuffered channels, missing context cancellation)
- Race conditions on shared maps

### Rust
- `unwrap()` in production code (use `?` or handle the error)
- Missing `Send`/`Sync` bounds for concurrent types

## Gotchas

- **Review the change, not the whole file**: Focus on what's new or modified. Don't nitpick existing code unless it interacts with the change.
- **Severity matters more than count**: One critical security issue outweighs ten style suggestions. Lead with the most important findings.
- **Suggest, don't rewrite**: Provide enough of a fix to be clear, but don't refactor their entire approach unless asked.
- **Check the tests**: If there are tests, verify they actually test the behavior, not just run without errors. Missing tests for new behavior is a finding.
- **Consider the context**: A quick prototype has different standards than production code. Calibrate accordingly.

## Validation

After completing a review:
1. Every finding has a file location and a clear suggestion
2. Severity levels are consistent (don't call style issues "critical")
3. The summary accurately reflects the findings
4. Positive patterns are acknowledged, not just problems
