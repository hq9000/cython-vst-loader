#!/bin/bash

#==================================
# This is a driver script to be
# executed on a development host.
# Internally, it starts manylinux docker
# containers and runs build_in_manilinux_container.sh
# inside the container for different
# python versions.
#==================================

set -e

SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="${SCRIPT_DIR}/../"

rm -rf ${PROJECT_DIR}/dist/*
echo "about to build for 3.7 manylinux"
docker run --rm -t -v .:/cython-vst-loader quay.io/pypa/manylinux2010_x86_64:latest bash /cython-vst-loader/build_scripts/build_in_manylinux_container.sh cp37-cp37m
echo "done building for 3.7 manylinux"

echo "about to build for 3.8 manylinux"
docker run --rm -t -v .:/cython-vst-loader quay.io/pypa/manylinux2010_x86_64:latest bash /cython-vst-loader/build_scripts/build_in_manylinux_container.sh cp38-cp38
echo "done building for 3.8 manylinux"

echo "about to build for 3.9 manylinux"
docker run --rm -t -v .:/cython-vst-loader quay.io/pypa/manylinux2010_x86_64:latest bash /cython-vst-loader/build_scripts/build_in_manylinux_container.sh cp39-cp39
echo "done building for 3.9 manylinux"
