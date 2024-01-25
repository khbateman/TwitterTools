#!/bin/sh
cd /Users/Kenan/Library/CloudStorage/OneDrive-Personal/Personal\ Development/Python/TwitterToolsLibrary

# This is going to be deprecated so not ideal
python setup.py pytest

# Run it this way directly
python3 -m pytest tests/

# or with flag to allow printout
python3 -m pytest tests/ -s