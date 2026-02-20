---
status: complete
priority: p2
issue_id: "004"
tags: [code-review, quality, visualization, export]
dependencies: []
---

# Reduce border-clipping risk in governance PNG exports

## Problem Statement

Several governance PNG subgroup charts render non-background pixels at image border row/column 0, indicating tight or clipped canvas margins. This can cut off titles/annotations/axes in static deliverables.

## Findings

- PNG border audit on `/tmp/faircareai_release_audit_prod/figures_governance.zip` flagged 6 charts with top/left edge contact.
- Affected charts include subgroup sensitivity/FPR PNGs for race, sex, and age group.
- Detected first non-background row/column at 0 for these files, indicating no padding safety margin.

## Proposed Solutions

### Option 1: Add figure-level export-safe margins (recommended)

**Approach:** Increase top/left margins for subgroup governance charts before PNG export and keep consistent plot area bounds.

**Pros:**
- Directly targets likely clipping source
- Keeps export pipeline simple

**Cons:**
- Slightly smaller plot area unless overall dimensions increase

**Effort:** 2-4 hours

**Risk:** Low

---

### Option 2: Add PNG post-render padding

**Approach:** Keep chart layout unchanged; add 16-24px white border around rendered PNG bytes.

**Pros:**
- Decouples from chart layout complexity
- Applies uniformly to all PNGs

**Cons:**
- Adds extra processing step
- May mask underlying layout issues

**Effort:** 2-3 hours

**Risk:** Medium

---

### Option 3: Increase export dimensions only

**Approach:** Raise default PNG width/height/scale for governance bundle.

**Pros:**
- Better readability and less crowding

**Cons:**
- Larger files
- May not fully solve edge-touching elements

**Effort:** 1-2 hours

**Risk:** Medium

## Recommended Action

Implemented Option 1 (figure-level padding/margin adjustments) and verified no edge contact in governance PNG bundle.

## Technical Details

**Affected files:**
- `src/faircareai/visualization/governance_dashboard.py`
- `src/faircareai/reports/figure_exports.py`

**Related components:**
- `to_png()` governance bundle generation
- Static figure distribution for slide/docs workflows

**Database changes (if any):**
- No

## Resources

- Export bundle analyzed: `/tmp/faircareai_release_audit_prod/figures_governance.zip`
- Sample affected files:
  - `race_-_Sensitivity_by_Subgroup.png`
  - `sex_-_FPR_by_Subgroup.png`
  - `age_group_-_Sensitivity_by_Subgroup.png`

## Acceptance Criteria

- [x] No governance subgroup PNG has first non-background row/col at 0
- [x] Visual inspection confirms no clipped text/titles/axes
- [x] PNG export tests pass
- [x] File sizes remain acceptable for sharing

## Work Log

### 2026-02-20 - Initial Discovery

**By:** Codex

**Actions:**
- Ran border-density and bounding audits on generated governance PNG bundle
- Identified six subgroup charts with edge-contacting rendered content

**Learnings:**
- Risk is concentrated in subgroup bar charts, not broad across all exports

### 2026-02-20 - Fix Implemented

**By:** Codex

**Actions:**
- Increased chart title/axis padding and subplot margins in `src/faircareai/visualization/governance_dashboard.py`
- Re-generated governance PNG bundle and reran border-edge audits
- Confirmed `potential_edge_contact_count = 0` in `/tmp/faircareai_release_audit_visualfix2/figures_governance.zip`

**Learnings:**
- Title anchoring and margin padding were the dominant contributors to edge-touching in static PNG output

## Notes

- Prefer chart-margin fix first; use post-render padding only if necessary.
