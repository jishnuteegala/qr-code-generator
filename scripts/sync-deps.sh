#!/bin/bash
# Sync lock files from pyproject.toml using pip-tools

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -x ".venv/bin/pip-compile" ]; then
    PIP_COMPILE=".venv/bin/pip-compile"
elif [ -x ".venv/Scripts/pip-compile.exe" ]; then
    PIP_COMPILE=".venv/Scripts/pip-compile.exe"
elif command -v pip-compile >/dev/null 2>&1; then
    PIP_COMPILE="pip-compile"
else
    echo "Error: pip-compile not found. Install pip-tools first: pip install pip-tools" >&2
    exit 1
fi

DRY_RUN=false
INCLUDE_TEST=false

for arg in "$@"; do
    case "$arg" in
        --dry-run)
            DRY_RUN=true
            ;;
        --with-test)
            INCLUDE_TEST=true
            ;;
        *)
            echo "Unknown option: $arg" >&2
            echo "Usage: bash scripts/sync-deps.sh [--dry-run] [--with-test]" >&2
            exit 1
            ;;
    esac
done

EXTRA_ARGS=()
if [ "$DRY_RUN" = true ]; then
    EXTRA_ARGS+=("--dry-run")
fi

"$PIP_COMPILE" pyproject.toml --strip-extras --output-file requirements.txt "${EXTRA_ARGS[@]}"
if [ "$INCLUDE_TEST" = true ]; then
    "$PIP_COMPILE" pyproject.toml --extra test --strip-extras --constraint requirements.txt --output-file requirements-dev.txt "${EXTRA_ARGS[@]}"
fi

echo "requirements.txt is synced with pyproject.toml"
if [ "$INCLUDE_TEST" = true ]; then
    echo "requirements-dev.txt is synced with pyproject.toml[test]"
fi
