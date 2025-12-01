"""Tests for PHI redaction helpers in the ADK.

These tests exercise the rule-based `redact_phi` implementation and are
designed to run without external dependencies.
"""
from adk import ClinicalAssistantADK


def test_redact_date_and_id():
    client = ClinicalAssistantADK()
    text = "Patient DOB: 1980-05-12; MRN: 123456789; SSN: 123-45-6789"
    redacted = client.redact_phi(text)
    assert "[REDACTED_DATE]" in redacted
    assert redacted.count("[REDACTED_ID]") >= 2


def test_redact_simple_name():
    client = ClinicalAssistantADK()
    text = "Dr. John Doe reported that Patient Jane Smith was stable."
    redacted = client.redact_phi(text)
    assert "[REDACTED_NAME]" in redacted
    # should redact multiple names
    assert redacted.count("[REDACTED_NAME]") >= 2


def test_redact_keeps_non_phi():
    client = ClinicalAssistantADK()
    text = "The patient improved. Follow-up in 2 weeks."
    redacted = client.redact_phi(text)
    # No redaction tokens should appear
    assert "[REDACTED" not in redacted
