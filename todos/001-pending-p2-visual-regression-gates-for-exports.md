---
status: pending
priority: p2
issue_id: "001"
tags: [code-review, quality, visualization, release]
dependencies: []
---

# Add visual regression gates for HTML/PNG/PPTX exports

## Problem Statement

Release quality currently relies on functional tests and spot checks for charts/exports, but there is no deterministic regression gate that compares rendered output across versions. For a healthcare-facing package, visual drift (overlap, clipping, unreadable labels) should be caught before release.

## Findings

- Full test suite passes (`1213 passed, 2 skipped`), and export tests pass, but they do not maintain screenshot baselines for all persona outputs.
- A generated release audit run produced all outputs successfully (`/tmp/faircareai_release_audit_final`), confirming functionality but not long-term layout stability.
- Playwright checks found no console errors, but this is not equivalent to baseline diffing.

## Proposed Solutions

### Option 1: Add baseline screenshot tests (recommended)

**Approach:** Add deterministic synthetic fixtures and baseline screenshots for key HTML sections and PNG bundles; compare via perceptual threshold in CI.

**Pros:**
- Catches clipping/overlap/font regressions early
- Repeatable release gate

**Cons:**
- Baseline maintenance overhead
- CI artifacts grow

**Effort:** 1-2 days

**Risk:** Medium

---

### Option 2: Add chart-level geometry assertions only

**Approach:** Assert text bounding boxes and margins programmatically for Plotly figures without image diffs.

**Pros:**
- Faster CI
- No binary baselines

**Cons:**
- Can miss color/contrast/spacing regressions

**Effort:** 4-8 hours

**Risk:** Medium

---

### Option 3: Manual release checklist only

**Approach:** Keep manual visual QA in release SOP.

**Pros:**
- No engineering cost

**Cons:**
- Human error risk
- Not scalable

**Effort:** 1-2 hours per release

**Risk:** High

## Recommended Action


## Technical Details

**Affected files:**
- `tests/test_visualization_audit.py`
- `tests/test_exporters.py`
- `scripts/test_playwright_charts.py`
- `.github/workflows/ci.yml`

**Related components:**
- Plotly HTML report rendering
- PNG bundle export pipeline
- PPTX chart embedding

**Database changes (if any):**
- No

## Resources

- **CI workflow:** `.github/workflows/ci.yml`
- **Current visual tests:** `tests/test_visualization_audit.py`
- **Manual/automation script:** `scripts/test_playwright_charts.py`

## Acceptance Criteria

- [ ] Add deterministic synthetic fixture for export QA
- [ ] Add baseline or geometry-based visual regression checks for HTML + PNG + PPTX representative outputs
- [ ] Wire checks into CI release path
- [ ] Document visual QA process in docs
- [ ] Tests pass in CI

## Work Log

### 2026-02-20 - Initial Discovery

**By:** Codex

**Actions:**
- Ran full suite and export validations
- Generated end-to-end release artifacts for both personas
- Assessed current visual checks vs release-grade regression gating

**Learnings:**
- Functional coverage is strong; regression diffing is the remaining gap for world-class release assurance

## Notes

- Keep visual fixtures small and deterministic to reduce CI flakiness.
