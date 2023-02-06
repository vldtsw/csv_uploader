#!/usr/bin/env bash
set -e

VENV_PATH="./venv"
SCRIPT_PATH="add_to_source_review_gsheet.py"

source "$VENV_PATH/bin/activate"
python -u "$SCRIPT_PATH"
deactivate