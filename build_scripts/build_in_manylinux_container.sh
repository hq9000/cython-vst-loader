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

echo "=============== inspecting platform value ======================"
python inspect_platform.py

echo "=============== running a subset of unit tests ======================"
# running a subset of tests which is expected to pass in manylinux container
python -m pytest tests/test_buffers.py

mkdir -p /cython-vst-loader/dist/manylinux
ls -la /cython-vst-loader/dist
auditwheel repair --plat manylinux1_x86_64 --wheel-dir /cython-vst-loader/dist/manylinux /cython-vst-loader/dist/*.whl
rm -f /cython-vst-loader/dist/*.whl
deactivate
rm -rf ${VENV_PATH}

chmod -R 777 /cython-vst-loader/dist/*