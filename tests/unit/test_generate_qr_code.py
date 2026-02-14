import pytest
from pathlib import Path
from qr_code_generator.core.generator import QRCodeGenerator


class TestQRCodeGenerator:
    def test_generate_qr_code_basic(self, temp_dir):
        generator = QRCodeGenerator()
        output_path = temp_dir / "test_qr.png"
        
        result = generator.generate(
            "Test data",
            output_path,
            fill_color="black",
            back_color="white",
            box_size=10,
            border=4,
            error_correction='L'
        )
        
        assert result.success is True
        assert output_path.exists()
        assert result.filepath == output_path

    def test_generate_qr_code_custom_colors(self, temp_dir):
        generator = QRCodeGenerator()
        output_path = temp_dir / "colored_qr.png"
        
        result = generator.generate(
            "Test data",
            output_path,
            fill_color="red",
            back_color="blue",
        )
        
        assert result.success is True

    def test_generate_qr_code_svg(self, temp_dir):
        generator = QRCodeGenerator()
        output_path = temp_dir / "test_qr"

        result = generator.generate(
            "Test SVG data",
            output_path,
            output_format="svg",
        )

        assert result.success is True
        assert result.filepath is not None
        assert result.filepath.suffix == ".svg"
        assert result.filepath.exists()

    def test_generate_qr_code_pdf(self, temp_dir):
        generator = QRCodeGenerator()
        output_path = temp_dir / "test_qr"

        result = generator.generate(
            "Test PDF data",
            output_path,
            output_format="pdf",
        )

        assert result.success is True
        assert result.filepath is not None
        assert result.filepath.suffix == ".pdf"
        assert result.filepath.exists()

    def test_validate_data_valid(self):
        generator = QRCodeGenerator()
        valid, error = generator.validate_data("Test data")
        assert valid is True
        assert error is None

    def test_validate_data_empty(self):
        generator = QRCodeGenerator()
        valid, error = generator.validate_data("")
        assert valid is False
        assert error is not None
        assert "empty" in error.lower()

    def test_validate_data_too_long(self):
        generator = QRCodeGenerator()
        long_data = "x" * 3000
        valid, error = generator.validate_data(long_data)
        assert valid is False
        assert error is not None
        assert "capacity" in error.lower()
