"""Model card generator for FairCareAI audits (CHAI Applied Model Card aligned)."""

from __future__ import annotations

from pathlib import Path

from faircareai.core.results import AuditResults
from faircareai.reports.chai_model_card import build_chai_model_card


def _format_value(value: object) -> str:
    if value is None:
        return "Not specified"
    if isinstance(value, float):
        return f"{value:.4f}"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "Not specified"
    if isinstance(value, dict):
        return "See structured section"
    return str(value)


def _section_lines(title: str, rows: list[tuple[str, object]]) -> list[str]:
    lines = [f"## {title}"]
    for label, value in rows:
        lines.append(f"- **{label}**: {_format_value(value)}")
    lines.append("")
    return lines


def generate_model_card_markdown(results: AuditResults, path: str | Path) -> Path:
    """Generate a CHAI Applied Model Card-aligned Markdown report."""
    path = Path(path)
    card = build_chai_model_card(results)

    lines: list[str] = ["# CHAI Applied Model Card (FairCareAI)", ""]

    lines += _section_lines(
        "Schema Alignment",
        [
            ("Schema version", card.get("schema_version")),
            ("Schema URL", card.get("schema_url")),
            ("Template URL", card.get("template_url")),
            ("Generated at", card.get("generated_at")),
            ("Audit ID", card.get("audit_id")),
            ("Run timestamp", card.get("run_timestamp")),
        ],
    )

    model_overview = card.get("model_overview", {})
    lines += _section_lines(
        "Model Overview",
        [
            ("Name", model_overview.get("name")),
            ("Developer", model_overview.get("developer")),
            ("Inquiries", model_overview.get("inquiries")),
            ("Release stage", model_overview.get("release_stage")),
            ("Release date", model_overview.get("release_date")),
            ("Version", model_overview.get("version")),
            ("Global availability", model_overview.get("global_availability")),
            ("Regulatory approval", model_overview.get("regulatory_approval")),
            ("Summary", model_overview.get("summary")),
            ("Keywords", model_overview.get("keywords")),
        ],
    )

    intended_use = card.get("intended_use", {})
    lines += _section_lines(
        "Uses and Directions",
        [
            ("Intended use and workflow", intended_use.get("intended_use_and_workflow")),
            ("Primary intended users", intended_use.get("primary_intended_users")),
            ("How to use", intended_use.get("how_to_use")),
            ("Targeted patient population", intended_use.get("targeted_patient_population")),
            ("Out of scope settings", intended_use.get("out_of_scope_settings")),
        ],
    )

    warnings = card.get("warnings", {})
    lines += _section_lines(
        "Warnings",
        [
            ("Risks and limitations", warnings.get("risks_and_limitations")),
            ("Biases and ethical considerations", warnings.get("biases_and_ethical_considerations")),
            ("Clinical risk level", warnings.get("clinical_risk_level")),
        ],
    )

    trust = card.get("trust_ingredients", {})
    lines += _section_lines(
        "Trust Ingredients",
        [
            ("AI system facts", trust.get("ai_system_facts")),
            ("Model type", trust.get("model_type")),
            ("Use case type", trust.get("use_case_type")),
            ("Input data", trust.get("input_data")),
            ("Outputs", trust.get("outputs")),
            ("Development data", trust.get("development_data")),
            ("Evaluation data", trust.get("evaluation_data")),
            ("Foundation models", trust.get("foundation_models")),
            ("Bias mitigation", trust.get("bias_mitigation")),
            ("Ongoing maintenance", trust.get("ongoing_maintenance")),
            ("Security and compliance", trust.get("security_and_compliance")),
            ("Transparency mechanisms", trust.get("transparency_mechanisms")),
        ],
    )

    transparency = card.get("transparency_information", {})
    lines += _section_lines(
        "Transparency Information",
        [
            ("Funding source", transparency.get("funding_source")),
            ("Third-party information", transparency.get("third_party_info")),
            ("Stakeholders consulted", transparency.get("stakeholders_consulted")),
        ],
    )

    key_metrics = card.get("key_metrics", {})
    lines.append("## Key Metrics")
    for section, metrics in key_metrics.items():
        lines.append(f"### {section.replace('_', ' ').title()}")
        if isinstance(metrics, list):
            for metric in metrics:
                if isinstance(metric, dict):
                    name = metric.get("name", "Metric")
                    value = _format_value(metric.get("value"))
                    lines.append(f"- **{name}**: {value}")
                else:
                    lines.append(f"- {metric}")
        else:
            lines.append(f"- {_format_value(metrics)}")
        lines.append("")

    resources = card.get("resources", {})
    lines += _section_lines(
        "Resources",
        [
            ("Evaluation references", resources.get("evaluation_references")),
            ("Clinical trials", resources.get("clinical_trials")),
            ("Publications", resources.get("publications")),
            ("Reimbursement status", resources.get("reimbursement_status")),
            ("Patient consent / disclosure", resources.get("patient_consent")),
            ("Stakeholders consulted", resources.get("stakeholders_consulted")),
        ],
    )

    governance = card.get("governance", {})
    lines += _section_lines(
        "Governance",
        [
            ("Status", governance.get("status")),
            ("Advisory", governance.get("advisory")),
            ("Review notes", governance.get("review_notes")),
        ],
    )

    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return path
