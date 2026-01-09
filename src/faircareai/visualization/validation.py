"""Shared validation utilities for visualization functions."""

from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go
import polars as pl

if TYPE_CHECKING:
    pass

from .themes import SEMANTIC_COLORS, TYPOGRAPHY


def validate_required_columns(
    df: pl.DataFrame,
    required: list[str],
) -> list[str]:
    """Check for required columns, return list of missing.

    Args:
        df: DataFrame to validate
        required: Required column names

    Returns:
        List of missing column names (empty if all present)
    """
    return [col for col in required if col not in df.columns]


def create_error_figure(
    message: str,
    title: str = "Error",
) -> go.Figure:
    """Create standardized error figure with message.

    Args:
        message: Error message to display
        title: Figure title

    Returns:
        Plotly Figure with error annotation
    """
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        font={"size": TYPOGRAPHY["body_size"], "color": SEMANTIC_COLORS["fail"]},
        xanchor="center",
        yanchor="middle",
    )
    fig.update_layout(
        title=title,
        xaxis={"visible": False},
        yaxis={"visible": False},
        template="faircareai",
    )
    return fig


def validate_metric_exists(
    df: pl.DataFrame,
    metric: str,
) -> str | None:
    """Check if metric column exists in dataframe.

    Args:
        df: DataFrame to check
        metric: Metric column name

    Returns:
        Error message if missing, None if valid
    """
    if metric not in df.columns:
        available = [c for c in df.columns if c not in ["group", "n", "attribute"]]
        return f"Metric '{metric}' not found. Available metrics: {', '.join(available[:5])}"
    return None
