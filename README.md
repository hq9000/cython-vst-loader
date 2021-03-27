# cython-vst-loader
A loader for VST2 audio plugins providing a clean python object-oriented interface

- Supported platforms: **Linux 64bit**, **Windows 64bit**
- Supported python versions: **3.7**, **3.8**, **3.9**

In-depth documentation:
- [Usage examples](doc/usage_examples.md)
- [Setting up development environment](doc/development.md)
- [Building and releasing](doc/build_and_release.md)

home page: https://github.com/hq9000/cython-vst-loader

## Project goals
The purpose is to have a simple wrapper for VST plugins to be used in higher-level projects, such as https://github.com/hq9000/py_headless_daw

## Supported plugins

Recreating a complete VST host environment in Python is a challenging task. 
Because of that, not every plugin will work with this wrapper, many are known not to work.
Also, in case of a closed-source plugins, troubleshooting issues is almost impossible.

Because of that, the loader "officially" supports (by testing) a limited number of free and (mostly) open source plugins. 
Other plugins may or may not work, if you discover an open source plugin that is causing issues, feel free to write a bug.  

The list of (tested/known-not-to-work/reportedly-working) plugins will be refreshed as new information arrives.

Note: only 64-bit/VST2 plugins are currently supported. 

### Plugins tested on Windows

### Synths
- TAL NoiseMaker (https://tal-software.com/products/tal-noisemaker)
- TAL Elec7ro (https://tal-software.com/products/tal-elek7ro)
- DiscoDSP OB-Xd (https://www.discodsp.com/obxd/)
- Tunefish4 (https://www.tunefish-synth.com/download)

### Effects
- Dragonfly Reverb (https://michaelwillis.github.io/dragonfly-reverb/)
- TAL Reverb 2 (https://tal-software.com/products/tal-reverb)

### Plugins tested on Linux

### Synths
- amsynth (http://amsynth.github.io/)

### Effects
- Dragonfly Reverb (https://michaelwillis.github.io/dragonfly-reverb/)

## Plugins known not to work with the loader
- Synth1
- TyrellN6








## Installation

`pip install cython_vst_loader`



