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
            ("Inquiries or report issue", model_overview.get("inquiries_or_report_issue")),
            ("Release stage", model_overview.get("release_stage")),
            ("Release date", model_overview.get("release_date")),
            ("Version", model_overview.get("version")),
            ("Global availability", model_overview.get("global_availability")),
            ("Regulatory approval", model_overview.get("regulatory_approval")),
            ("Summary", model_overview.get("summary")),
            ("Keywords", model_overview.get("keywords")),
        ],
    )

    uses = card.get("uses_and_directions", {})
    lines += _section_lines(
        "Uses and Directions",
        [
            ("Intended use and workflow", uses.get("intended_use_and_workflow")),
            ("Primary intended users", uses.get("primary_intended_users")),
            ("How to use", uses.get("how_to_use")),
            ("Targeted patient population", uses.get("targeted_patient_population")),
            ("Cautioned out-of-scope settings", uses.get("cautioned_out_of_scope_settings")),
        ],
    )

    warnings = card.get("warnings", {})
    lines += _section_lines(
        "Warnings",
        [
            ("Known risks and limitations", warnings.get("known_risks_and_limitations")),
            (
                "Known biases or ethical considerations",
                warnings.get("known_biases_or_ethical_considerations"),
            ),
            ("Clinical risk level", warnings.get("clinical_risk_level")),
        ],
    )

    trust = card.get("trust_ingredients", {})
    ai_facts = trust.get("ai_system_facts", {})
    lines += _section_lines(
        "Trust Ingredients",
        [
            ("Outcomes and outputs", ai_facts.get("outcomes_and_outputs")),
            ("Model type", ai_facts.get("model_type")),
            ("Foundation models used", ai_facts.get("foundation_models_used")),
            ("Input data source", ai_facts.get("input_data_source")),
            ("Output/Input data type", ai_facts.get("output_input_data_type")),
            ("Development data characterization", ai_facts.get("development_data_characterization")),
            ("Bias mitigation approaches", ai_facts.get("bias_mitigation_approaches")),
            ("Ongoing maintenance", ai_facts.get("ongoing_maintenance")),
            ("Security and compliance environment", ai_facts.get("security_and_compliance_environment")),
            (
                "Transparency mechanisms",
                ai_facts.get("transparency_intelligibility_accountability_mechanisms"),
            ),
        ],
    )

    transparency = card.get("transparency_information", {})
    lines += _section_lines(
        "Transparency Information",
        [
            (
                "Funding source of technical implementation",
                transparency.get("funding_source_of_technical_implementation"),
            ),
            ("Third-party information", transparency.get("third_party_information")),
            (
                "Stakeholders consulted during design",
                transparency.get("stakeholders_consulted_during_design"),
            ),
        ],
    )

    key_metrics = card.get("key_metrics", {})
    lines.append("## Key Metrics")
    for section, metrics in key_metrics.items():
        lines.append(f"### {section.replace('_', ' ').title()}")
        if isinstance(metrics, dict):
            lines.append(f"- **Goal of metrics**: {_format_value(metrics.get('goal_of_metrics'))}")
            lines.append(f"- **Result**: {_format_value(metrics.get('result'))}")
            lines.append(f"- **Interpretation**: {_format_value(metrics.get('interpretation'))}")
            lines.append(f"- **Test type**: {_format_value(metrics.get('test_type'))}")
            lines.append(
                f"- **Testing data description**: {_format_value(metrics.get('testing_data_description'))}"
            )
            lines.append(
                "- **Validation process and justification**: "
                f"{_format_value(metrics.get('validation_process_and_justification'))}"
            )
        else:
            lines.append(f"- {_format_value(metrics)}")
        lines.append("")

    resources = card.get("resources", {})
    lines += _section_lines(
        "Resources",
        [
            ("Evaluation references", resources.get("evaluation_references")),
            ("Clinical trials", resources.get("clinical_trials")),
            ("Peer reviewed publications", resources.get("peer_reviewed_publications")),
            ("Reimbursement status", resources.get("reimbursement_status")),
            ("Patient consent or disclosure", resources.get("patient_consent_or_disclosure")),
            (
                "Stakeholders consulted during design",
                resources.get("stakeholders_consulted_during_design"),
            ),
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
