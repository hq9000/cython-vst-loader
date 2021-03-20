# Dev Env in Windows

## my initial setup:

Win10, it's 2021.02.28 out there.

## Installing the Visual Studio compiler
1. to get a compiler, I'm now installing a "Visual Studio Community" from here: https://visualstudio.microsoft.com/vs/community/
2. after launching the installer, from the many options it gives me, I only choose "development of classical apps", the expected installation size is terrifying 7Gbs.

## Setting up a linux-like environment using git-bash

### Installing git-bash

Git bash comes with git for windows

### Installing make and wget

These two are needed to download VSTSDK. To install them into the mingw supplied withing git bash, I followed this instruction [here](https://gist.github.com/evanwill/0207876c3243bbb6863e65ec5dc3f058):
below is an extract from that doc:

> ## Make
> 
> Keep in mind you can easy add `make`, but it doesn't come packaged with all the standard UNIX build toolchain--so you will have to ensure those are installed *and* on your PATH, or you will encounter endless error messages.
> - Go to [ezwinports](https://sourceforge.net/projects/ezwinports/files/).
> - Download `make-4.1-2-without-guile-w32-bin.zip` (get the version without guile).
> - Extract zip.
> - Copy the contents to your `Git\mingw64\` merging the folders, but do NOT overwrite/replace any existing files. 
> 
> ## Wget 
> - Download the latest wget binary for windows from [eternallybored](https://eternallybored.org/misc/wget/) (they are available as a zip with documentation, or just an exe)
> - If you downloaded the zip, extract all (if windows built in zip utility gives an error, use [7-zip](http://www.7-zip.org/)).
> - Rename the file `wget64.exe` to `wget.exe` if necessary. 
> - Move `wget.exe` to your `Git\mingw64\bin\`.
 
Essentially, it all comes down to copying a few additional files into `c:\Program Files\Git\mingw64` as shown on the screenshots below:

![image](https://user-images.githubusercontent.com/21345604/111060267-9db41c00-84ac-11eb-8d14-bc7fb1f0f484.png)
![image](https://user-images.githubusercontent.com/21345604/111060356-61cd8680-84ad-11eb-997a-0044763fd7d9.png)

## Install Pythons and create venvs

Download from here `https://www.python.org/downloads/` and install python 3.7, 3.8, 3.9 

In my case, python binaries end up here: `C:\Users\user\AppData\Local\Programs\Python\`

![image](https://user-images.githubusercontent.com/21345604/111866019-71e8d880-897b-11eb-8870-91319cbbdaa4.png)

create venvs:

- `/c/Users/user/AppData/Local/Programs/Python/Python37/python.exe -m venv /c/home/em/test_python/venv37`
- `/c/Users/user/AppData/Local/Programs/Python/Python38/python.exe -m venv /c/home/em/test_python/venv38`
- `/c/Users/user/AppData/Local/Programs/Python/Python39/python.exe -m venv /c/home/em/test_python/venv39`


### Building the extension

- launch git-bash
- Activate venv: `source venv/Scripts/activate`
- finally, build `python setup.py build_ext --inplace`

### Plugins used for testing

- [TyrellN6](https://www.amazona.de/freeware-synthesizer-tyrell-n6-plugin-vst-au-win-mac/) win64 dll
- [Dexed](https://asb2m10.github.io/dexed/)
- [Surge](https://github.com/surge-synthesizer/releases/releases/tag/1.6.6)

### Where to find python in windows


