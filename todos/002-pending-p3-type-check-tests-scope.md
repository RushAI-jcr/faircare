---
status: pending
priority: p3
issue_id: "002"
tags: [code-review, quality, typing]
dependencies: []
---

# Decide and enforce test type-checking policy

## Problem Statement

`mypy` is strict and clean for `src`, but `tests` still produce many typing errors when checked directly. CI intentionally runs `mypy src/faircareai`, which is valid, but the policy is not explicitly documented for contributors.

## Findings

- `python3 -m mypy src` passes cleanly.
- `python3 -m mypy src tests` reports substantial test-only typing debt.
- CI currently runs `uv run mypy src/faircareai` (source-only).

## Proposed Solutions

### Option 1: Keep source-only typing, document clearly (recommended)

**Approach:** Document that strict type checks are enforced for package code only; tests are runtime-validated by pytest.

**Pros:**
- Keeps signal high
- Minimal maintenance overhead

**Cons:**
- Test typing debt remains

**Effort:** 1-2 hours

**Risk:** Low

---

### Option 2: Incrementally type tests

**Approach:** Add relaxed mypy profile for tests and gradually improve over time.

**Pros:**
- Improves test quality and editor assistance

**Cons:**
- Non-trivial sustained effort

**Effort:** 1-2 weeks (incremental)

**Risk:** Medium

---

### Option 3: Enforce strict typing for tests now

**Approach:** Fix all test typing errors and gate CI on `tests` too.

**Pros:**
- Maximum static guarantees

**Cons:**
- High effort; slows feature velocity

**Effort:** Multi-week

**Risk:** Medium

## Recommended Action


## Technical Details

**Affected files:**
- `pyproject.toml`
- `.github/workflows/ci.yml`
- `tests/*`

**Related components:**
- Contributor workflow
- CI quality gates

**Database changes (if any):**
- No

## Resources

- **CI workflow:** `.github/workflows/ci.yml`
- **Mypy config:** `pyproject.toml`

## Acceptance Criteria

- [ ] Team agrees on test typing policy
- [ ] Policy documented in `CONTRIBUTING.md`
- [ ] CI and local commands reflect documented policy

## Work Log

### 2026-02-20 - Initial Discovery

**By:** Codex

**Actions:**
- Audited static typing status for source and tests
- Confirmed CI scope is source-only

**Learnings:**
- Source typing is production-ready; tests need explicit policy to avoid confusion

## Notes

- This is not a release blocker given current CI policy.
