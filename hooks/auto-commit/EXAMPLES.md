# Auto-Commit Hook Examples

Real-world examples of how the auto-commit hook behaves in different scenarios.

## Scenario 1: Feature Development with Iterations

### Initial Request
**User:** "Create a user authentication system"

**Claude's actions:**
- Creates `src/auth/login.py`
- Creates `src/auth/register.py`
- Updates `src/routes.py`

**Result:**
```
feat(src): add new functionality

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Follow-up Refinement (within 5 minutes)
**User:** "Add password strength validation"

**Claude's actions:**
- Updates `src/auth/register.py` (same file from previous commit)

**Result:**
```
[AMENDED] feat(src): add new functionality
(Previous changes + new password validation in single commit)
```

### New Feature Request (after 10 minutes)
**User:** "Add email verification"

**Claude's actions:**
- Creates `src/auth/email_verification.py`

**Result:**
```
feat(auth): add new functionality
(New commit because >5 minutes passed)
```

---

## Scenario 2: Bug Fix then Refactor

### Bug Fix
**User:** "Fix the login bug where users can't login with email"

**Claude's actions:**
- Fixes `src/auth/login.py`

**Result:**
```
fix(src): fix bugs

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Immediate Refactor (within 2 minutes)
**User:** "Refactor that fix to be cleaner"

**Claude's actions:**
- Refactors `src/auth/login.py`

**Result:**
```
[AMENDED] fix(src): fix bugs
(Amends because it's a refactor of the same file)
```

### Unrelated Refactor
**User:** "Now refactor the database connection code"

**Claude's actions:**
- Refactors `src/db/connection.py`

**Result:**
```
refactor(src): refactor code
(New commit because different files)
```

---

## Scenario 3: Documentation Updates

### Initial Documentation
**User:** "Update the README with installation instructions"

**Claude's actions:**
- Updates `README.md`

**Result:**
```
docs(README): update documentation

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Add More Docs (within 3 minutes)
**User:** "Also add a usage section"

**Claude's actions:**
- Updates `README.md` (same file)

**Result:**
```
[AMENDED] docs(README): update documentation
(Amends because same file, same type, recent)
```

### Different Documentation
**User:** "Create a CONTRIBUTING.md file"

**Claude's actions:**
- Creates `CONTRIBUTING.md`

**Result:**
```
docs: update documentation
(New commit because different file)
```

---

## Scenario 4: Test Development

### Writing Tests
**User:** "Write tests for the user model"

**Claude's actions:**
- Creates `tests/test_user.py`

**Result:**
```
test(tests): add/update tests

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Adding More Tests (within 4 minutes)
**User:** "Add edge case tests"

**Claude's actions:**
- Updates `tests/test_user.py`

**Result:**
```
[AMENDED] test(tests): add/update tests
(Amends because same file, same type)
```

### Tests for Different Module
**User:** "Write tests for the auth module"

**Claude's actions:**
- Creates `tests/test_auth.py`

**Result:**
```
test(tests): add/update tests
(New commit because different concern, even though same type)
```

---

## Scenario 5: Multi-file Refactoring

### Large Refactor
**User:** "Refactor the entire project structure"

**Claude's actions:**
- Moves `auth.py` → `src/auth/login.py`
- Moves `db.py` → `src/database/connection.py`
- Updates 5 other files with new imports

**Result:**
```
refactor(src): reorganize files

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Small Cleanup (within 2 minutes)
**User:** "Remove unused imports from those files"

**Claude's actions:**
- Updates 3 of the same files

**Result:**
```
[AMENDED] refactor(src): reorganize files
(Amends because >30% file overlap, same type, recent)
```

---

## Scenario 6: Dependency Management

### Adding Dependencies
**User:** "Add pytest and requests to the project"

**Claude's actions:**
- Updates `pyproject.toml`

**Result:**
```
build(pyproject): update dependencies

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### More Dependencies (within 1 minute)
**User:** "Also add black and mypy"

**Claude's actions:**
- Updates `pyproject.toml`

**Result:**
```
[AMENDED] build(pyproject): update dependencies
(Amends because same file, very recent)
```

---

## Scenario 7: Mixed Changes Won't Amend

### Feature Implementation
**User:** "Implement user profile page"

**Claude's actions:**
- Creates `src/profile.py`
- Updates `src/routes.py`

**Result:**
```
feat(src): add new functionality

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Bug Fix in Different Area (within 2 minutes)
**User:** "Fix the logout bug"

**Claude's actions:**
- Fixes `src/auth/logout.py`

**Result:**
```
fix(src): fix bugs
(New commit because different type: feat → fix)
```

---

## Scenario 8: After Push Protection

### Initial Work
**User:** "Add API endpoints"

**Claude's actions:**
- Creates `src/api/endpoints.py`
- Commits the changes

**Result:**
```
feat(src): add new functionality
```

### Push to Remote
```bash
$ git push origin main
```

### More Changes (within 3 minutes)
**User:** "Add error handling to those endpoints"

**Claude's actions:**
- Updates `src/api/endpoints.py`

**Result:**
```
feat(src): add new functionality
(New commit, NOT amended, because previous was pushed)
```

---

## Scenario 9: Time-based Separation

### Morning Work
**User:** "Create data models" (9:00 AM)

**Claude's actions:**
- Creates models

**Result:**
```
feat(src): add new functionality
```

### Afternoon Work
**User:** "Update those models" (2:00 PM - 5 hours later)

**Claude's actions:**
- Updates same models

**Result:**
```
feat(src): add new functionality
(New commit because >5 minutes passed)
```

---

## Scenario 10: Complex Project Organization

### Create Project Structure
**User:** "Initialize a Python project with UV"

**Claude's actions:**
- Creates `pyproject.toml`
- Creates `src/`, `tests/`
- Creates `.gitignore`
- Creates `.pre-commit-config.yaml`

**Result:**
```
feat: add new files

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

### Configure Tools (within 2 minutes)
**User:** "Update the Ruff configuration"

**Claude's actions:**
- Updates `pyproject.toml`

**Result:**
```
[AMENDED] feat: add new files
(Amends because same files touched, recent change)
```

### Add First Feature (within 5 minutes)
**User:** "Create a hello world module"

**Claude's actions:**
- Creates `src/hello.py`
- Updates `src/__init__.py`

**Result:**
```
feat(src): add new functionality
(New commit because this is a distinct feature, not project setup)
```

---

## Decision Matrix

| Condition | Last Commit Time | File Overlap | Commit Types | Result |
|-----------|-----------------|--------------|--------------|---------|
| Same files, quick fix | <5 min | >30% | Same or refactor | **AMEND** |
| Same files, later | >5 min | >30% | Same | **NEW** |
| Different files | <5 min | <30% | Same | **NEW** |
| Related files | <5 min | >30% | feat → refactor | **AMEND** |
| Different concern | <5 min | Any | feat → fix | **NEW** |
| After push | Any | Any | Any | **NEW** |
| Different author | Any | Any | Any | **NEW** |

---

## Tips for Best Results

1. **Quick iterations** - Multiple small requests within 5 minutes will be grouped
2. **Clear separation** - Wait >5 minutes or work on different areas for separate commits
3. **Refactoring** - Refactors of recent changes will be amended
4. **Push early** - Push to prevent amendments after code review
5. **Review logs** - Use `git log` to verify commit history makes sense
