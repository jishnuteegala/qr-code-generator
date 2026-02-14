import qrcode
from qrcode.image.svg import SvgPathImage
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from pathlib import Path
from typing import Optional, Dict, Any
from qr_code_generator.core.interfaces import QRCodeResult
from qr_code_generator.plugins.output import (
    OutputAdapter,
    PNGOutputAdapter,
    SVGOutputAdapter,
    PDFOutputAdapter,
)


class QRCodeGenerator:
    ERROR_LEVELS = {
        'L': ERROR_CORRECT_L,
        'M': ERROR_CORRECT_M,
        'Q': ERROR_CORRECT_Q,
        'H': ERROR_CORRECT_H,
    }

    OUTPUT_ADAPTERS: Dict[str, type[OutputAdapter]] = {
        'png': PNGOutputAdapter,
        'svg': SVGOutputAdapter,
        'pdf': PDFOutputAdapter,
    }

    def generate(
        self,
        data: str,
        output_path: Path,
        fill_color: str = "black",
        back_color: str = "white",
        box_size: int = 10,
        border: int = 4,
        error_correction: str = 'L',
        output_format: str = 'png'
    ) -> QRCodeResult:
        try:
            output_format = output_format.lower()
            adapter_cls = self.OUTPUT_ADAPTERS.get(output_format)
            if adapter_cls is None:
                return QRCodeResult(success=False, error=f"Unsupported output format: {output_format}")

            qr = qrcode.QRCode(
                version=1,
                error_correction=self.ERROR_LEVELS.get(error_correction, ERROR_CORRECT_L),
                box_size=box_size,
                border=border,
            )
            qr.add_data(data)
            qr.make(fit=True)

            if output_format == 'svg':
                qr_image = qr.make_image(image_factory=SvgPathImage)
            else:
                qr_image = qr.make_image(fill_color=fill_color, back_color=back_color)

            adapter = adapter_cls()
            result = adapter.save(qr_image, output_path)
            if not result.success:
                return result

            return QRCodeResult(
                success=True,
                filepath=result.filepath,
                metadata={
                    'data_length': len(data),
                    'box_size': box_size,
                    'border': border,
                    'error_correction': error_correction,
                    'output_format': output_format,
                }
            )
        except Exception as e:
            return QRCodeResult(success=False, error=str(e))

    def validate_data(self, data: str) -> tuple[bool, Optional[str]]:
        if not data or not data.strip():
            return False, "Data cannot be empty"
        if len(data) > 2953:
            return False, "Data exceeds maximum QR code capacity"
        return True, None
