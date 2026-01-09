"""Centralized validation and safe computation utilities.

This module provides reusable validation functions and safe computation
helpers used across the FairCareAI metrics modules. Centralizing these
utilities reduces code duplication and ensures consistent behavior.

Usage:
    from faircareai.core.validation import safe_divide, validate_probability_array

    sensitivity = safe_divide(tp, tp + fn)
    validate_probability_array(y_prob)
"""

from __future__ import annotations

import numpy as np


def safe_divide(
    numerator: float,
    denominator: float,
    default: float = 0.0,
) -> float:
    """Safely divide two numbers, returning default if denominator is zero.

    This utility eliminates the repetitive pattern of:
        x / y if y > 0 else 0.0

    Args:
        numerator: The dividend.
        denominator: The divisor.
        default: Value to return if denominator is zero or negative.

    Returns:
        numerator / denominator if denominator > 0, else default.

    Examples:
        >>> safe_divide(10, 5)
        2.0
        >>> safe_divide(10, 0)
        0.0
        >>> safe_divide(10, 0, default=-1.0)
        -1.0
    """
    return numerator / denominator if denominator > 0 else default


def validate_probability_array(y_prob: np.ndarray) -> None:
    """Validate that probabilities are in the valid [0, 1] range.

    Args:
        y_prob: Array of predicted probabilities.

    Raises:
        ValueError: If any probability is outside [0, 1] range.

    Examples:
        >>> validate_probability_array(np.array([0.1, 0.5, 0.9]))  # OK
        >>> validate_probability_array(np.array([0.1, 1.5]))  # Raises ValueError
    """
    if np.any((y_prob < 0) | (y_prob > 1)):
        raise ValueError("Probabilities must be in [0, 1] range")


def validate_binary_array(y: np.ndarray) -> None:
    """Validate that an array contains only binary values (0 or 1).

    Ignores NaN values during validation.

    Args:
        y: Array of binary labels.

    Raises:
        ValueError: If non-binary values (other than NaN) are present.

    Examples:
        >>> validate_binary_array(np.array([0, 1, 1, 0]))  # OK
        >>> validate_binary_array(np.array([0, 1, 2]))  # Raises ValueError
    """
    unique_vals = np.unique(y[~np.isnan(y)])
    if not np.all(np.isin(unique_vals, [0, 1])):
        raise ValueError("Array must contain only 0 or 1 values")


def validate_threshold(threshold: float) -> None:
    """Validate that a decision threshold is in valid range.

    Args:
        threshold: Decision threshold value.

    Raises:
        ValueError: If threshold is outside (0, 1) range.

    Examples:
        >>> validate_threshold(0.5)  # OK
        >>> validate_threshold(1.5)  # Raises ValueError
    """
    if not 0 < threshold < 1:
        raise ValueError(f"Threshold must be in (0, 1), got {threshold}")


def validate_sample_size(
    n: int,
    min_size: int,
    context: str = "computation",
) -> None:
    """Validate that sample size meets minimum requirements.

    Args:
        n: Actual sample size.
        min_size: Minimum required sample size.
        context: Description for error message.

    Raises:
        ValueError: If sample size is below minimum.

    Examples:
        >>> validate_sample_size(100, 50)  # OK
        >>> validate_sample_size(10, 50)  # Raises ValueError
    """
    if n < min_size:
        raise ValueError(f"Insufficient sample size for {context}: n={n} < {min_size}")
