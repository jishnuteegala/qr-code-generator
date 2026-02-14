import pytest
from qr_code_generator.utils.pii_utils import PIIRedactor


class TestPIIRedactor:
    def test_mask_phone_basic(self):
        result = PIIRedactor.mask_phone("+441234567890")
        assert result.endswith("7890")
        assert "+" in result
        assert len(result) >= 10

    def test_mask_phone_short(self):
        result = PIIRedactor.mask_phone("+4412345")
        assert "+" in result

    def test_mask_email_basic(self):
        result = PIIRedactor.mask_email("john@example.com")
        assert "@" in result
        assert "example" in result or "com" in result
        assert result != "john@example.com"

    def test_redact_pii_phone(self):
        text = "Call +441234567890 for more info"
        result = PIIRedactor.redact_pii(text)
        assert "+441234567890" not in result
        assert "7890" in result

    def test_redact_pii_email(self):
        text = "Contact john@example.com please"
        result = PIIRedactor.redact_pii(text)
        assert "john@example.com" not in result

    def test_redact_pii_mixed(self):
        text = "Call +441234567890 or email john@example.com"
        result = PIIRedactor.redact_pii(text)
        assert "7890" in result
        assert "*****" in result

    def test_redact_pii_empty(self):
        assert PIIRedactor.redact_pii("") == ""
        assert PIIRedactor.redact_pii("No PII here") == "No PII here"
