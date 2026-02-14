from enum import Enum
from typing import Final

MAX_FILENAME_LENGTH: Final[int] = 255

DEFAULT_BOX_SIZE: Final[int] = 10
DEFAULT_BORDER: Final[int] = 4

DEFAULT_MAX_FILE_SIZE_MB: Final[int] = 100
DEFAULT_MAX_ROWS: Final[int] = 100000

VALID_INPUT_EXTENSIONS: Final[set] = {".xlsx", ".xls", ".csv", ".json"}
VALID_OUTPUT_EXTENSIONS: Final[set] = {".png", ".svg", ".pdf"}

WINDOWS_RESERVED_NAMES: Final[set] = {
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
}

EXCEL_LEGACY_MAGIC_BYTES: Final[bytes] = b'\x50\x0b\x01\x02\x00\x00'
EXCEL_ZIP_MAGIC_BYTES: Final[bytes] = b'\x50\x4b\x03\x04'

PATH_TRAVERSAL_PATTERNS: Final[list] = [
    '..\\',
    '../',
    '%2e%2e/',
    '%2e%2e\\',
]

ERROR_CORRECTION_LEVELS = {
    'L': 'L',
    'M': 'M',
    'Q': 'Q',
    'H': 'H',
}

PAYLOAD_FORMATS = ['phone', 'vcard', 'mecard', 'wifi', 'url', 'sms', 'email']
OUTPUT_FORMATS = ['png', 'svg', 'pdf']
