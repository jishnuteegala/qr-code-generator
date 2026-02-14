# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-02-14

### Added

- **Modular Architecture**
  - Package structure with DI container
  - Abstract interfaces for all components
  - Plugin system for payload generators and output adapters
  - Constructor injection throughout

- **Security Hardening**
  - Path traversal prevention in filename templates
  - Output sandboxing with `--allowed-output-path`
  - PII redaction in logs (enabled by default)
  - Excel file validation (magic bytes)
  - File size and row limits

- **New Payload Formats**
  - WiFi: `WIFI:T:WPA;S:NetworkName;P:Password;;`
  - URL: `https://example.com`
  - SMS: `smsto:+1234567890:Message`
  - Email: `mailto:user@example.com?subject=...&body=...`

- **New CLI Options**
  - `--dry-run`: Validate inputs without generating QR codes
  - `--export-manifest`: Export metadata to JSON/CSV
  - `--manifest-format`: Choose manifest format
  - `--redact-logs` / `--no-redact-logs`: Control PII redaction
  - `--max-file-size-mb`: Limit input file size
  - `--max-rows`: Limit number of rows
  - `--output-format`: Choose output format (`png`, `svg`, `pdf`)

- **Test Suite**
  - 58 unit and integration tests
  - pytest configuration in pyproject.toml
  - Test fixtures for Excel files, temporary directories
  - Coverage reporting

### Fixed

- Output format generation now works end-to-end for `png`, `svg`, and `pdf`
- SVG generation now uses the correct SVG image factory path instead of Pillow `format='SVG'`
- QR generator now delegates output writing to format-specific adapters

### Changed

- **Package Rename**: `generate_qr_code_images.py` → `qr_code_generator` package
- **Entry Point**: `python -m qr_code_generator` (previously `python generate_qr_code_images.py`)
- **CLI Script**: `qrgen` now points to `qr_code_generator.cli:main`

### Removed

- Single-script `generate_qr_code_images.py` (replaced by package)
- Dependencies on global state

### Technical Details

- **New Dependencies**: None (same as v2.0.0)
- **Python Versions**: 3.8+
- **Test Framework**: pytest with pytest-cov

---

## [2.0.0] - 2025-12-17

### Added

- **Full CLI Support**: All options configurable via command-line arguments
  - `--input` and `--output` for custom paths (absolute or relative)
  - `--payload-format` to choose between phone, vcard, mecard formats
  - `--filename-template` for custom naming with column substitution
  - `--fill-color`, `--back-color`, `--box-size`, `--border` for QR customization
  - `--error-correction` for L, M, Q, H error correction levels
  - `--keep-plus` / `--no-keep-plus` to control phone number prefix
  - `--overwrite` to replace existing files
  - `--dedup` to skip duplicate phone numbers
  - `--verbose` / `--quiet` for logging control
  - `--version` to display version information

- **Multiple Payload Formats**
  - Phone (default): Simple `Phone: +441234567890`
  - vCard: Standard contact card for iOS/Android import
  - MeCard: Compact format for Japanese phones

- **Customizable QR Appearance**
  - Custom colors: `--fill-color darkblue --back-color lightgray`
  - Size control: `--box-size` and `--border` parameters
  - Error correction levels: L, M, Q, H

- **Flexible Filenames**
  - Template system using `{Phone}`, `{Name}`, `{Email}`
  - Automatic Windows reserved name sanitization
  - Special character handling

- **Data Validation & Safety**
  - Required `Phone` column validation
  - Skips blank/NaN rows with reporting
  - Optional deduplication
  - Won't overwrite existing files unless explicitly requested

- **Better Feedback**
  - Structured logging with --verbose/--quiet modes
  - Summary statistics at completion
  - Progress updates for each generated file
  - Proper exit codes for scripting

- **Quality of Life Improvements**
  - Sample Excel file: `input/contacts.xlsx` (3 sample rows)
  - Virtual environment with `requirements.txt`
  - Windows helpers: `run.bat`, `scripts\setup.ps1`
  - Linux/Mac helpers: `run.sh`, `scripts/setup.sh`
  - Proper packaging with `pyproject.toml`
  - Cross-platform `.gitignore`
  - AI agent instructions: `.github/copilot-instructions.md`

- **Cross-Platform Support**
  - Full compatibility: Windows, Linux, macOS
  - Platform-specific documentation and examples
  - Automated setup for all platforms
  - Supports both absolute and relative paths on all platforms

### Changed

- **Default Behavior**: Now uses workspace-relative paths instead of hardcoded absolute paths
  - Default input: `input/contacts.xlsx`
  - Default output: `images/`
- **Error Handling**: Replaced print statements with structured logging
- **Path Handling**: Uses `os.path` for cross-platform compatibility

### Removed

- Hardcoded absolute Windows paths
- Manual constant editing requirement
- Bare exception printing

### Fixed

- Filename sanitization for Windows reserved names (CON, PRN, AUX, NUL, etc.)
- Path handling across different operating systems

### Technical Details

- **Dependencies**:
  - `pandas==2.3.3` - Excel parsing
  - `qrcode==8.2` - QR code generation
  - `pillow==12.0.0` - Image backend
  - `openpyxl==3.1.5` - Excel engine

- **Platform Support**:
  - Windows (10, 11)
  - Linux (Ubuntu, Debian, Fedora, etc.)
  - macOS (10.15+)

- **Python Versions**: 3.8+

### Breaking Changes from 1.x

- Default paths changed from absolute to workspace-relative
- CLI now required for custom behavior (previously edited constants)
- Exit codes now return non-zero on errors (enables scripting)

### Backward Compatibility

The default behavior maintains 1.x semantics:
- Phone-only QR codes by default
- `+` prefix in payload and filenames (can be disabled)
- Black on white styling
- Same QR settings (version=1, ERROR_CORRECT_L, box_size=10, border=4)

---

## [1.0.0] - 2023-01-01

### Initial Release

- Basic QR code generation from Excel files
- Two simple functions: `generate_qr_code()` and `generate_qr_codes_from_excel()`
- Hardcoded Windows paths (user had to edit constants before running)
- Phone-only QR codes with `+` prefix
- Fixed QR settings: version=1, ERROR_CORRECT_L, box_size=10, border=4
- Black on white styling (hardcoded)
- Basic error handling with print statements
- No CLI - required editing Python constants to change input/output paths
- No validation of Excel columns
- No logging framework
