import pytest
from qr_code_generator.core.formatter import PhoneFormatter


class TestPhoneFormatter:
    def test_format_phone_keep_plus(self):
        assert PhoneFormatter.format_phone("441234567890", keep_plus=True) == "+441234567890"
        assert PhoneFormatter.format_phone("+441234567890", keep_plus=True) == "+441234567890"

    def test_format_phone_no_keep_plus(self):
        assert PhoneFormatter.format_phone("+441234567890", keep_plus=False) == "+441234567890"
        assert PhoneFormatter.format_phone("441234567890", keep_plus=False) == "441234567890"

    def test_format_phone_strips_whitespace(self):
        assert PhoneFormatter.format_phone("  441234567890  ") == "+441234567890"

    def test_normalize_phone(self):
        assert PhoneFormatter.normalize_phone("+441234567890") == "+441234567890"
        result = PhoneFormatter.normalize_phone("00441234567890")
        assert result == "+441234567890"
        result = PhoneFormatter.normalize_phone("01234567890")
        assert result == "+1234567890"

    def test_validate_phone_valid(self):
        assert PhoneFormatter.validate_phone("+441234567890") == (True, None)
        assert PhoneFormatter.validate_phone("1234567890") == (True, None)

    def test_validate_phone_empty(self):
        valid, error = PhoneFormatter.validate_phone("")
        assert valid is False
        assert error is not None
        assert "empty" in error.lower()

    def test_validate_phone_too_short(self):
        valid, error = PhoneFormatter.validate_phone("123")
        assert valid is False
        assert error is not None
        assert "7 digits" in error

    def test_validate_phone_too_long(self):
        valid, error = PhoneFormatter.validate_phone("+" + "1" * 20)
        assert valid is False
        assert error is not None
        assert "15 digits" in error
