## Some useful notes to help in development process

### Rebuilding while developing

this command builds the extension using local tools (not container):
`python setup.py build_ext --inplace`

if distributions have been made on this host (they are built in containers), your directory is expected to be pollutted with root-owned files in these directories:

- cython_vst_loader
- build

these files will not allow your local build to succeed (assuming you are not doing this with `root`). Therefore, to proceed, you will have to solve it somehow with `sudo chmod`  

