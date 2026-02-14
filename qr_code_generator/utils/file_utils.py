import os
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
from qr_code_generator.utils.constants import (
    DEFAULT_MAX_FILE_SIZE_MB, 
    DEFAULT_MAX_ROWS,
    EXCEL_LEGACY_MAGIC_BYTES,
    EXCEL_ZIP_MAGIC_BYTES,
    VALID_INPUT_EXTENSIONS
)


class FileValidator:
    @staticmethod
    def validate_excel_file(filepath: str) -> Tuple[bool, Optional[str]]:
        path = Path(filepath)
        if not path.exists():
            return False, f"File not found: {filepath}"
        if not path.is_file():
            return False, f"Not a file: {filepath}"
        ext = path.suffix.lower()
        if ext not in VALID_INPUT_EXTENSIONS:
            return False, f"Unsupported file extension: {ext}"
        if ext in ('.xlsx', '.xls'):
            try:
                with open(filepath, 'rb') as f:
                    header = f.read(8)
                    if not (header.startswith(EXCEL_ZIP_MAGIC_BYTES) or header.startswith(EXCEL_LEGACY_MAGIC_BYTES)):
                        return False, "Invalid Excel file format"
            except Exception as e:
                return False, f"Error reading file: {str(e)}"
        return True, None

    @staticmethod
    def check_file_size_limits(
        filepath: str, 
        max_size_mb: int = DEFAULT_MAX_FILE_SIZE_MB,
        max_rows: int = DEFAULT_MAX_ROWS
    ) -> Tuple[bool, Optional[str]]:
        file_size = os.path.getsize(filepath)
        max_bytes = max_size_mb * 1024 * 1024
        if file_size > max_bytes:
            return False, f"File size ({file_size / (1024*1024):.1f}MB) exceeds limit ({max_size_mb}MB)"
        try:
            df = pd.read_excel(filepath, nrows=max_rows + 1)
            if len(df) > max_rows:
                return False, f"Row count ({len(df)}) exceeds limit ({max_rows})"
        except Exception as e:
            return False, f"Error reading file: {str(e)}"
        return True, None

    @staticmethod
    def validate_input_file(filepath: str, max_rows: int = DEFAULT_MAX_ROWS) -> Tuple[bool, Optional[str]]:
        valid, error = FileValidator.validate_excel_file(filepath)
        if not valid:
            return valid, error
        return FileValidator.check_file_size_limits(filepath, max_rows=max_rows)
