---
module: Governance Dashboard
date: 2026-02-20
problem_type: ui_bug
component: tooling
symptoms:
  - "Subgroup charts used unreadable x-axis labels for dense categories."
  - "ROC and probability charts showed overlapping origin tick labels at 0%."
  - "Governance PNG exports showed title and legend edge clipping risk."
root_cause: config_error
resolution_type: code_fix
severity: medium
tags: [plotly, governance-report, typography, label-overlap, png-export]
---

# Troubleshooting: Governance Chart Text Overlap and Clipping

## Problem
Governance report visuals were not publication-ready. Some labels were hard to read, origin ticks overlapped, and exported PNGs risked clipping titles/legends at figure edges.

## Environment
- Module: FairCareAI Governance Dashboard
- Stage: post-implementation release hardening
- Affected Component: Plotly governance and subgroup chart generators
- Date: 2026-02-20

## Symptoms
- Subgroup x-axis category labels were too small for dense subgroup sets.
- ROC/probability visuals displayed duplicate `0%` labels at the origin.
- Exported PNGs showed edge-contact risk around title/legend regions.

## What Didn't Work

**Attempted Solution 1:** Increase font sizes only in global plotting constants.
- **Why it failed:** Several governance figures set local axis/legend styles, so global font updates did not fully propagate.

**Attempted Solution 2:** Enable automatic margins without changing tick and title anchors.
- **Why it failed:** Auto-margins cannot resolve logical overlap from duplicate origin labels and edge-anchored titles.

## Solution

Updated `/Users/JCR/Desktop/fcpackage/src/faircareai/visualization/governance_dashboard.py` with explicit layout corrections:

- Raised subgroup x-axis tick size to readable baseline and increased label angle/spacing.
- Added title offsets and padding (`x=0.02`, non-zero title pad) to avoid edge clipping.
- Removed origin label collisions by setting non-zero x-axis tick values for ROC/probability charts.
- Standardized governance axis/legend font sizes to publication-ready defaults.

**Code changes** (representative):
```python
fig.update_xaxes(tickfont={"size": 12}, tickangle=-55)
fig.update_layout(title={"x": 0.02, "pad": {"t": 12, "l": 8, "r": 8, "b": 0}})
fig.update_xaxes(tickvals=[0.2, 0.4, 0.6, 0.8, 1.0], tickformat=".0%")
```

## Why This Works

1. The root issue was figure-level layout configuration, not only theme defaults.
2. Explicit per-figure typography/margins align chart geometry with text footprint.
3. Removing `0` from competing axis tick labels prevents duplicate-origin overlap.
4. Edge-safe title anchoring and padding preserve readability in static PNG exports.

## Prevention

- Keep a minimum chart text baseline (`>=12px`) for governance-facing outputs.
- Use explicit tick policies when axes share an origin to avoid duplicate labels.
- Include HTML and PNG visual audits in release QA for overlap/clipping checks.
- Maintain figure-level layout tests for subgroup-heavy scenarios.

## Related Issues

No related issues documented yet.
