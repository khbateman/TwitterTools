#!/bin/sh
cd /Users/Kenan/Library/CloudStorage/OneDrive-Personal/Personal\ Development/Python/TwitterToolsLibrary

# create the wheel file in /dist
python setup.py bdist_wheel

# reinstall this file by pip installing the newest file in that directory
cd dist
most_recent_file=$(ls -t | head -1)
pip install "$most_recent_file"