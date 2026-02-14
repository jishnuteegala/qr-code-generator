import re
from typing import Optional
from qr_code_generator.utils.constants import PATH_TRAVERSAL_PATTERNS, WINDOWS_RESERVED_NAMES, MAX_FILENAME_LENGTH


class FilenameSanitizer:
    @staticmethod
    def sanitize_filename(filename: str, max_length: int = MAX_FILENAME_LENGTH) -> str:
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
        name_without_ext = sanitized.rsplit('.', 1)[0] if '.' in sanitized else sanitized
        if name_without_ext.upper() in WINDOWS_RESERVED_NAMES:
            sanitized = f"_{sanitized}"
        if len(sanitized) > max_length:
            ext = sanitized.rsplit('.', 1)[1] if '.' in sanitized else ''
            name_part = sanitized.rsplit('.', 1)[0] if '.' in sanitized else sanitized
            max_name_length = max_length - len(ext) - 1 if ext else max_length
            sanitized = name_part[:max_name_length] + f".{ext}" if ext else name_part[:max_length]
        return sanitized

    @staticmethod
    def validate_output_path(filepath: str, allowed_root: Optional[str] = None) -> tuple[bool, Optional[str]]:
        import os
        abs_path = os.path.abspath(filepath)
        if allowed_root:
            abs_allowed = os.path.abspath(allowed_root)
            if not abs_path.startswith(abs_allowed):
                return False, f"Path '{filepath}' is outside allowed directory '{allowed_root}'"
        return True, None

    @staticmethod
    def sanitize_template_value(value: str) -> str:
        for pattern in PATH_TRAVERSAL_PATTERNS:
            if pattern.lower() in value.lower():
                value = value.replace(pattern, '_')
        if re.match(r'^[a-zA-Z]:[/\\]', value):
            value = '_' + value
        if value.startswith('\\\\') or value.startswith('//'):
            value = '_' + value
        return FilenameSanitizer.sanitize_filename(value)


class PathValidator:
    @staticmethod
    def is_path_traversal_attempt(value: str) -> bool:
        value_lower = value.lower()
        for pattern in PATH_TRAVERSAL_PATTERNS:
            if pattern.lower() in value_lower:
                return True
        return False

    @staticmethod
    def is_absolute_path(value: str) -> bool:
        import os
        return os.path.isabs(value)

    @staticmethod
    def validate_and_sanitize_path(value: str, allowed_root: Optional[str] = None) -> tuple[str, Optional[str]]:
        import os
        if PathValidator.is_path_traversal_attempt(value):
            return "", "Path traversal detected in value"
        if PathValidator.is_absolute_path(value):
            return "", "Absolute paths are not allowed in template variables"
        sanitized = FilenameSanitizer.sanitize_template_value(value)
        if allowed_root:
            test_path = os.path.join(allowed_root, sanitized)
            valid, error = FilenameSanitizer.validate_output_path(test_path, allowed_root)
            if not valid:
                return "", error
        return sanitized, None
