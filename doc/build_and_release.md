# Build and Release

Binary wheels are distributed for `manylinux1_x86_64` and `win_amd64` platforms for python versions `3.7-3.9`

Currently, building and releasing is a semi-manual process.

1. Step a version by changing it in `version.txt`
2. build linux binaries
3. build windows binaries
   
2. `bash release.sh`
    - during the process, it will ask for pypi login/password
3. commit version change into git