"""CHAI Applied Model Card generator for FairCareAI audits (template v0.1)."""

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


def _format_flag_summary(flags: list[dict[str, Any]]) -> list[str] | str:
    if not flags:
        return "No flags raised."
    summaries = []
    for flag in flags:
        message = flag.get("message") or ""
        details = flag.get("details") or ""
        if message and details:
            summaries.append(f"{message} ({details})")
        elif message:
            summaries.append(message)
        elif details:
            summaries.append(details)
    return summaries or "Flags raised."


def _default_data_description(results: AuditResults) -> str:
    overview = results.descriptive_stats.get("cohort_overview", {})
    n_total = overview.get("n_total")
    prevalence = overview.get("prevalence_pct")
    if n_total is None and prevalence is None:
        return "Not specified"
    parts = []
    if n_total is not None:
        parts.append(f"n={n_total}")
    if prevalence is not None:
        parts.append(f"prevalence={prevalence}")
    return ", ".join(parts)


def _build_metric_section(
    overrides: dict[str, Any],
    *,
    default_goal: str,
    default_result: list[dict[str, Any]] | str,
    default_interpretation: str,
    default_test_type: str,
    default_testing_data_description: str,
    default_validation_process: str,
) -> dict[str, Any]:
    return {
        "goal_of_metrics": _get_override(overrides, "goal_of_metrics", default_goal),
        "result": _get_override(overrides, "result", default_result),
        "interpretation": _get_override(overrides, "interpretation", default_interpretation),
        "test_type": _get_override(overrides, "test_type", default_test_type),
        "testing_data_description": _get_override(
            overrides, "testing_data_description", default_testing_data_description
        ),
        "validation_process_and_justification": _get_override(
            overrides, "validation_process_and_justification", default_validation_process
        ),
    }


def build_chai_model_card(results: AuditResults) -> dict[str, Any]:
    """Build a CHAI Applied Model Card-aligned dict (template v0.1)."""
    config = results.config
    overrides = getattr(config, "model_card", {}) or {}
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    run_timestamp = results.run_timestamp or config.report_date or "N/A"

    model_overview_overrides = _get_section(overrides, "model_overview")
    uses_overrides = _get_section(overrides, "uses_and_directions")
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

    default_testing_data = _default_data_description(results)
    key_metrics = {
        "usefulness_usability_efficacy": _build_metric_section(
            _get_section(key_metrics_overrides, "usefulness_usability_efficacy"),
            default_goal="Assess clinical usefulness and model discrimination.",
            default_result=[
                {"name": "AUROC", "value": disc.get("auroc", "N/A")},
                {"name": "AUPRC", "value": disc.get("auprc", "N/A")},
                {"name": "Decision threshold", "value": results.threshold},
            ],
            default_interpretation=gov.get("status", "Not specified"),
            default_test_type=_get_override(key_metrics_overrides, "test_type", "Not specified"),
            default_testing_data_description=default_testing_data,
            default_validation_process=config.fairness_justification or "Not specified",
        ),
        "fairness_and_equity": _build_metric_section(
            _get_section(key_metrics_overrides, "fairness_and_equity"),
            default_goal="Assess parity across protected groups.",
            default_result=[
                {
                    "name": "Primary fairness metric",
                    "value": (
                        config.primary_fairness_metric.value
                        if config.primary_fairness_metric
                        else "Not specified"
                    ),
                },
                {"name": "Fairness flags", "value": len(results.flags)},
                {"name": "Fairness summary", "value": fairness_summary or "Not specified"},
            ],
            default_interpretation=gov.get("advisory", "Not specified"),
            default_test_type=_get_override(key_metrics_overrides, "test_type", "Not specified"),
            default_testing_data_description=default_testing_data,
            default_validation_process=config.fairness_justification or "Not specified",
        ),
        "safety_and_reliability": _build_metric_section(
            _get_section(key_metrics_overrides, "safety_and_reliability"),
            default_goal="Assess calibration and error tradeoffs.",
            default_result=[
                {"name": "Brier score", "value": cal.get("brier_score", "N/A")},
                {"name": "Calibration slope", "value": cal.get("calibration_slope", "N/A")},
                {"name": "Sensitivity (TPR)", "value": cls.get("sensitivity", "N/A")},
                {"name": "Specificity", "value": cls.get("specificity", "N/A")},
            ],
            default_interpretation=gov.get("status", "Not specified"),
            default_test_type=_get_override(key_metrics_overrides, "test_type", "Not specified"),
            default_testing_data_description=default_testing_data,
            default_validation_process="Not specified",
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
            "inquiries_or_report_issue": _get_override(
                model_overview_overrides, "inquiries_or_report_issue", "Not specified"
            ),
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
        "uses_and_directions": {
            "intended_use_and_workflow": _get_override(
                uses_overrides, "intended_use_and_workflow", config.intended_use or "Not specified"
            ),
            "primary_intended_users": _get_override(uses_overrides, "primary_intended_users"),
            "how_to_use": _get_override(uses_overrides, "how_to_use"),
            "targeted_patient_population": _get_override(
                uses_overrides, "targeted_patient_population", config.intended_population or "Not specified"
            ),
            "cautioned_out_of_scope_settings": _get_override(
                uses_overrides, "cautioned_out_of_scope_settings", config.out_of_scope or []
            ),
        },
        "warnings": {
            "known_risks_and_limitations": _get_override(
                warnings_overrides,
                "known_risks_and_limitations",
                _format_flag_summary(results.flags),
            ),
            "known_biases_or_ethical_considerations": _get_override(
                warnings_overrides,
                "known_biases_or_ethical_considerations",
                config.fairness_justification or "Not specified",
            ),
            "clinical_risk_level": _get_override(warnings_overrides, "clinical_risk_level"),
        },
        "trust_ingredients": {
            "ai_system_facts": {
                "outcomes_and_outputs": _get_override(
                    trust_overrides, "outcomes_and_outputs", "Not specified"
                ),
                "model_type": _get_override(
                    trust_overrides, "model_type", config.model_type.value
                ),
                "foundation_models_used": _get_override(
                    trust_overrides, "foundation_models_used", []
                ),
                "input_data_source": _get_override(
                    trust_overrides, "input_data_source", "Not specified"
                ),
                "output_input_data_type": _get_override(
                    trust_overrides, "output_input_data_type", "Not specified"
                ),
                "development_data_characterization": _get_override(
                    trust_overrides, "development_data_characterization", "Not specified"
                ),
                "bias_mitigation_approaches": _get_override(
                    trust_overrides, "bias_mitigation_approaches", "Not specified"
                ),
                "ongoing_maintenance": _get_override(
                    trust_overrides, "ongoing_maintenance", "Not specified"
                ),
                "security_and_compliance_environment": _get_override(
                    trust_overrides, "security_and_compliance_environment", "Not specified"
                ),
                "transparency_intelligibility_accountability_mechanisms": _get_override(
                    trust_overrides,
                    "transparency_intelligibility_accountability_mechanisms",
                    ["FairCareAI audit report", "Governance report", "RAIC evidence checklist"],
                ),
            }
        },
        "transparency_information": {
            "funding_source_of_technical_implementation": _get_override(
                transparency_overrides, "funding_source_of_technical_implementation"
            ),
            "third_party_information": _get_override(
                transparency_overrides, "third_party_information"
            ),
            "stakeholders_consulted_during_design": _get_override(
                transparency_overrides, "stakeholders_consulted_during_design"
            ),
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
            "peer_reviewed_publications": _get_override(
                resources_overrides, "peer_reviewed_publications", []
            ),
            "reimbursement_status": _get_override(resources_overrides, "reimbursement_status"),
            "patient_consent_or_disclosure": _get_override(
                resources_overrides, "patient_consent_or_disclosure"
            ),
            "stakeholders_consulted_during_design": _get_override(
                resources_overrides, "stakeholders_consulted_during_design"
            ),
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
