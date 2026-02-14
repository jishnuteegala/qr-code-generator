import re
from typing import Optional


class PIIRedactor:
    PHONE_REGEX = re.compile(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}')
    EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    @staticmethod
    def mask_phone(phone_str: str, mask_char: str = '*') -> str:
        phone_str = phone_str.strip()
        digits = re.sub(r'\D', '', phone_str)
        if len(digits) <= 4:
            return phone_str
        visible_end = digits[-4:]
        masked = mask_char * (len(digits) - 4) + visible_end
        if phone_str.startswith('+'):
            return '+' + masked
        return masked

    @staticmethod
    def mask_email(email_str: str, mask_char: str = '*') -> str:
        email_str = email_str.strip()
        match = PIIRedactor.EMAIL_REGEX.match(email_str)
        if not match:
            return email_str
        local, domain = email_str.split('@', 1)
        if len(local) <= 2:
            masked_local = mask_char * len(local)
        else:
            masked_local = local[0] + mask_char * (len(local) - 2) + local[-1]
        parts = domain.split('.')
        if len(parts) > 1:
            masked_domain = parts[0][0] + mask_char * (len(parts[0]) - 1) + '.' + '.'.join(parts[1:])
        else:
            masked_domain = domain[0] + mask_char * (len(domain) - 1)
        return f"{masked_local}@{masked_domain}"

    @staticmethod
    def redact_pii(text: str, mask_char: str = '*') -> str:
        text = PIIRedactor.PHONE_REGEX.sub(
            lambda m: PIIRedactor.mask_phone(m.group(0), mask_char), text
        )
        text = PIIRedactor.EMAIL_REGEX.sub(
            lambda m: PIIRedactor.mask_email(m.group(0), mask_char), text
        )
        return text
