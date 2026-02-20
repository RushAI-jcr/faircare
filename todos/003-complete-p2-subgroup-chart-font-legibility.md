---
status: complete
priority: p2
issue_id: "003"
tags: [code-review, quality, visualization, ux]
dependencies: []
---

# Raise subgroup chart label font legibility

## Problem Statement

Subgroup bar charts currently render some visible chart text at 11px, which is below the package’s publication-style readability target and can be hard to read in HTML/PDF exports.

## Findings

- Automated Playwright audit on generated production-candidate reports shows minimum visible chart text size of 11px.
- Under-12px text appears in subgroup charts (`race_*`, `sex_*`, `age_group_*`) for axis/group labels.
- Source code sets x-axis tick font to 11 in subgroup bar utility:
  - `src/faircareai/visualization/governance_dashboard.py:1499`

## Proposed Solutions

### Option 1: Standardize subgroup ticks to ≥13px (recommended)

**Approach:** Increase subgroup x-axis tick font from 11 to 13, keep 13+ for y-axis/title, and adjust bottom margin/tick angle as needed.

**Pros:**
- Immediate readability improvement
- Minimal code changes

**Cons:**
- May need slightly more bottom margin for long labels

**Effort:** 1-2 hours

**Risk:** Low

---

### Option 2: Adaptive font sizing by label density

**Approach:** Compute tick size dynamically based on group count and max label length.

**Pros:**
- Better handling for varying group cardinality

**Cons:**
- More complexity and tuning

**Effort:** 3-5 hours

**Risk:** Medium

---

### Option 3: Keep size, abbreviate/wrap labels

**Approach:** Preserve current font size, shorten labels and add hover/full labels.

**Pros:**
- Avoids layout growth

**Cons:**
- Reduced immediate readability

**Effort:** 2-4 hours

**Risk:** Medium

## Recommended Action

Implemented Option 1 with validation: subgroup x-axis labels were made more readable while preserving layout safety across HTML and static exports.

## Technical Details

**Affected files:**
- `src/faircareai/visualization/governance_dashboard.py:1499`
- `tests/test_visualization_audit.py`

**Related components:**
- Governance subgroup charts (HTML/PDF/PPTX/PNG)

**Database changes (if any):**
- No

## Resources

- Playwright visual audit artifacts: `/tmp/faircareai_release_audit_prod`
- Generated report checked: `/tmp/faircareai_release_audit_prod/report_data_scientist.html`

## Acceptance Criteria

- [x] Minimum visible chart text in subgroup figures is >= 12px (target >= 13px)
- [x] No new text overlap introduced in subgroup charts
- [x] HTML/PDF/PNG tests pass
- [x] Visual audit confirms improved readability

## Work Log

### 2026-02-20 - Initial Discovery

**By:** Codex

**Actions:**
- Ran Playwright font-size audit across DS and governance reports
- Identified repeated 11px visible text in subgroup visuals
- Traced source configuration to subgroup chart x-axis tick font

**Learnings:**
- Legibility issue is configuration-level and can be addressed surgically

### 2026-02-20 - Fix Implemented

**By:** Codex

**Actions:**
- Updated subgroup chart typography/layout settings in `src/faircareai/visualization/governance_dashboard.py`
- Re-generated reports and re-ran Playwright geometry checks
- Confirmed minimum visible chart font is now 12px with no under-12 chart text

**Learnings:**
- Increasing label readability required coordinated spacing updates (tick angle + margins), not font size alone

## Notes

- Prioritize governance persona readability for committee-facing outputs.
