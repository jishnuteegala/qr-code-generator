import os
import pytest
from qr_code_generator.core.sanitizer import FilenameSanitizer, PathValidator


class TestFilenameSanitizer:
    def test_sanitize_filename_basic(self):
        assert FilenameSanitizer.sanitize_filename("test.png") == "test.png"
        assert FilenameSanitizer.sanitize_filename("test<>file.png") == "test__file.png"

    def test_sanitize_filename_windows_reserved(self):
        assert FilenameSanitizer.sanitize_filename("CON.png") == "_CON.png"
        assert FilenameSanitizer.sanitize_filename("PRN.png") == "_PRN.png"
        assert FilenameSanitizer.sanitize_filename("aux.png") == "_aux.png"

    def test_sanitize_filename_max_length(self):
        long_name = "a" * 300 + ".png"
        result = FilenameSanitizer.sanitize_filename(long_name)
        assert len(result) <= 255

    def test_validate_output_path_valid(self):
        valid, error = FilenameSanitizer.validate_output_path("/output/test.png", "/output")
        assert valid is True
        assert error is None

    def test_validate_output_path_outside_allowed(self):
        valid, error = FilenameSanitizer.validate_output_path("/other/test.png", "/output")
        assert valid is False
        assert error is not None
        assert "outside" in error.lower()

    def test_sanitize_template_value_traversal(self):
        result = FilenameSanitizer.sanitize_template_value("../etc/passwd")
        assert ".." not in result

    def test_sanitize_template_value_absolute(self):
        result = FilenameSanitizer.sanitize_template_value("/etc/passwd")
        assert result.startswith("_")


class TestPathValidator:
    def test_is_path_traversal_attempt(self):
        assert PathValidator.is_path_traversal_attempt("../etc/passwd") is True
        assert PathValidator.is_path_traversal_attempt("..\\windows\\system32") is True
        assert PathValidator.is_path_traversal_attempt("normal_file.txt") is False

    def test_is_absolute_path(self):
        assert PathValidator.is_absolute_path("/home/user/file") is True
        assert PathValidator.is_absolute_path("C:\\Users\\file") is True
        assert PathValidator.is_absolute_path("relative/file") is False
