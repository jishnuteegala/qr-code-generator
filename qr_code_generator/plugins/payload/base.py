from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from qr_code_generator.core.interfaces import QRCodeResult


class PayloadGenerator(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    def required_columns(self) -> List[str]:
        return ["Phone"]

    @property
    def optional_columns(self) -> List[str]:
        return []

    @abstractmethod
    def generate(self, data: Dict[str, Any]) -> str:
        pass

    def validate(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        for col in self.required_columns:
            if col not in data or not data[col]:
                return False, f"Missing required column: {col}"
        return True, None


class PhonePayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "phone"

    @property
    def description(self) -> str:
        return "Simple phone number payload"

    def generate(self, data: Dict[str, Any]) -> str:
        phone = data.get('Phone', '')
        return f"Phone: {phone}"


class VCardPayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "vcard"

    @property
    def description(self) -> str:
        return "vCard 3.0 format"

    @property
    def optional_columns(self) -> List[str]:
        return ["Name", "Email", "Organization", "Phone"]

    def generate(self, data: Dict[str, Any]) -> str:
        name = data.get('Name', 'Unknown')
        phone = data.get('Phone', '')
        email = data.get('Email', '')
        org = data.get('Organization', '')
        lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{name}",
            f"TEL:{phone}",
        ]
        if email:
            lines.append(f"EMAIL:{email}")
        if org:
            lines.append(f"ORG:{org}")
        lines.append("END:VCARD")
        return "\n".join(lines)


class MeCardPayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "mecard"

    @property
    def description(self) -> str:
        return "MeCard format"

    @property
    def optional_columns(self) -> List[str]:
        return ["Name", "Email"]

    def generate(self, data: Dict[str, Any]) -> str:
        name = data.get('Name', 'Unknown')
        phone = data.get('Phone', '')
        email = data.get('Email', '')
        parts = [f"N:{name}", f"TEL:{phone}"]
        if email:
            parts.append(f"EMAIL:{email}")
        parts.append("")
        return "MECARD:" + ";".join(parts)


class WiFiPayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "wifi"

    @property
    def description(self) -> str:
        return "WiFi network configuration"

    @property
    def required_columns(self) -> List[str]:
        return ["SSID"]

    @property
    def optional_columns(self) -> List[str]:
        return ["Password", "Encryption", "Hidden"]

    def generate(self, data: Dict[str, Any]) -> str:
        ssid = data.get('SSID', '')
        password = data.get('Password', '')
        encryption = data.get('Encryption', 'WPA')
        hidden = data.get('Hidden', 'false')
        parts = [f"WIFI:T:{encryption};S:{ssid};"]
        if password:
            parts.append(f"P:{password};")
        parts.append(f"H:{hidden};;")
        return "".join(parts)


class URLPayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "url"

    @property
    def description(self) -> str:
        return "URL payload"

    @property
    def required_columns(self) -> List[str]:
        return ["URL"]

    def generate(self, data: Dict[str, Any]) -> str:
        url = data.get('URL', '')
        if not url.startswith(('http://', 'https://')):
            url = f"https://{url}"
        return url


class SMSPayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "sms"

    @property
    def description(self) -> str:
        return "SMS message"

    @property
    def optional_columns(self) -> List[str]:
        return ["Message"]

    def generate(self, data: Dict[str, Any]) -> str:
        phone = data.get('Phone', '')
        message = data.get('Message', '')
        return f"smsto:{phone}:{message}"


class EmailPayload(PayloadGenerator):
    @property
    def name(self) -> str:
        return "email"

    @property
    def description(self) -> str:
        return "Email message"

    @property
    def required_columns(self) -> List[str]:
        return ["Email"]

    @property
    def optional_columns(self) -> List[str]:
        return ["Subject", "Body"]

    def generate(self, data: Dict[str, Any]) -> str:
        email = data.get('Email', '')
        subject = data.get('Subject', '')
        body = data.get('Body', '')
        parts = [f"mailto:{email}"]
        params = []
        if subject:
            params.append(f"subject={subject}")
        if body:
            params.append(f"body={body}")
        if params:
            parts[0] += "?" + "&".join(params)
        return parts[0]
