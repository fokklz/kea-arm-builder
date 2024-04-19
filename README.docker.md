# Kea Docker Base Image

**DISCLAIMER**: This is a personal project and is not affiliated with the Internet Systems Consortium, Inc. (ISC).

**DATABASE**: PostgreSQL

[GitHub](https://github.com/fokklz/kea-arm-builder)

## Overview

This Docker image serves as a base for the Kea DHCP server and is **not functional by itself**. Kea DHCP is a high-performance, extensible DHCP server engine developed by the Internet Systems Consortium (ISC). This image is built on `alpine` and covers the following architectures:
 - `amd64`
 - `arm64`
## Contents

The following binaries are installed in `/usr/local/sbin`:

*also linked to `/usr/sbin` for convenience and compatibility with the official Kea Docker configuration files*
- `kea-admin`
- `kea-dhcp-ddns`
- `kea-dhcp4`
- `kea-dhcp6`
- `kea-ctrl-agent`
- `kea-lfc`
- `keactrl`

The following directories are created in the image, **not populated with any files**:
- `/etc/supervisor/conf.d`
- `/var/log/supervisor`	
- `/etc/kea`
- `/var/log/kea`


Example configuration files are located in `/usr/local/etc/kea` inside the container. Or at [ISC's Kea Docker repository](https://gitlab.isc.org/isc-projects/kea-docker)

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

## Additional Information

For a detailed overview of the Kea DHCP server, visit the [ISC's official Kea page](https://www.isc.org/kea/).

**Note**: A version table is provided near the end of that page.

## Caviats

- The versions `2.0.0`, `2.0.1` and `2.0.2` do not include the supervisor since i forgot to include it in the build process. Add it with `apk add supervisor` in your Dockerfile if you plan to use those versions. Also the binaries are not linked to the `/usr/sbin` folder, you will need to do that manually or use `/usr/local/sbin/` instead. Any common directories are also not created.