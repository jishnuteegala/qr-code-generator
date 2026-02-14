import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from qr_code_generator.core.formatter import PhoneFormatter


class DataValidator:
    REQUIRED_COLUMNS = {'Phone'}

    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        errors = []
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            errors.append(f"Missing required columns: {', '.join(missing)}")
        return len(errors) == 0, errors

    def validate_row(self, row: pd.Series) -> Tuple[bool, Optional[str]]:
        phone = row.get('Phone')
        if phone is None or pd.isna(phone) or str(phone).strip() == '':
            return False, "Missing phone number"
        valid, error = PhoneFormatter.validate_phone(str(phone))
        if not valid:
            return False, error
        return True, None

    def validate_dataframe(self, df: pd.DataFrame) -> Tuple[bool, Dict[str, Any]]:
        is_valid, schema_errors = self.validate_schema(df)
        if not is_valid:
            return False, {'schema_errors': schema_errors}

        issues = []
        valid_count = 0
        for row_num, (_, row) in enumerate(df.iterrows(), start=2):
            row_valid, row_error = self.validate_row(row)
            if row_valid:
                valid_count += 1
            else:
                issues.append({'row': row_num, 'error': row_error})

        return valid_count > 0, {
            'valid_count': valid_count,
            'invalid_count': len(df) - valid_count,
            'issues': issues[:100],
        }
