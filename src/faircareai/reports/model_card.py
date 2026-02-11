"""Model card generator for FairCareAI audits."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from faircareai.core.results import AuditResults


def _fmt_pct(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value * 100:.1f}%"


def _fmt_num(value: float | int | None) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{value:,}"
    except Exception:
        return str(value)


def generate_model_card_markdown(results: AuditResults, path: str | Path) -> Path:
    """Generate a governance-focused model card (Markdown)."""
    path = Path(path)

    desc = results.descriptive_stats.get("cohort_overview", {})
    perf = results.overall_performance
    disc = perf.get("discrimination", {})
    cal = perf.get("calibration", {})
    cls = perf.get("classification_at_threshold", {})
    gov = results.governance_recommendation or {}

    model_name = results.config.model_name
    model_version = results.config.model_version
    intended_use = results.config.intended_use or "Not specified"
    intended_population = results.config.intended_population or "Not specified"
    out_of_scope = (
        ", ".join(results.config.out_of_scope) if results.config.out_of_scope else "Not specified"
    )
    primary_metric = (
        results.config.primary_fairness_metric.value
        if results.config.primary_fairness_metric
        else "Not specified"
    )
    fairness_justification = results.config.fairness_justification or "Not specified"
    thresholds = results.config.thresholds or {}
    flags = results.flags or []
    n_flags = len(flags)
    n_errors = len([f for f in flags if f.get("severity") == "error"])
    n_warnings = len([f for f in flags if f.get("severity") == "warning"])
    n_groups = 0
    for _attr, metrics in results.subgroup_performance.items():
        if isinstance(metrics, dict):
            groups = metrics.get("groups", {})
            n_groups += len([k for k in groups if k not in ("reference", "attribute", "threshold")])

    lines = [
        "# FairCareAI Model Card",
        "",
        "## Model Overview",
        f"- **Model name**: {model_name}",
        f"- **Model version**: {model_version}",
        f"- **Audit ID**: {results.audit_id}",
        f"- **Audit run timestamp**: {results.run_timestamp or 'N/A'}",
        f"- **Report generated**: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "",
        "## Intended Use",
        f"- **Intended use**: {intended_use}",
        f"- **Intended population**: {intended_population}",
        f"- **Out of scope**: {out_of_scope}",
        "",
        "## Data Summary",
        f"- **Samples (n)**: {_fmt_num(desc.get('n_total'))}",
        f"- **Outcome prevalence**: {desc.get('prevalence_pct', 'N/A')}",
        f"- **Sensitive attributes**: {', '.join(results.fairness_metrics.keys()) or 'Not specified'}",
        f"- **Subgroups evaluated**: {_fmt_num(n_groups)}",
        "",
        "## Performance Summary",
        f"- **AUROC**: {disc.get('auroc', 'N/A')}",
        f"- **AUPRC**: {disc.get('auprc', 'N/A')}",
        f"- **Brier score**: {cal.get('brier_score', 'N/A')}",
        f"- **Calibration slope**: {cal.get('calibration_slope', 'N/A')}",
        f"- **Sensitivity (TPR)**: {_fmt_pct(cls.get('sensitivity'))}",
        f"- **Specificity**: {_fmt_pct(cls.get('specificity'))}",
        f"- **PPV**: {_fmt_pct(cls.get('ppv'))}",
        "",
        "## Fairness Summary",
        f"- **Primary fairness metric**: {primary_metric}",
        f"- **Justification**: {fairness_justification}",
        f"- **Decision threshold**: {results.threshold:.2f}",
        f"- **Governance status**: {gov.get('status', 'N/A')}",
        f"- **Advisory**: {gov.get('advisory', 'N/A')}",
        f"- **Flags**: {n_flags} total ({n_errors} error, {n_warnings} warning)",
        "",
        "## CHAI RAIC Alignment",
        "- **AC1.CR92-93**: Primary fairness metric selected with documented justification.",
        "- **AC1.CR95**: Subgroup performance assessed for protected attributes.",
        "- **AC1.CR1-4**: Model identity, intended use, and scope documented.",
        "",
        "## Thresholds & Policy Settings",
        f"- **Minimum subgroup n**: {thresholds.get('min_subgroup_n', 'N/A')}",
        f"- **Demographic parity ratio**: {thresholds.get('demographic_parity_ratio', 'N/A')}",
        f"- **Equalized odds diff**: {thresholds.get('equalized_odds_diff', 'N/A')}",
        f"- **Calibration diff**: {thresholds.get('calibration_diff', 'N/A')}",
        f"- **Minimum AUROC**: {thresholds.get('min_auroc', 'N/A')}",
        f"- **Max missing rate**: {thresholds.get('max_missing_rate', 'N/A')}",
        "",
        "## Reproducibility",
        f"- **Random seed**: {results.random_seed if results.random_seed is not None else 'N/A'}",
        "",
        "## Governance Sign-off",
        "- **Reviewer name**: _______________________________",
        "- **Role/Title**: _______________________________",
        "- **Review date**: _______________________________",
        "- **Decision**: ☐ Approve ☐ Conditional ☐ Reject",
        "- **Comments**:",
        "",
        "## Notes",
        "This model card is generated by FairCareAI and is intended to support governance review.",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path
