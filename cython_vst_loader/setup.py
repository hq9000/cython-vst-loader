from distutils.core import setup
from pathlib import Path

from Cython.Build import cythonize

this_directory = Path(__file__).parents[0]

include_paths = [
    this_directory.as_posix() + "/../c/vendor/vstsdk/pluginterfaces/vst2.x"
]

ext_modules = cythonize(
    'vst_loader_wrapper.pyx',
    compiler_directives={'language_level': "3"}
)

# workaround for https://github.com/cython/cython/issues/1480
for module in ext_modules:
    module.include_dirs = include_paths
    module.extra_compile_args = [
        "-Wno-unused-function"
    ]

setup(ext_modules=ext_modules)
