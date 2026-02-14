import re
from typing import Optional


class PhoneFormatter:
    @staticmethod
    def format_phone(phone: str, keep_plus: bool = True) -> str:
        phone_str = str(phone).strip()
        if keep_plus and not phone_str.startswith('+'):
            return f"+{phone_str}"
        return phone_str

    @staticmethod
    def normalize_phone(phone: str) -> str:
        digits = re.sub(r'\D', '', phone)
        if phone.startswith('00') and len(digits) > 11:
            digits = digits[2:]
        elif digits.startswith('0') and len(digits) > 10:
            digits = digits[1:]
        if not digits.startswith('+'):
            digits = f"+{digits}"
        return digits

    @staticmethod
    def validate_phone(phone: str) -> tuple[bool, Optional[str]]:
        if not phone or not str(phone).strip():
            return False, "Phone number cannot be empty"
        digits = re.sub(r'\D', '', str(phone))
        if len(digits) < 7:
            return False, "Phone number must have at least 7 digits"
        if len(digits) > 15:
            return False, "Phone number cannot exceed 15 digits (E.164)"
        return True, None
