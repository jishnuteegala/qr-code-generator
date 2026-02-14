import pytest
from qr_code_generator.plugins.payload.base import (
    PhonePayload, VCardPayload, MeCardPayload,
    WiFiPayload, URLPayload, SMSPayload, EmailPayload
)


class TestPayloadGenerators:
    def test_phone_payload(self):
        payload = PhonePayload()
        assert payload.name == "phone"
        result = payload.generate({'Phone': '+441234567890'})
        assert "Phone: +441234567890" in result

    def test_vcard_payload(self):
        payload = VCardPayload()
        assert payload.name == "vcard"
        result = payload.generate({
            'Phone': '+441234567890',
            'Name': 'John Smith',
            'Email': 'john@example.com'
        })
        assert "BEGIN:VCARD" in result
        assert "FN:John Smith" in result
        assert "TEL:+441234567890" in result

    def test_mecard_payload(self):
        payload = MeCardPayload()
        assert payload.name == "mecard"
        result = payload.generate({
            'Phone': '+441234567890',
            'Name': 'John Smith',
            'Email': 'john@example.com'
        })
        assert "MECARD:" in result
        assert "TEL:+441234567890" in result

    def test_wifi_payload(self):
        payload = WiFiPayload()
        assert payload.name == "wifi"
        result = payload.generate({
            'SSID': 'TestNetwork',
            'Password': 'testpass',
            'Encryption': 'WPA'
        })
        assert "WIFI:" in result
        assert "S:TestNetwork" in result
        assert "P:testpass" in result

    def test_wifi_payload_no_password(self):
        payload = WiFiPayload()
        result = payload.generate({'SSID': 'OpenNetwork'})
        assert "WIFI:" in result
        assert "P:" not in result

    def test_url_payload(self):
        payload = URLPayload()
        assert payload.name == "url"
        result = payload.generate({'URL': 'https://example.com'})
        assert result == "https://example.com"

    def test_url_payload_auto_https(self):
        payload = URLPayload()
        result = payload.generate({'URL': 'example.com'})
        assert result == "https://example.com"

    def test_sms_payload(self):
        payload = SMSPayload()
        assert payload.name == "sms"
        result = payload.generate({
            'Phone': '+441234567890',
            'Message': 'Hello'
        })
        assert "smsto:+441234567890" in result
        assert "Hello" in result

    def test_email_payload(self):
        payload = EmailPayload()
        assert payload.name == "email"
        result = payload.generate({
            'Email': 'test@example.com',
            'Subject': 'Test Subject',
            'Body': 'Test Body'
        })
        assert "mailto:test@example.com" in result
        assert "subject=Test Subject" in result
        assert "body=Test Body" in result

    def test_payload_validate_missing_column(self):
        payload = VCardPayload()
        valid, error = payload.validate({})
        assert valid is False
        assert error is not None
        assert "Phone" in error

    def test_payload_validate_valid(self):
        payload = VCardPayload()
        valid, error = payload.validate({
            'Phone': '+441234567890',
        })
        assert valid is True
