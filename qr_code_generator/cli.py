import argparse
import logging
import sys

from qr_code_generator import __version__
from qr_code_generator.service import QRCodeService


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Generate QR codes from Excel contact data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with defaults
  python -m qr_code_generator
  
  # Specify custom input and output
  python -m qr_code_generator --input data.xlsx --output qr_images/
  
  # Generate vCard format
  python -m qr_code_generator --payload-format vcard
  
  # Custom filename using Name field
  python -m qr_code_generator --filename-template "{Name}"
  
  # Enable deduplication
  python -m qr_code_generator --dedup
  
  # Dry-run mode to test configuration
  python -m qr_code_generator --dry-run
  
  # Export manifest
  python -m qr_code_generator --export-manifest --manifest-format json
  
  # Security options
  python -m qr_code_generator --allowed-output-path ./output --redact-logs
        """
    )

    parser.add_argument('-i', '--input', default='input/contacts.xlsx',
                       help='Input Excel file (default: input/contacts.xlsx)')
    parser.add_argument('-o', '--output', default='images',
                       help='Output folder for QR codes (default: images)')
    parser.add_argument('-s', '--sheet', type=int, default=0,
                       help='Sheet index (default: 0)')
    parser.add_argument('--keep-plus', dest='keep_plus', action='store_true', default=True,
                       help='Prefix phone numbers with + (default)')
    parser.add_argument('--no-keep-plus', dest='keep_plus', action='store_false',
                       help='Do not prefix phone numbers with +')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing QR code files')
    parser.add_argument('--dedup', action='store_true',
                       help='Skip duplicate phone numbers')

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

    format_group = parser.add_argument_group('Payload and filename')
    format_group.add_argument('--payload-format', 
                             choices=['phone', 'vcard', 'mecard', 'wifi', 'url', 'sms', 'email'],
                             default='phone',
                             help='QR code payload format (default: phone)')
    format_group.add_argument('--output-format',
                             choices=['png', 'svg', 'pdf'],
                             default='png',
                             help='Output image format (default: png)')
    format_group.add_argument('--filename-template', default='{Phone}',
                             help='Filename template using {ColumnName} (default: {Phone})')

    security_group = parser.add_argument_group('Security options')
    security_group.add_argument('--allowed-output-path',
                               help='Restrict output to specified directory for sandboxing (security)')
    security_group.add_argument('--redact-logs', action='store_true', default=True,
                              help='Redact PII from logs (default: enabled)')
    security_group.add_argument('--no-redact-logs', dest='redact_logs', action='store_false',
                              help='Disable PII redaction in logs')
    security_group.add_argument('--max-file-size-mb', type=int, default=100,
                              help='Maximum input file size in MB (default: 100)')
    security_group.add_argument('--max-rows', type=int, default=100000,
                              help='Maximum number of rows (default: 100000)')

    output_group = parser.add_argument_group('Output options')
    output_group.add_argument('--dry-run', action='store_true',
                             help='Validate inputs without generating QR codes')
    output_group.add_argument('--export-manifest', action='store_true',
                             help='Generate manifest file with metadata')
    output_group.add_argument('--manifest-format', choices=['json', 'csv'], default='json',
                             help='Manifest file format (default: json)')

    logging_group = parser.add_argument_group('Logging')
    logging_group.add_argument('-v', '--verbose', action='store_true',
                             help='Enable verbose output')
    logging_group.add_argument('-q', '--quiet', action='store_true',
                             help='Suppress non-error output')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}',
                       help='Show version and exit')

    args = parser.parse_args()

    if args.quiet:
        logger.setLevel(logging.ERROR)
    elif args.verbose:
        logger.setLevel(logging.DEBUG)

    service = QRCodeService()
    
    exit_code = service.generate_from_excel(
        args.input,
        args.output,
        args.sheet,
        args.keep_plus,
        args.overwrite,
        args.fill_color,
        args.back_color,
        args.box_size,
        args.border,
        args.error_correction,
        args.payload_format,
        args.output_format,
        args.filename_template,
        args.dedup,
        args.allowed_output_path,
        args.max_file_size_mb,
        args.max_rows,
        args.redact_logs,
        args.dry_run,
        args.export_manifest,
        args.manifest_format,
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
