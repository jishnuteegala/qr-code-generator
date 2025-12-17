# Excel to QR Code Generator

> **v2.0.0** - Generate QR Code images from contact details stored in an Excel file with flexible output formats, customization options, and an intuitive CLI.

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

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run with sample data:**
   ```cmd
   python generate_qr_code_images.py
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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run with sample data:**
   ```bash
   python generate_qr_code_images.py
   ```

---

This generates QR codes from `input/contacts.xlsx` and saves them to the `images/` folder.

## Usage

### Basic Commands

**Default behavior** (Phone-only QR codes with `+` prefix):
```cmd
python generate_qr_code_images.py
```

**Specify custom paths (relative):**
```cmd
python generate_qr_code_images.py --input data.xlsx --output qr_images/
```

**Use absolute paths anywhere on your system:**
```bash
# Windows
python generate_qr_code_images.py --input "C:\Users\YourName\Documents\contacts.xlsx" --output "D:\QR_Codes"

# Linux/Mac
python generate_qr_code_images.py --input "/home/username/documents/contacts.xlsx" --output "/home/username/qr_codes"
```

**Generate vCard format without plus sign:**
```cmd
python generate_qr_code_images.py --payload-format vcard --no-keep-plus
```

**Custom filename using Name field:**
```cmd
python generate_qr_code_images.py --filename-template "{Name}"
```

**Enable deduplication and overwrite existing files:**
```cmd
python generate_qr_code_images.py --dedup --overwrite
```

### CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | Input Excel file path (absolute or relative) | `input/contacts.xlsx` |
| `-o, --output` | Output folder for QR codes (absolute or relative) | `images` |
| `-s, --sheet` | Sheet name or index | `0` |
| `--keep-plus` | Prefix phone numbers with `+` | Enabled |
| `--no-keep-plus` | Don't prefix phone numbers | - |
| `--overwrite` | Overwrite existing QR files | Disabled |
| `--dedup` | Skip duplicate phone numbers | Disabled |
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
| `--payload-format` | Format: `phone`, `vcard`, `mecard` | `phone` |
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

## Filename Templates

Use column names from your Excel file in curly braces:

- `{Phone}` → `+441234567890.png`
- `{Name}` → `John Smith.png`
- `{Email}` → `john.smith@example.com.png`
- `{Name}_{Phone}` → `John Smith_+441234567890.png`

The script automatically sanitizes filenames to remove invalid characters and handle Windows reserved names.

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
python generate_qr_code_images.py --fill-color darkblue --back-color lightgray
```

**High error correction for damaged/small codes:**
```cmd
python generate_qr_code_images.py --error-correction H
```

**Process specific Excel sheet:**
```cmd
python generate_qr_code_images.py --sheet "Contacts 2024"
```

**Combine multiple options:**
```cmd
python generate_qr_code_images.py ^
    --input data/employees.xlsx ^
    --output qr_codes/employees/ ^
    --payload-format vcard ^
    --filename-template "{Name}_{Phone}" ^
    --fill-color navy ^
    --dedup ^
    --verbose
```

**Process files from anywhere on your system:**
```bash
# Windows (CMD)
python generate_qr_code_images.py ^
    --input "C:\Users\John\Documents\Sales\contacts_2024.xlsx" ^
    --output "D:\Shared\QR_Codes\Sales" ^
    --payload-format vcard

# Linux/Mac (bash/zsh)
python generate_qr_code_images.py \
    --input "/home/john/documents/sales/contacts_2024.xlsx" \
    --output "/mnt/shared/qr_codes/sales" \
    --payload-format vcard
```

> **Note:** Use `^` for line continuation in CMD, `` ` `` in PowerShell, or `\` in bash/zsh. Quote paths with spaces.

## Platform Support

**Fully cross-platform** - works on:
- ✅ Windows (10, 11)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ macOS (10.15+)

**Path formats:**
- Windows: `C:\Users\...\file.xlsx` or `C:/Users/.../file.xlsx` (both work)
- Linux/Mac: `/home/username/documents/file.xlsx`

**Python versions:** 3.8+ (tested on 3.12.1)

## Project Structure

```
qr-code-generator/
├── .venv/                          # Virtual environment
├── .github/
│   └── copilot-instructions.md     # AI agent instructions
├── scripts/
│   ├── setup.ps1                   # Windows setup automation
│   └── setup.sh                    # Linux/Mac setup automation
├── input/
│   └── contacts.xlsx               # Sample input data
├── images/                         # Generated QR codes
│   └── .gitkeep
├── generate_qr_code_images.py      # Main script
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Packaging metadata
├── run.bat                         # Windows quick runner
├── run.sh                          # Linux/Mac quick runner
├── .gitignore                      # Git ignore rules
├── CHANGELOG.md                    # Version history
├── README.md                       # This file
└── LICENSE                         # MIT License
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
