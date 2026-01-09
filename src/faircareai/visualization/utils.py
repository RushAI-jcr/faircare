"""Shared utility functions for visualization modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go

if TYPE_CHECKING:
    pass

# Import Van Calster constants from core.constants
from faircareai.core.constants import (
    VANCALSTER_ALL_CAUTION,
    VANCALSTER_ALL_OPTIONAL,
    VANCALSTER_ALL_RECOMMENDED,
)

# Import theming constants
from faircareai.visualization.themes import (
    EDITORIAL_COLORS,
    FAIRCAREAI_BRAND,
    TYPOGRAPHY,
)


def get_metric_category(metric: str) -> str:
    """Get Van Calster category for a metric.

    Categorizes performance metrics according to the Van Calster et al. (2025)
    methodology into RECOMMENDED, OPTIONAL, CAUTION, or UNKNOWN categories.

    Args:
        metric: Metric name (case-insensitive).

    Returns:
        One of "RECOMMENDED", "OPTIONAL", "CAUTION", or "UNKNOWN".

    Example:
        >>> get_metric_category("auroc")
        "RECOMMENDED"
        >>> get_metric_category("accuracy")
        "CAUTION"
    """
    metric_lower = metric.lower()
    if metric_lower in VANCALSTER_ALL_RECOMMENDED:
        return "RECOMMENDED"
    if metric_lower in VANCALSTER_ALL_OPTIONAL:
        return "OPTIONAL"
    if metric_lower in VANCALSTER_ALL_CAUTION:
        return "CAUTION"
    return "UNKNOWN"


def add_source_annotation(
    fig: go.Figure,
    source_note: str | None = None,
    citation: str | None = None,
) -> go.Figure:
    """Add FairCareAI source annotation to a figure.

    Adds a source annotation at the bottom of the figure. Optionally includes
    a methodology citation (e.g., for Van Calster plots).

    Args:
        fig: Plotly Figure object.
        source_note: Custom source note (uses brand default if None).
        citation: Optional methodology citation to append.

    Returns:
        Figure with source annotation added.

    Example:
        >>> fig = go.Figure()
        >>> add_source_annotation(fig, citation="Van Calster et al. (2025)")
    """
    effective_source = source_note if source_note is not None else FAIRCAREAI_BRAND["source_note"]

    # Add citation if provided
    if citation:
        annotation_text = f"{effective_source} | Methodology: {citation}"
    else:
        annotation_text = effective_source

    fig.add_annotation(
        text=annotation_text,
        xref="paper",
        yref="paper",
        x=0,
        y=-0.12,
        showarrow=False,
        font={"size": TYPOGRAPHY["source_size"], "color": EDITORIAL_COLORS["slate"]},
        xanchor="left",
    )
    return fig
