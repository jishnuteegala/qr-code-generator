#!/bin/bash
# Quick runner for QR code generator (Linux/Mac)

# Activate virtual environment if it exists
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
fi

# Run the script with all arguments
python generate_qr_code_images.py "$@"

# Capture exit code
exit_code=$?

# Keep terminal open on error (only in interactive shells)
if [ $exit_code -ne 0 ] && [ -t 0 ]; then
    echo ""
    echo "Press Enter to continue..."
    read
fi

exit $exit_code
