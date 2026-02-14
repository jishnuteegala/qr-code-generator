import pytest

from pathlib import Path
from qr_code_generator.service import QRCodeService


class TestIntegration:
    def test_end_to_end_basic(self, sample_excel_file, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            sheet_name=0,
            keep_plus=True,
            overwrite=False,
            payload_format='phone',
            filename_template='{Phone}',
            dedup=False,
        )
        
        assert exit_code == 0
        output_path = Path(output_folder)
        assert len(list(output_path.glob("*.png"))) == 3

    def test_end_to_end_vcard(self, sample_excel_file, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            payload_format='vcard',
        )
        
        assert exit_code == 0

    def test_end_to_end_with_dedup(self, sample_excel_with_duplicates, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_with_duplicates),
            output_folder,
            dedup=True,
        )
        
        assert exit_code == 0
        output_path = Path(output_folder)
        assert len(list(output_path.glob("*.png"))) == 2

    @pytest.mark.parametrize("output_format", ["svg", "pdf"])
    def test_end_to_end_with_output_formats(self, sample_excel_file, temp_dir, output_format):
        service = QRCodeService()
        output_folder = str(temp_dir / f"output_{output_format}")

        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            output_format=output_format,
            overwrite=True,
        )

        assert exit_code == 0
        output_path = Path(output_folder)
        assert len(list(output_path.glob(f"*.{output_format}"))) == 3

    def test_end_to_end_dry_run(self, sample_excel_file, temp_dir, capsys):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            dry_run=True,
        )
        
        assert exit_code == 0
        output_path = Path(output_folder)
        assert len(list(output_path.glob("*.png"))) == 0

    def test_end_to_end_with_manifest(self, sample_excel_file, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            export_manifest=True,
            manifest_format='json',
        )
        
        assert exit_code == 0
        manifest_path = Path(output_folder) / "manifest.json"
        assert manifest_path.exists()

    def test_end_to_end_with_sandbox(self, sample_excel_file, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        allowed_path = str(temp_dir / "allowed")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            allowed_output_path=allowed_path,
        )
        
        assert exit_code == 0

    def test_end_to_end_max_rows(self, sample_excel_file, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(sample_excel_file),
            output_folder,
            max_rows=1,
        )
        
        assert exit_code == 1

    def test_end_to_end_invalid_file(self, temp_dir):
        service = QRCodeService()
        output_folder = str(temp_dir / "output")
        
        exit_code = service.generate_from_excel(
            str(temp_dir / "nonexistent.xlsx"),
            output_folder,
        )
        
        assert exit_code == 1
