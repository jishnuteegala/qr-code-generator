import argparse
import logging
import os
import re
import sys
from pathlib import Path

import pandas as pd
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image


__version__ = "2.0.0"
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def sanitize_filename(filename):
    """Sanitize filename to remove invalid characters and reserved names."""
    # Remove invalid characters for Windows/Unix
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', filename)
    
    # Handle Windows reserved names
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    
    name_without_ext = os.path.splitext(sanitized)[0]
    if name_without_ext.upper() in reserved:
        sanitized = f"_{sanitized}"
    
    return sanitized


def generate_qr_code(data, output_file, fill_color="black", back_color="white", 
                     box_size=10, border=4, error_correction='L'):
    """Generate QR code from contact details with customizable settings."""
    error_levels = {
        'L': ERROR_CORRECT_L,
        'M': ERROR_CORRECT_M,
        'Q': ERROR_CORRECT_Q,
        'H': ERROR_CORRECT_H,
    }
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_levels.get(error_correction, ERROR_CORRECT_L),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    img.save(output_file)


def format_phone(phone, keep_plus=True):
    """Format phone number with optional plus sign."""
    phone_str = str(phone).strip()
    if keep_plus and not phone_str.startswith('+'):
        return f"+{phone_str}"
    return phone_str


def generate_qr_codes_from_excel(input_excel_file, output_folder, sheet_name=0, 
                                 keep_plus=True, overwrite=False, 
                                 fill_color="black", back_color="white",
                                 box_size=10, border=4, error_correction='L',
                                 payload_format='phone', filename_template='{Phone}',
                                 dedup=False):
    """Process Excel file and generate QR codes with advanced options."""
    
    # Validate input file
    if not os.path.exists(input_excel_file):
        logger.error(f"Input file not found: {input_excel_file}")
        return 1
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    logger.info(f"Output folder: {output_folder}")
    
    # Statistics
    stats = {
        'total': 0,
        'generated': 0,
        'skipped_existing': 0,
        'skipped_invalid': 0,
        'skipped_duplicate': 0
    }
    
    seen_phones = set()
    
    try:
        # Read Excel file
        logger.info(f"Reading Excel file: {input_excel_file}")
        df = pd.read_excel(input_excel_file, sheet_name=sheet_name)
        stats['total'] = len(df)
        logger.info(f"Found {stats['total']} rows")
        
        # Validate required columns
        if 'Phone' not in df.columns:
            logger.error(f"Required column 'Phone' not found. Available columns: {', '.join(df.columns)}")
            return 1
        
        # Process each row
        for index, row in df.iterrows():
            row_num: int = int(index) + 2  # type: ignore
            # Skip rows with missing phone
            if pd.isna(row['Phone']) or str(row['Phone']).strip() == '':
                logger.debug(f"Row {row_num}: Skipping - missing phone number")
                stats['skipped_invalid'] += 1
                continue
            
            phone = format_phone(row['Phone'], keep_plus)
            
            # Deduplication
            if dedup:
                if phone in seen_phones:
                    logger.debug(f"Row {row_num}: Skipping duplicate - {phone}")
                    stats['skipped_duplicate'] += 1
                    continue
                seen_phones.add(phone)
            
            # Build payload based on format
            if payload_format == 'phone':
                contact_data = f"Phone: {phone}"
            elif payload_format == 'vcard':
                name = row.get('Name', 'Unknown')
                email = row.get('Email', '')
                contact_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"
            elif payload_format == 'mecard':
                name = row.get('Name', 'Unknown')
                email = row.get('Email', '')
                contact_data = f"MECARD:N:{name};TEL:{phone};EMAIL:{email};;"
            else:
                contact_data = f"Phone: {phone}"
            
            # Build filename from template
            try:
                filename_data = {col: str(row[col]) if col in df.columns else '' for col in df.columns}
                filename_data['Phone'] = phone.lstrip('+') if not keep_plus else phone
                filename_base = filename_template.format(**filename_data)
                filename = sanitize_filename(filename_base) + '.png'
            except (KeyError, IndexError) as e:
                logger.warning(f"Row {row_num}: Invalid filename template, using phone number")
                filename = sanitize_filename(phone) + '.png'
            
            output_file = os.path.join(output_folder, filename)
            
            # Check if file exists
            if os.path.exists(output_file) and not overwrite:
                logger.debug(f"Row {row_num}: Skipping existing file - {filename}")
                stats['skipped_existing'] += 1
                continue
            
            # Generate QR code
            try:
                generate_qr_code(contact_data, output_file, fill_color, back_color, 
                               box_size, border, error_correction)
                stats['generated'] += 1
                logger.info(f"Generated: {filename}")
            except Exception as e:
                logger.error(f"Row {row_num}: Failed to generate QR - {str(e)}")
                stats['skipped_invalid'] += 1
        
        # Print summary
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


def main():
    parser = argparse.ArgumentParser(
        description='Generate QR codes from Excel contact data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with defaults
  python generate_qr_code_images.py
  
  # Specify custom input and output (relative paths)
  python generate_qr_code_images.py --input data.xlsx --output qr_images/
  
  # Use absolute paths - Windows
  python generate_qr_code_images.py --input "C:\\Users\\John\\Documents\\contacts.xlsx" --output "D:\\QR_Codes"
  
  # Use absolute paths - Linux/Mac
  python generate_qr_code_images.py --input "/home/john/documents/contacts.xlsx" --output "/home/john/qr_codes"
  
  # Generate vCard format without plus sign
  python generate_qr_code_images.py --payload-format vcard --no-keep-plus
  
  # Custom filename using Name field
  python generate_qr_code_images.py --filename-template "{Name}"
  
  # Enable deduplication and overwrite existing files
  python generate_qr_code_images.py --dedup --overwrite
        """
    )
    
    parser.add_argument('-i', '--input', default='input/contacts.xlsx',
                       help='Input Excel file - absolute or relative path (default: input/contacts.xlsx)')
    parser.add_argument('-o', '--output', default='images',
                       help='Output folder for QR codes - absolute or relative path (default: images)')
    parser.add_argument('-s', '--sheet', default=0,
                       help='Sheet name or index (default: 0)')
    parser.add_argument('--keep-plus', dest='keep_plus', action='store_true', default=True,
                       help='Prefix phone numbers with + (default)')
    parser.add_argument('--no-keep-plus', dest='keep_plus', action='store_false',
                       help='Do not prefix phone numbers with +')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing QR code files')
    parser.add_argument('--dedup', action='store_true',
                       help='Skip duplicate phone numbers')
    
    # QR code appearance
    qr_group = parser.add_argument_group('QR code appearance')
    qr_group.add_argument('--fill-color', default='black',
                         help='Foreground color (default: black)')
    qr_group.add_argument('--back-color', default='white',
                         help='Background color (default: white)')
    qr_group.add_argument('--box-size', type=int, default=10,
                         help='Size of each box in pixels (default: 10)')
    qr_group.add_argument('--border', type=int, default=4,
                         help='Border size in boxes (default: 4)')
    qr_group.add_argument('--error-correction', choices=['L', 'M', 'Q', 'H'], default='L',
                         help='Error correction level (default: L)')
    
    # Payload and filename
    format_group = parser.add_argument_group('Payload and filename')
    format_group.add_argument('--payload-format', choices=['phone', 'vcard', 'mecard'], default='phone',
                             help='QR code payload format (default: phone)')
    format_group.add_argument('--filename-template', default='{Phone}',
                             help='Filename template using {ColumnName} (default: {Phone})')
    
    # Logging
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Suppress non-error output')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                       help='Show version and exit')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.quiet:
        logger.setLevel(logging.ERROR)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Run generation
    exit_code = generate_qr_codes_from_excel(
        args.input, args.output, args.sheet,
        args.keep_plus, args.overwrite,
        args.fill_color, args.back_color,
        args.box_size, args.border, args.error_correction,
        args.payload_format, args.filename_template,
        args.dedup
    )
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
