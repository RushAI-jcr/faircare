"""Reproducibility utilities for FairCareAI.

Captures runtime environment metadata and audit settings to support
deterministic, auditable analyses in clinical contexts.
"""

from __future__ import annotations

import platform
import sys
from importlib import metadata


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def capture_environment() -> dict:
    """Capture environment metadata for reproducibility."""
    packages = [
        "faircareai",
        "numpy",
        "polars",
        "scipy",
        "statsmodels",
        "scikit-learn",
        "plotly",
        "altair",
        "great-tables",
        "pyarrow",
        "streamlit",
        "playwright",
        "python-pptx",
    ]
    versions = {pkg: _package_version(pkg) for pkg in packages}

    return {
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
        },
        "packages": {k: v for k, v in versions.items() if v is not None},
    }


def build_reproducibility_bundle(
    *,
    bootstrap_ci: bool,
    n_bootstrap: int,
    random_seed: int | None,
) -> dict:
    """Build a reproducibility bundle with environment + audit settings."""
    return {
        "environment": capture_environment(),
        "bootstrap_ci": bootstrap_ci,
        "n_bootstrap": n_bootstrap,
        "random_seed": random_seed,
    }
