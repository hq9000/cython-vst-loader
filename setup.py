# from distutils.core import setup
import setuptools
from pathlib import Path
import os

from setuptools import Extension

USE_CYTHON = True

try:
    # noinspection PyUnresolvedReferences
    from Cython.Build import cythonize
except ImportError:
    USE_CYTHON = False

this_directory = Path(__file__).parents[0]

os.system("make")

include_paths = [
    this_directory.as_posix() + "/build/vstsdk/pluginterfaces/vst2.x"
]

if USE_CYTHON:
    ext_modules = cythonize(
        'cython_vst_loader/vst_loader_wrapper.pyx',
        compiler_directives={'language_level': "3"}
    )
else:
    ext_modules = [
        Extension("cython_vst_loader.vst_loader_wrapper", ["cython_vst_loader/vst_loader_wrapper.c"]),
    ]

# workaround for https://github.com/cython/cython/issues/1480
for module in ext_modules:
    module.include_dirs = include_paths
    module.extra_compile_args = [
        "-Wno-unused-function"
    ]
with open(str(this_directory) + '/README.md', encoding='utf-8') as f:
    long_description = f.read()

with open(str(this_directory) + '/version.txt', encoding='utf-8') as f:
    version = f.read()

setuptools.setup(
    ext_modules=ext_modules,
    name='cython_vst_loader',
    packages=['cython_vst_loader'],
    version=version,
    license='MIT',
    description='a cython-based loader for VST audio plugins providing a clean python object-oriented interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sergey Grechin',  # Type in your name
    author_email='grechin.sergey@gmail.com',
    url='https://github.com/hq9000/cython-vst-loader',
    keywords=['vst', 'plugin', 'cython'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
