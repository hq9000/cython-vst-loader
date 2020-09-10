from distutils.core import setup
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

setup(
    ext_modules=ext_modules,
    name='cython-vst-loader',  # How you named your package folder (MyLib)
    packages=['cython-vst-loader'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='a cython-based loader for VST audio plugins proving a clean python object-oriented interface',
    # Give a short description about your library
    author='Sergey Grechin',  # Type in your name
    author_email='grechin.sergey@gmail.com',  # Type in your E-Mail
    url='https://github.com/hq9000/cython-vst-loader',  # Provide either the link to your github or to your website
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',  # I explain this later on
    keywords=['vst', 'plugin', 'cython'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'validators',
        'beautifulsoup4',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
