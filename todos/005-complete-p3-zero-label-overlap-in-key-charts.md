---
status: complete
priority: p3
issue_id: "005"
tags: [code-review, quality, visualization]
dependencies: []
---

# Remove duplicate zero-label overlaps in key charts

## Problem Statement

A small number of charts show overlapping zero-value labels (e.g., `0%` over `0%`) at the origin, which is a minor polish issue in publication-quality outputs.

## Findings

- Playwright overlap audit detected overlap pairs in:
  - `chart-calibration`
  - `chart-roc-curve`
  - `chart-prob-dist`
- Overlaps are limited and do not break rendering, but reduce visual polish.

## Proposed Solutions

### Option 1: Suppress duplicate origin labels (recommended)

**Approach:** Configure axes/ticks to avoid duplicate `0` labels where x and y origins coincide.

**Pros:**
- Clean visual improvement
- Minimal impact to chart semantics

**Cons:**
- Small chart-specific logic required

**Effort:** 1-2 hours

**Risk:** Low

---

### Option 2: Offset one axis label layer

**Approach:** Keep both labels but offset one to prevent overlap.

**Pros:**
- Preserves both axes label sets

**Cons:**
- Can look unconventional

**Effort:** 1-2 hours

**Risk:** Low

---

### Option 3: Accept as-is

**Approach:** Document as non-blocking cosmetic artifact.

**Pros:**
- Zero engineering effort

**Cons:**
- Not ideal for world-class polish expectations

**Effort:** 0

**Risk:** Low

## Recommended Action

Implemented Option 1 by suppressing duplicate origin tick-label collisions through axis tick configuration updates in governance visual generators.

## Technical Details

**Affected files:**
- `src/faircareai/visualization/performance_charts.py`
- `src/faircareai/visualization/plots.py`

**Related components:**
- Calibration/ROC/probability distribution figure rendering

**Database changes (if any):**
- No

## Resources

- HTML analyzed: `/tmp/faircareai_release_audit_prod/report_data_scientist.html`
- Overlap audit output from Playwright (chart ids above)

## Acceptance Criteria

- [x] No overlapping duplicate zero labels in targeted charts
- [x] Chart readability unchanged or improved
- [x] Existing visualization tests remain green

## Work Log

### 2026-02-20 - Initial Discovery

**By:** Codex

**Actions:**
- Ran geometry-based overlap audit for Plotly text elements
- Isolated overlaps to duplicate zero labels in three charts

**Learnings:**
- Issue is cosmetic and localized; low-risk cleanup

### 2026-02-20 - Fix Implemented

**By:** Codex

**Actions:**
- Updated tick configuration for calibration/ROC/probability-distribution governance figures in `src/faircareai/visualization/governance_dashboard.py`
- Re-generated reports and reran overlap geometry audit
- Confirmed `overlap_pairs = 0` for both data scientist and governance HTML reports

**Learnings:**
- Duplicate-origin overlap was best resolved by axis tick selection rather than per-text manual offsets

## Notes

- Keep this behind a readability/polish milestone if higher-priority items exist.
