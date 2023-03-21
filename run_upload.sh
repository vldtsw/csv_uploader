#!/usr/bin/env bash
set -e

# Set the path to the virtual environment directory
VENV_PATH="./venv"

# Set the path to the Python script to run
# This script adds data to a Google Sheet for source file reviews
SCRIPT_PATH="add_to_source_review_gsheet.py"

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python script in unbuffered mode
python -u "$SCRIPT_PATH"

# Deactivate the virtual environment
deactivate

# Prompt the user to press any key before exiting the script
# The -n1 option reads only one character at a time
# The -r option disables backslash escaping
# The -p option displays a prompt message for the user
read -n1 -r -p "Press any key to close this window..."

