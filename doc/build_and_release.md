# Build and Release

## Overview
Binary wheels are distributed for `manylinux1_x86_64` and `win_amd64` platforms for python versions `3.7-3.9`

Building and publishing in PyPI are automated through github actions. The main workflow file is `.github/worksflows/build.yaml`

## When the workflow is run:
- on every push to `master` branch
- on every push to a branch that has an open `master`-targeted pull request

## Publishing to PyPI
Publishing only happens when a `tag` is put to a commit. Commits without tags still invoke builds, but the final publishing steps are omitted.

## Versioning
Care must be taken when putting tags:

- tags should use semantic versioning 
- tags of the form `1.2.3` are considered "production" and builds are pushed to the main PyPI
- tags of the form `1.2.dev3` are considered "development" and corresponding builds are pushed to test PyPI

tags of any other format are not supported and behavior is undefined.

To conveniently put tags, github "releases" can be used:
![create_release_github](https://user-images.githubusercontent.com/21345604/112721460-ea6c0e00-8f14-11eb-829d-e2ee3f3906b9.gif)
 
## Checking uploaded releases

Normally, the releases uploaded to PyPI are checked automatically in the workflow.
However, you might want to check a given release separately for some reason. 

One situation that can lead to this is the delay of pypi that makes the last jobs unable to download the package. 
Although there is a delay inserted into the workflow to account for that, it can theoretically break at some point.

For that, there is a dedicated workflow called `test_published_packages.yaml`. 
Beware that you will have to change the version to be tested in the workflow.