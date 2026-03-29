# Code Review — Advanced Reference

## OWASP Top 10 Quick Reference

Use this when reviewing web application code.

| # | Vulnerability | What to look for |
|---|--------------|-----------------|
| A01 | Broken Access Control | Missing auth checks, IDOR, CORS misconfig, path traversal |
| A02 | Cryptographic Failures | Plaintext passwords, weak hashing (MD5/SHA1), hardcoded keys |
| A03 | Injection | SQL, NoSQL, OS command, LDAP injection via unsanitized input |
| A04 | Insecure Design | Missing rate limiting, no abuse case modeling |
| A05 | Security Misconfiguration | Debug mode in prod, default credentials, verbose errors |
| A06 | Vulnerable Components | Outdated deps with known CVEs |
| A07 | Auth Failures | Weak passwords allowed, missing brute-force protection, session fixation |
| A08 | Data Integrity Failures | Unsigned updates, insecure deserialization, unverified CI/CD |
| A09 | Logging Failures | Missing audit logs, logging sensitive data, no alerting |
| A10 | SSRF | Unvalidated URLs in server-side requests |

## Common Anti-Patterns by Language

### Python

```python
# ❌ Mutable default argument
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ Fixed
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

```python
# ❌ Bare except swallows all errors including KeyboardInterrupt
try:
    do_something()
except:
    pass

# ✅ Catch specific exceptions
try:
    do_something()
except (ValueError, TypeError) as e:
    logger.warning("Failed: %s", e)
```

### JavaScript

```javascript
// ❌ Prototype pollution
function merge(target, source) {
  for (const key in source) {
    target[key] = source[key]; // __proto__ can be overwritten
  }
}

// ✅ Safe merge
function merge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === '__proto__' || key === 'constructor') continue;
    target[key] = source[key];
  }
}
```

```javascript
// ❌ XSS via innerHTML
element.innerHTML = userInput;

// ✅ Use textContent for plain text
element.textContent = userInput;
```

### SQL

```python
# ❌ SQL injection
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ Parameterized query
cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
```

## Performance Review Patterns

### N+1 Query Detection

```python
# ❌ N+1: one query per order
orders = Order.objects.all()
for order in orders:
    customer = Customer.objects.get(id=order.customer_id)  # N queries

# ✅ Eager loading
orders = Order.objects.select_related("customer").all()  # 1 query
```

### Unnecessary Work in Loops

```python
# ❌ Regex compiled on every iteration
for line in lines:
    match = re.search(r"\d{4}-\d{2}-\d{2}", line)

# ✅ Compile once
date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
for line in lines:
    match = date_pattern.search(line)
```

## Review Comment Templates

### For PRs/Diffs

```markdown
## PR Review: #123 — Add user authentication

**Reviewed**: src/auth.py, src/middleware.py, tests/test_auth.py
**Verdict**: REQUEST CHANGES

### Must Fix
1. **[CRITICAL]** `src/auth.py:45` — JWT secret is hardcoded. Move to environment variable.
2. **[HIGH]** `src/auth.py:78` — Token expiry not checked. Expired tokens are accepted.

### Should Fix
3. **[MEDIUM]** `src/middleware.py:23` — Auth check runs a DB query per request. Cache the user lookup.

### Suggestions
4. **[LOW]** `src/auth.py:12` — Consider using `python-jose` instead of manually parsing JWTs.

### Good
- Clean separation of auth logic from business logic
- Tests cover both happy path and invalid token cases
```
