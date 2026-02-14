import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import pandas as pd

from qr_code_generator.core.generator import QRCodeGenerator
from qr_code_generator.core.formatter import PhoneFormatter
from qr_code_generator.core.validator import DataValidator
from qr_code_generator.core.sanitizer import FilenameSanitizer, PathValidator
from qr_code_generator.utils.file_utils import FileValidator
from qr_code_generator.utils.pii_utils import PIIRedactor
from qr_code_generator.plugins.payload import (
    PayloadGenerator, PhonePayload, VCardPayload, MeCardPayload,
    WiFiPayload, URLPayload, SMSPayload, EmailPayload
)


logger = logging.getLogger(__name__)


class QRCodeService:
    PAYLOAD_MAP: Dict[str, type] = {
        'phone': PhonePayload,
        'vcard': VCardPayload,
        'mecard': MeCardPayload,
        'wifi': WiFiPayload,
        'url': URLPayload,
        'sms': SMSPayload,
        'email': EmailPayload,
    }

    def __init__(
        self,
        generator: Optional[QRCodeGenerator] = None,
        formatter: Optional[PhoneFormatter] = None,
        validator: Optional[DataValidator] = None,
        sanitizer: Optional[FilenameSanitizer] = None,
    ):
        self.generator = generator or QRCodeGenerator()
        self.formatter = formatter or PhoneFormatter()
        self.validator = validator or DataValidator()
        self.sanitizer = sanitizer or FilenameSanitizer()

    def get_payload_generator(self, format_name: str) -> PayloadGenerator:
        generator_class = self.PAYLOAD_MAP.get(format_name.lower())
        if not generator_class:
            raise ValueError(f"Unknown payload format: {format_name}")
        return generator_class()  # type: ignore[return-value]

    def generate_from_excel(
        self,
        input_file: str,
        output_folder: str,
        sheet_name: int = 0,
        keep_plus: bool = True,
        overwrite: bool = False,
        fill_color: str = "black",
        back_color: str = "white",
        box_size: int = 10,
        border: int = 4,
        error_correction: str = 'L',
        payload_format: str = 'phone',
        output_format: str = 'png',
        filename_template: str = '{Phone}',
        dedup: bool = False,
        allowed_output_path: Optional[str] = None,
        max_file_size_mb: int = 100,
        max_rows: int = 100000,
        redact_logs: bool = True,
        dry_run: bool = False,
        export_manifest: bool = False,
        manifest_format: str = 'json',
    ) -> int:
        valid, error = FileValidator.validate_input_file(input_file, max_rows=max_rows)
        if not valid:
            logger.error(error)
            return 1

        os.makedirs(output_folder, exist_ok=True)
        
        if allowed_output_path:
            os.makedirs(allowed_output_path, exist_ok=True)

        stats: Dict[str, Any] = {
            'total': 0,
            'generated': 0,
            'skipped_existing': 0,
            'skipped_invalid': 0,
            'skipped_duplicate': 0,
            'start_time': datetime.now().isoformat(),
        }

        seen_phones = set()
        manifest = []

        try:
            df = pd.read_excel(input_file, sheet_name=sheet_name)
            stats['total'] = len(df)
            logger.info(f"Found {stats['total']} rows")

            is_valid, validation_result = self.validator.validate_dataframe(df)
            if not is_valid:
                logger.warning(f"Data validation issues: {validation_result}")

            payload_gen = self.get_payload_generator(payload_format)

            for index, row in df.iterrows():
                row_num = int(index) + 2  # type: ignore[arg-type]

                phone_val = row.get('Phone')
                if phone_val is None or pd.isna(phone_val) or str(phone_val).strip() == '':
                    stats['skipped_invalid'] += 1
                    continue

                phone = self.formatter.format_phone(str(phone_val), keep_plus)

                if dedup:
                    if phone in seen_phones:
                        stats['skipped_duplicate'] += 1
                        continue
                    seen_phones.add(phone)

                row_dict = {col: str(row[col]) if col in df.columns else '' for col in df.columns}
                
                valid_payload, payload_error = payload_gen.validate(row_dict)
                if not valid_payload:
                    logger.warning(f"Row {row_num}: {payload_error}")
                    stats['skipped_invalid'] += 1
                    continue

                payload = payload_gen.generate(row_dict)

                try:
                    filename_data = row_dict.copy()
                    filename_data['Phone'] = phone.lstrip('+') if not keep_plus else phone
                    
                    for key, value in filename_data.items():
                        sanitized_value, path_error = PathValidator.validate_and_sanitize_path(
                            value, allowed_output_path
                        )
                        if path_error:
                            logger.warning(f"Row {row_num}: {path_error}")
                            sanitized_value = self.sanitizer.sanitize_template_value(value)
                        filename_data[key] = sanitized_value
                    
                    filename_base = filename_template.format(**filename_data)
                    filename = self.sanitizer.sanitize_filename(filename_base) + f'.{output_format}'
                except (KeyError, IndexError) as e:
                    filename = self.sanitizer.sanitize_filename(phone) + f'.{output_format}'

                if allowed_output_path:
                    full_output_path = os.path.join(allowed_output_path, filename)
                else:
                    full_output_path = os.path.join(output_folder, filename)

                valid_path, path_error = self.sanitizer.validate_output_path(full_output_path, allowed_output_path)
                if not valid_path:
                    logger.error(f"Row {row_num}: {path_error}")
                    stats['skipped_invalid'] += 1
                    continue

                if os.path.exists(full_output_path) and not overwrite:
                    stats['skipped_existing'] += 1
                    continue

                if dry_run:
                    logger.info(f"[DRY RUN] Would generate: {filename}")
                    stats['generated'] += 1
                    continue

                result = self.generator.generate(
                    payload,
                    Path(full_output_path),
                    fill_color,
                    back_color,
                    box_size,
                    border,
                    error_correction,
                    output_format,
                )

                if result.success:
                    stats['generated'] += 1
                    log_msg = f"Generated: {filename}"
                    if redact_logs:
                        log_msg = PIIRedactor.redact_pii(log_msg)
                    logger.info(log_msg)
                    
                    if export_manifest:
                        manifest.append({
                            'row_number': row_num,
                            'filename': filename,
                            'payload_type': payload_format,
                            'timestamp': datetime.now().isoformat(),
                        })
                else:
                    logger.error(f"Row {row_num}: {result.error}")
                    stats['skipped_invalid'] += 1

            if export_manifest and manifest:
                manifest_path = os.path.join(output_folder, f"manifest.{manifest_format}")
                if manifest_format == 'json':
                    with open(manifest_path, 'w') as f:
                        json.dump(manifest, f, indent=2)
                elif manifest_format == 'csv':
                    pd.DataFrame(manifest).to_csv(manifest_path, index=False)
                logger.info(f"Manifest exported to: {manifest_path}")

            stats['end_time'] = datetime.now().isoformat()
            
            logger.info("\n" + "="*50)
            logger.info("SUMMARY")
            logger.info("="*50)
            logger.info(f"Total rows:        {stats['total']}")
            logger.info(f"QR codes generated: {stats['generated']}")
            if stats['skipped_existing'] > 0:
                logger.info(f"Skipped (existing): {stats['skipped_existing']}")
            if stats['skipped_duplicate'] > 0:
                logger.info(f"Skipped (duplicate): {stats['skipped_duplicate']}")
            if stats['skipped_invalid'] > 0:
                logger.info(f"Skipped (invalid):  {stats['skipped_invalid']}")
            logger.info("="*50)

            return 0

        except Exception as e:
            logger.error(f"Error processing Excel file: {str(e)}")
            return 1
