"""CHAI Applied Model Card generator for FairCareAI audits."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from faircareai.core.results import AuditResults


def _get_override(overrides: dict[str, Any], key: str, default: Any = "Not specified") -> Any:
    value = overrides.get(key, default)
    return default if value in (None, "") else value


def _get_section(overrides: dict[str, Any], key: str) -> dict[str, Any]:
    section = overrides.get(key, {})
    return section if isinstance(section, dict) else {}


def build_chai_model_card(results: AuditResults) -> dict[str, Any]:
    """Build a CHAI Applied Model Card-aligned dict."""
    config = results.config
    overrides = getattr(config, "model_card", {}) or {}
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    run_timestamp = results.run_timestamp or config.report_date or "N/A"

    model_overview_overrides = _get_section(overrides, "model_overview")
    intended_use_overrides = _get_section(overrides, "intended_use")
    warnings_overrides = _get_section(overrides, "warnings")
    trust_overrides = _get_section(overrides, "trust_ingredients")
    transparency_overrides = _get_section(overrides, "transparency_information")
    resources_overrides = _get_section(overrides, "resources")
    key_metrics_overrides = _get_section(overrides, "key_metrics")

    gov = results.governance_recommendation or {}
    perf = results.overall_performance
    disc = perf.get("discrimination", {})
    cal = perf.get("calibration", {})
    cls = perf.get("classification_at_threshold", {})

    fairness_summary = []
    for attr_name, metrics in results.fairness_metrics.items():
        if not isinstance(metrics, dict):
            continue
        for key, value in metrics.items():
            if key.endswith("_diff") and isinstance(value, dict):
                fairness_summary.append(
                    {
                        "metric": key,
                        "attribute": attr_name,
                        "value": value,
                    }
                )

    key_metrics = {
        "usefulness_and_efficacy": key_metrics_overrides.get(
            "usefulness_and_efficacy",
            [
                {"name": "AUROC", "value": disc.get("auroc", "N/A")},
                {"name": "AUPRC", "value": disc.get("auprc", "N/A")},
                {"name": "Decision threshold", "value": results.threshold},
            ],
        ),
        "fairness_and_equity": key_metrics_overrides.get(
            "fairness_and_equity",
            [
                {"name": "Primary fairness metric", "value": _get_override(overrides, "primary_fairness_metric", config.primary_fairness_metric.value if config.primary_fairness_metric else "Not specified")},
                {"name": "Fairness flags", "value": len(results.flags)},
                {"name": "Fairness summary", "value": fairness_summary or "Not specified"},
            ],
        ),
        "safety_and_reliability": key_metrics_overrides.get(
            "safety_and_reliability",
            [
                {"name": "Brier score", "value": cal.get("brier_score", "N/A")},
                {"name": "Calibration slope", "value": cal.get("calibration_slope", "N/A")},
                {"name": "Sensitivity (TPR)", "value": cls.get("sensitivity", "N/A")},
                {"name": "Specificity", "value": cls.get("specificity", "N/A")},
            ],
        ),
    }

    card = {
        "schema_version": _get_override(overrides, "schema_version", "v0.1"),
        "schema_url": _get_override(
            overrides,
            "schema_url",
            "https://github.com/coalition-for-health-ai/mc-schema",
        ),
        "template_url": _get_override(
            overrides,
            "template_url",
            "https://mc.chai.org/v0.1/documentation.pdf",
        ),
        "generated_at": now,
        "audit_id": results.audit_id,
        "run_timestamp": run_timestamp,
        "model_overview": {
            "name": _get_override(model_overview_overrides, "name", config.model_name),
            "developer": _get_override(
                model_overview_overrides,
                "developer",
                config.organization_name or "Not specified",
            ),
            "inquiries": _get_override(model_overview_overrides, "inquiries", "Not specified"),
            "release_stage": _get_override(model_overview_overrides, "release_stage"),
            "release_date": _get_override(model_overview_overrides, "release_date", run_timestamp),
            "version": _get_override(model_overview_overrides, "version", config.model_version),
            "global_availability": _get_override(model_overview_overrides, "global_availability"),
            "regulatory_approval": _get_override(model_overview_overrides, "regulatory_approval"),
            "summary": _get_override(
                model_overview_overrides,
                "summary",
                f"Governance status: {gov.get('status', 'N/A')}. {gov.get('advisory', '')}".strip(),
            ),
            "keywords": _get_override(model_overview_overrides, "keywords", []),
        },
        "intended_use": {
            "intended_use_and_workflow": _get_override(
                intended_use_overrides, "intended_use_and_workflow", config.intended_use or "Not specified"
            ),
            "primary_intended_users": _get_override(intended_use_overrides, "primary_intended_users"),
            "how_to_use": _get_override(intended_use_overrides, "how_to_use"),
            "targeted_patient_population": _get_override(
                intended_use_overrides, "targeted_patient_population", config.intended_population or "Not specified"
            ),
            "out_of_scope_settings": _get_override(
                intended_use_overrides, "out_of_scope_settings", config.out_of_scope or []
            ),
        },
        "warnings": {
            "risks_and_limitations": _get_override(
                warnings_overrides,
                "risks_and_limitations",
                f"{len(results.flags)} audit flags raised." if results.flags else "No flags raised.",
            ),
            "biases_and_ethical_considerations": _get_override(
                warnings_overrides,
                "biases_and_ethical_considerations",
                config.fairness_justification or "Not specified",
            ),
            "clinical_risk_level": _get_override(warnings_overrides, "clinical_risk_level"),
        },
        "trust_ingredients": {
            "ai_system_facts": _get_override(trust_overrides, "ai_system_facts", {}),
            "model_type": _get_override(trust_overrides, "model_type", config.model_type.value),
            "use_case_type": _get_override(
                trust_overrides,
                "use_case_type",
                config.use_case_type.value if config.use_case_type else "Not specified",
            ),
            "input_data": _get_override(trust_overrides, "input_data"),
            "outputs": _get_override(trust_overrides, "outputs"),
            "development_data": _get_override(trust_overrides, "development_data"),
            "evaluation_data": _get_override(trust_overrides, "evaluation_data"),
            "foundation_models": _get_override(trust_overrides, "foundation_models", []),
            "bias_mitigation": _get_override(trust_overrides, "bias_mitigation"),
            "ongoing_maintenance": _get_override(trust_overrides, "ongoing_maintenance"),
            "security_and_compliance": _get_override(trust_overrides, "security_and_compliance"),
            "transparency_mechanisms": _get_override(
                trust_overrides,
                "transparency_mechanisms",
                ["FairCareAI audit report", "Governance report", "RAIC evidence checklist"],
            ),
        },
        "transparency_information": {
            "funding_source": _get_override(transparency_overrides, "funding_source"),
            "third_party_info": _get_override(transparency_overrides, "third_party_info"),
            "stakeholders_consulted": _get_override(transparency_overrides, "stakeholders_consulted"),
        },
        "key_metrics": key_metrics,
        "resources": {
            "evaluation_references": resources_overrides.get(
                "evaluation_references",
                [
                    "Van Calster et al. (2025) - Evaluation of performance measures in predictive AI models",
                    "https://github.com/benvancalster/PerfMeasuresOverview",
                    "https://www.chai.org/workgroup/responsible-ai/responsible-ai-checklists-raic",
                ],
            ),
            "clinical_trials": _get_override(resources_overrides, "clinical_trials", []),
            "publications": _get_override(resources_overrides, "publications", []),
            "reimbursement_status": _get_override(resources_overrides, "reimbursement_status"),
            "patient_consent": _get_override(resources_overrides, "patient_consent"),
            "stakeholders_consulted": _get_override(resources_overrides, "stakeholders_consulted"),
        },
        "governance": {
            "status": gov.get("status", "N/A"),
            "advisory": gov.get("advisory", "N/A"),
            "review_notes": _get_override(overrides, "governance_notes", ""),
        },
    }

    return card


def generate_chai_model_card_json(results: AuditResults, path: str | Path) -> Path:
    """Generate a CHAI-aligned model card JSON export."""
    path = Path(path)
    card = build_chai_model_card(results)
    path.write_text(json.dumps(card, indent=2, default=str), encoding="utf-8")
    return path
