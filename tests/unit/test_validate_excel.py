import pytest
from pathlib import Path
from qr_code_generator.utils.file_utils import FileValidator


class TestFileValidator:
    def test_validate_excel_file_not_found(self):
        valid, error = FileValidator.validate_excel_file("/nonexistent/file.xlsx")
        assert valid is False
        assert error is not None
        assert "not found" in error.lower()

    def test_validate_excel_file_invalid_extension(self, temp_dir):
        txt_file = temp_dir / "contacts.txt"
        txt_file.write_text("test content")
        valid, error = FileValidator.validate_excel_file(str(txt_file))
        assert valid is False
        assert error is not None
        assert "unsupported" in error.lower()

    def test_validate_excel_file_valid(self, sample_excel_file):
        valid, error = FileValidator.validate_excel_file(str(sample_excel_file))
        assert valid is True
        assert error is None

    def test_check_file_size_limits_valid(self, sample_excel_file):
        valid, error = FileValidator.check_file_size_limits(str(sample_excel_file), max_size_mb=100, max_rows=100000)
        assert valid is True
        assert error is None

    def test_check_file_size_limits_too_many_rows(self, sample_excel_file):
        valid, error = FileValidator.check_file_size_limits(str(sample_excel_file), max_rows=1)
        assert valid is False
        assert error is not None
        assert "exceeds limit" in error.lower()

    def test_validate_input_file(self, sample_excel_file):
        valid, error = FileValidator.validate_input_file(str(sample_excel_file))
        assert valid is True
        assert error is None
