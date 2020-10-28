#!/bin/bash

#==================================
# This script is supposed to be
# run in a manylinux docker container
# in creates a venv for a required python
# version, install dependencies, builds extension, wheel, and, finally,
# a manylinux wheel.
#==================================

set -e

PYTHON_KEY=$1
PYTHON_EXECUTABLE=/opt/python/${PYTHON_KEY}/bin/python
VENV_PATH="/root/tmp_venv_${PYTHON_KEY}"
SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="${SCRIPT_DIR}/../"

$PYTHON_EXECUTABLE -m venv ${VENV_PATH}
source ${VENV_PATH}/bin/activate

cd /cython-vst-loader || exit
pip install -r requirements.txt
pip install wheel
python setup.py build_ext --inplace
python setup.py bdist_wheel

mkdir -p /cython-vst-loader/dist/manylinux
auditwheel repair --plat manylinux1_x86_64 --wheel-dir /cython-vst-loader/dist/manylinux /cython-vst-loader/dist/*.whl
rm -f /cython-vst-loader/dist/*.whl
deactivate
rm -rf ${VENV_PATH}

chmod -R 777 /cython-vst-loader/dist/*