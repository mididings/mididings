#!/usr/bin/env bash

NEW_VERSION="$(date +%Y%m%d)"

# pyproject.toml
sed -e "s/^version =.*/version = \"${NEW_VERSION}\"/" -i pyproject.toml

# doc/conf.py
sed -e "s/^version.*/version = \"${NEW_VERSION}\"/" -i doc/conf.py

