#!/usr/bin/env bash

NEW_VERSION="$(date +%Y%m%d)"

# pyproject.toml
sed -e "s/\(^project.*,\) *version *: *'[^']*'/\1 version: '${NEW_VERSION}'/" -i meson.build

