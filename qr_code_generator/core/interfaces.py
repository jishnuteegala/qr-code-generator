from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass


@dataclass
class QRCodeResult:
    success: bool
    filepath: Optional[Path] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class IDataReader(ABC):
    @abstractmethod
    def read(self, source: str | Path) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def validate_schema(self, source: str | Path) -> tuple[bool, List[str]]:
        pass


class IQRCodeGenerator(ABC):
    @abstractmethod
    def generate(
        self,
        data: str,
        output_path: Path,
        **kwargs
    ) -> QRCodeResult:
        pass

    @abstractmethod
    def validate_data(self, data: str) -> tuple[bool, Optional[str]]:
        pass


class IFormatter(ABC):
    @abstractmethod
    def format(self, data: Any, **kwargs) -> str:
        pass


class IValidator(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        pass


class IOutputHandler(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def extension(self) -> str:
        pass

    @abstractmethod
    def save(self, qr_image, filepath: Path, **kwargs) -> QRCodeResult:
        pass

    @abstractmethod
    def supports_format(self, format_name: str) -> bool:
        pass
