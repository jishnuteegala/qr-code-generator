from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path
from qr_code_generator.core.interfaces import QRCodeResult


class OutputAdapter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def extension(self) -> str:
        pass

    @property
    @abstractmethod
    def mime_type(self) -> str:
        pass

    @abstractmethod
    def save(self, qr_image: Any, filepath: Path, **kwargs) -> QRCodeResult:
        pass

    def supports_stream(self) -> bool:
        return False


class PNGOutputAdapter(OutputAdapter):
    @property
    def name(self) -> str:
        return "png"

    @property
    def extension(self) -> str:
        return ".png"

    @property
    def mime_type(self) -> str:
        return "image/png"

    def save(self, qr_image: Any, filepath: Path, **kwargs) -> QRCodeResult:
        try:
            filepath = filepath.with_suffix(self.extension)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            qr_image.save(str(filepath), format="PNG")
            return QRCodeResult(success=True, filepath=filepath)
        except Exception as e:
            return QRCodeResult(success=False, error=str(e))


class SVGOutputAdapter(OutputAdapter):
    @property
    def name(self) -> str:
        return "svg"

    @property
    def extension(self) -> str:
        return ".svg"

    @property
    def mime_type(self) -> str:
        return "image/svg+xml"

    def save(self, qr_image: Any, filepath: Path, **kwargs) -> QRCodeResult:
        try:
            filepath = filepath.with_suffix(self.extension)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            with open(filepath, 'wb') as f:
                qr_image.save(f)

            return QRCodeResult(success=True, filepath=filepath)
        except Exception as e:
            return QRCodeResult(success=False, error=str(e))


class PDFOutputAdapter(OutputAdapter):
    @property
    def name(self) -> str:
        return "pdf"

    @property
    def extension(self) -> str:
        return ".pdf"

    @property
    def mime_type(self) -> str:
        return "application/pdf"

    def save(self, qr_image: Any, filepath: Path, **kwargs) -> QRCodeResult:
        try:
            filepath = filepath.with_suffix(self.extension)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            if hasattr(qr_image, "get_image"):
                qr_image = qr_image.get_image()

            qr_image.convert("RGB").save(str(filepath), format="PDF")

            return QRCodeResult(success=True, filepath=filepath)
        except Exception as e:
            return QRCodeResult(success=False, error=str(e))
