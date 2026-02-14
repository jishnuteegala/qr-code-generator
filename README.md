# Excel to QR Code Generator

> **v3.0.0** - Generate QR Code images from contact details stored in an Excel file with flexible output formats, customization options, and an intuitive CLI.

For version history, see [CHANGELOG.md](CHANGELOG.md).

## Quick Start

### Windows

**Option 1: Automated Setup (Recommended)**
```powershell
# Run the setup script
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1

# Then use the quick runner
run.bat
```

**Option 2: Manual Setup**
1. **Clone and navigate to the repo:**
   ```cmd
   cd qr-code-generator
   ```

2. **Create and activate a virtual environment:**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install the package:**
   ```cmd
   pip install -e .
   ```

4. **Run with sample data:**
   ```cmd
   python -m qr_code_generator
   ```

### Linux/Mac

**Option 1: Automated Setup (Recommended)**
```bash
# Run the setup script
bash scripts/setup.sh

# Then use the quick runner
./run.sh
```

**Option 2: Manual Setup**
1. **Clone and navigate to the repo:**
   ```bash
   cd qr-code-generator
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the package:**
   ```bash
   pip install -e .
   ```

4. **Run with sample data:**
   ```bash
   python -m qr_code_generator
   ```

---

This generates QR codes from `input/contacts.xlsx` and saves them to the `images/` folder.

## Usage

### Basic Commands

**Default behavior** (Phone-only QR codes with `+` prefix):
```cmd
python -m qr_code_generator
```

**Using the CLI shortcut:**
```cmd
qrgen
```

**Specify custom paths (relative):**
```cmd
python -m qr_code_generator --input data.xlsx --output qr_images/
```

**Use absolute paths anywhere on your system:**
```bash
# Windows
python -m qr_code_generator --input "C:/Users/YourName/Documents/contacts.xlsx" --output "D:/QR_Codes"

# Linux/Mac
python -m qr_code_generator --input "/home/username/documents/contacts.xlsx" --output "/home/username/qr_codes"
```

### New in v3.0.0

**Dry-run mode to test configuration:**
```cmd
python -m qr_code_generator --dry-run
```

**Export manifest:**
```cmd
python -m qr_code_generator --export-manifest --manifest-format json
```

**Generate SVG or PDF outputs:**
```cmd
python -m qr_code_generator --output-format svg
python -m qr_code_generator --output-format pdf
```

**Security options:**
```cmd
python -m qr_code_generator --allowed-output-path ./output --redact-logs
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input Excel file path (absolute or relative) | `input/contacts.xlsx` |
| `-o, --output` | Output folder for QR codes (absolute or relative) | `images` |
| `-s, --sheet` | Sheet index | `0` |
| `--keep-plus` | Prefix phone numbers with `+` | Enabled |
| `--no-keep-plus` | Don't prefix phone numbers | - |
| `--overwrite` | Overwrite existing QR files | Disabled |
| `--dedup` | Skip duplicate phone numbers | Disabled |
| `--dry-run` | Validate without generating | - |
| `--export-manifest` | Export metadata JSON/CSV | - |
| `--allowed-output-path` | Restrict output to directory | - |
| `--redact-logs` | Redact PII from logs | Enabled |
| `--max-file-size-mb` | Max input file size (MB) | `100` |
| `--max-rows` | Max rows to process | `100000` |
| `-v, --verbose` | Verbose logging (DEBUG level) | - |
| `-q, --quiet` | Suppress non-error output | - |

**QR Code Appearance:**
| Option | Description | Default |
|--------|-------------|---------|
| `--fill-color` | Foreground color | `black` |
| `--back-color` | Background color | `white` |
| `--box-size` | Pixel size of each box | `10` |
| `--border` | Border size in boxes | `4` |
| `--error-correction` | Error correction: `L`, `M`, `Q`, `H` | `L` |

**Payload & Filename:**
| Option | Description | Default |
|--------|-------------|---------|
| `--payload-format` | Format: `phone`, `vcard`, `mecard`, `wifi`, `url`, `sms`, `email` | `phone` |
| `--output-format` | File format: `png`, `svg`, `pdf` | `png` |
| `--filename-template` | Template using `{ColumnName}` | `{Phone}` |

### Excel Format

Your Excel file should include a **Phone** column (required). Optional columns like **Name** and **Email** are used for vCard/MeCard formats and filename templates.

**Example:**
| Name | Email | Phone |
|------|-------|-------|
| John Smith | john.smith@example.com | 441234567890 |
| Alice Johnson | alice.johnson@example.com | 442345678901 |

> **Note:** Phone numbers can include or omit the `+` prefix. The script handles both formats.

## Payload Formats

### Phone (default)
Simple text format: `Phone: +441234567890`

### vCard
Standard contact card format compatible with most phones:
```
BEGIN:VCARD
VERSION:3.0
FN:John Smith
TEL:+441234567890
EMAIL:john.smith@example.com
END:VCARD
```

### MeCard
Compact Japanese format supported by many QR readers:
```
MECARD:N:John Smith;TEL:+441234567890;EMAIL:john.smith@example.com;;
```

### WiFi (v3.0.0)
WiFi network configuration:
```
WIFI:T:WPA;S:NetworkName;P:Password;H:false;;
```

### URL (v3.0.0)
Direct URL:
```
https://example.com
```

### SMS (v3.0.0)
SMS message:
```
smsto:+441234567890:Message body
```

### Email (v3.0.0)
Email message:
```
mailto:user@example.com?subject=Subject&body=Body
```

## Filename Templates

Use column names from your Excel file in curly braces:

- `{Phone}` → `+441234567890.png`
- `{Name}` → `John Smith.png`
- `{Email}` → `john.smith@example.com.png`
- `{Name}_{Phone}` → `John Smith_+441234567890.png`

If you use `--output-format svg` or `--output-format pdf`, the same template is used with `.svg` or `.pdf` extensions.

The script automatically sanitizes filenames to remove invalid characters and handle Windows reserved names.

## Security Features (v3.0.0)

- **Path Traversal Prevention**: Template variables are validated to prevent path traversal attacks
- **Output Sandbox**: Use `--allowed-output-path` to restrict output to a specific directory
- **PII Redaction**: Phone numbers and emails are masked in logs by default
- **File Validation**: Excel files are validated for magic bytes and size limits

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'openpyxl'`  
**Solution:** Install openpyxl: `pip install openpyxl`

**Issue:** `FileNotFoundError: [Errno 2] No such file or directory: 'input/contacts.xlsx'`  
**Solution:** Ensure your Excel file exists at the specified path or use `--input` to specify a different location.

**Issue:** `Required column 'Phone' not found`  
**Solution:** Your Excel file must have a column named 'Phone'. Check the column headers.

**Issue:** QR codes are too small/large  
**Solution:** Adjust `--box-size` (default: 10) and `--border` (default: 4) values.

**Issue:** Script overwrites existing files  
**Solution:** Remove the `--overwrite` flag. By default, existing files are skipped.

## Advanced Examples

**Generate colored QR codes:**
```cmd
python -m qr_code_generator --fill-color darkblue --back-color lightgray
```

**High error correction for damaged/small codes:**
```cmd
python -m qr_code_generator --error-correction H
```

**Process specific Excel sheet:**
```cmd
python -m qr_code_generator --sheet 1
```

**Combine multiple options:**
```cmd
python -m qr_code_generator ^
    --input data/employees.xlsx ^
    --output qr_codes/employees/ ^
    --payload-format vcard ^
    --filename-template "{Name}_{Phone}" ^
    --fill-color navy ^
    --dedup ^
    --verbose
```

## Project Structure (v3.0.0)

```
qr-code-generator/
├── .venv/                          # Virtual environment
├── scripts/
│   ├── setup.ps1                   # Windows setup automation
│   └── setup.sh                    # Linux/Mac setup automation
├── qr_code_generator/              # Main package
│   ├── __init__.py
│   ├── __version__.py
│   ├── cli.py                      # CLI entry point
│   ├── service.py                  # Main orchestration
│   ├── di/                         # Dependency injection
│   ├── core/                       # Core modules
│   │   ├── generator.py           # QR generation
│   │   ├── formatter.py           # Phone formatting
│   │   ├── sanitizer.py           # Filename sanitization
│   │   ├── validator.py           # Data validation
│   │   └── interfaces.py          # Abstract interfaces
│   ├── plugins/
│   │   ├── payload/               # Payload generators
│   │   └── output/                # Output adapters
│   └── utils/                     # Utilities
├── tests/                         # Test suite
│   ├── unit/
│   └── integration/
├── input/
│   └── contacts.xlsx               # Sample input data
├── images/                         # Generated QR codes
├── pyproject.toml                  # Packaging metadata
├── pytest.ini                      # Test configuration
├── run.bat                         # Windows quick runner
├── run.sh                          # Linux/Mac quick runner
├── .gitignore                      # Git ignore rules
├── CHANGELOG.md                    # Version history
├── README.md                       # This file
├── AGENTS.md                       # AI agent instructions
└── LICENSE                         # MIT License
```

## Architecture Notes

- `cli.py` parses command-line arguments and maps them to service options.
- `service.py` (`QRCodeService`) is the orchestration layer used by CLI and tests. It validates input files/data, applies dedup and filename sanitization, creates payloads, invokes the QR generator, and writes optional manifests.
- `core/generator.py` performs QR generation and delegates file writing to output adapters (`png`/`svg`/`pdf`).

## Using QRCodeService Programmatically

If you want to use the package from Python code (without invoking the CLI), call `QRCodeService` directly:

```python
from qr_code_generator.service import QRCodeService

service = QRCodeService()

exit_code = service.generate_from_excel(
   input_file="input/contacts.xlsx",
   output_folder="images",
   payload_format="vcard",      # phone|vcard|mecard|wifi|url|sms|email
   output_format="svg",         # png|svg|pdf
   filename_template="{Name}_{Phone}",
   dedup=True,
   overwrite=False,
   dry_run=False,
   export_manifest=True,
   manifest_format="json",      # json|csv
)

if exit_code != 0:
   raise RuntimeError("QR generation failed")
```

Notes:
- Return value is an exit-style status code (`0` success, `1` failure).
- `allowed_output_path` enables output sandboxing when needed.
- This is the same workflow the CLI uses internally, so behavior stays consistent.

## Testing

Pytest configuration is maintained in `pytest.ini`.

Run the test suite:
```cmd
python -m pytest tests -v
```

Run with coverage:
```cmd
python -m pytest tests --cov=qr_code_generator --cov-report=term-missing
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
