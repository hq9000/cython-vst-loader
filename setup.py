# from distutils.core import setup
import setuptools
from pathlib import Path
import os

from Cython.Build import cythonize

this_directory = Path(__file__).parents[0]

os.system("make")

include_paths = [
    this_directory.as_posix() + "/build/vstsdk/pluginterfaces/vst2.x"
]

ext_modules = cythonize(
    'cython_vst_loader/vst_loader_wrapper.pyx',
    compiler_directives={'language_level': "3"}
)

# workaround for https://github.com/cython/cython/issues/1480
for module in ext_modules:
    module.include_dirs = include_paths
    module.extra_compile_args = [
        "-Wno-unused-function"
    ]

setuptools.setup(
    ext_modules=ext_modules,
    name='cython_vst_loader',
    packages=['cython_vst_loader'],
    version='0.1',
    license='MIT',
    description='a cython-based loader for VST audio plugins proving a clean python object-oriented interface',
    author='Sergey Grechin',  # Type in your name
    author_email='grechin.sergey@gmail.com',
    url='https://github.com/hq9000/cython-vst-loader',
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    keywords=['vst', 'plugin', 'cython'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Cython'
    ],
    install_requires=[
        'Cython>=0.29.19'
    ]
)
