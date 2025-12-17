#!/bin/bash
# Setup script for QR Code Generator (Linux/Mac)
# This automates the setup process

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}QR Code Generator - Setup Script${NC}"
echo -e "${CYAN}=================================${NC}"
echo ""

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo -e "${RED}✗ Python not found. Please install Python 3.8+ from your package manager${NC}"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-venv python3-pip"
    echo "  Fedora/RHEL:   sudo dnf install python3 python3-pip"
    echo "  macOS:         brew install python3"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
echo -e "${GREEN}✓ Found: $PYTHON_VERSION${NC}"

# Create virtual environment
echo ""
echo -e "${YELLOW}Creating virtual environment...${NC}"
if [ -d .venv ]; then
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
else
    $PYTHON_CMD -m venv .venv
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Virtual environment created${NC}"
    else
        echo -e "${RED}✗ Failed to create virtual environment${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}✗ Failed to activate virtual environment${NC}"
    exit 1
fi

# Install dependencies
echo ""
echo -e "${YELLOW}Installing dependencies from requirements.txt...${NC}"
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Verify sample input file
echo ""
echo -e "${YELLOW}Checking sample input file...${NC}"
if [ -f input/contacts.xlsx ]; then
    echo -e "${GREEN}✓ Sample input file exists${NC}"
else
    echo -e "${YELLOW}⚠ Sample input file not found at input/contacts.xlsx${NC}"
    echo "  You'll need to create your own Excel file with a 'Phone' column"
fi

# Make run.sh executable
if [ -f run.sh ]; then
    chmod +x run.sh
    echo -e "${GREEN}✓ Made run.sh executable${NC}"
fi

# Success message
echo ""
echo -e "${CYAN}=================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${CYAN}=================================${NC}"
echo ""
echo -e "${CYAN}Quick start commands:${NC}"
echo "  python generate_qr_code_images.py                    # Generate with defaults"
echo "  python generate_qr_code_images.py --help             # View all options"
echo "  python generate_qr_code_images.py --payload-format vcard --filename-template '{Name}'"
echo ""
echo "Or use the convenience script:"
echo "  ./run.sh --payload-format vcard"
echo ""
echo -e "${YELLOW}Remember to activate the virtual environment before running:${NC}"
echo "  source .venv/bin/activate"
echo ""
