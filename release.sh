#!/bin/bash

set -e

SCRIPT_DIR=$(dirname "$0")

rm -rf dist/*
bash ${SCRIPT_DIR}/build_scripts/build_on_host.sh
twine upload dist/manylinux/*