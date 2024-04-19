# Kea ARM Builder

**DISCLAIMER**: This is a personal project and is not affiliated with the Internet Systems Consortium, Inc. (ISC).


## Overview

This repository contains the files used to build the `kea-base` image for `ARM64` and `AMD64` architectures based on the `alpine` image.

The python script `main.py` is used to get the latest version of `kea` not yet built and published in the `docker hub` and build the image for the `ARM64` and `AMD64` architectures.

The goal of this repository is to provide insight on how its built if your interested. I'd recommend using the [docker hub image](https://hub.docker.com/r/fokklz/kea-base) instead of building it yourself.

**Does not yet include anything related to premium, you will need to include that at your own**

## Usage

```Dockerfile

FROM fokklz/kea-base:latest

# include your kea configuration files
# create your "way" of initializing the kea server
# you can have a look at the kea-docker image examples to get an idea of how to do it 

# https://gitlab.isc.org/isc-projects/kea-docker
# the upper cloudsmith part can be ignored since the binaries are already included in the image
```