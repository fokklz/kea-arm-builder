# Use a specific version of alpine for better reproducibility
# also this image has 0 known vulnerabilities
FROM alpine:3.16 as builder

# Set the Kea version as an argument for easy updates
ARG VERSION=2.4.1

# Install necessary packages and build dependencies
RUN apk update && apk add --no-cache wget tar \
    automake make autoconf libtool postgresql-dev g++ binutils log4cplus-dev boost-dev \
    && wget https://downloads.isc.org/isc/kea/${VERSION}/kea-${VERSION}.tar.gz \
    && tar -xzvf kea-${VERSION}.tar.gz \
    && rm kea-${VERSION}.tar.gz \
    && cd kea-${VERSION} \
    && autoreconf --install \
    && ./configure --with-psql \
    && make -j$(nproc) \
    && make install \
    && cd .. \
    && rm -rf kea-${VERSION} \
    && find /usr/local/lib -name '*.a' -exec rm -f {} +

# Use a clean alpine image for the final stage
FROM alpine:3.16

# Copy the built Kea from the builder stage
COPY --from=builder /usr/local /usr/local

# Install runtime dependencies
RUN apk add --no-cache libpq log4cplus boost tzdata openntpd postgresql-client supervisor \
    # Remove the example config file for supervisor
    && rm -f /etc/supervisord.conf \
    # Create commmonly used directories
    && mkdir -p /etc/supervisor/conf.d /etc/kea /var/log/supervisor /var/log/kea \
    # Create a symlink for the Kea binaries (to work with the example config files)
    && ln -s /usr/local/sbin/kea-dhcp4 /usr/sbin/kea-dhcp4 \
    && ln -s /usr/local/sbin/kea-dhcp6 /usr/sbin/kea-dhcp6 \
    && ln -s /usr/local/sbin/kea-ctrl-agent /usr/sbin/kea-ctrl-agent \
    && ln -s /usr/local/sbin/kea-admin /usr/sbin/kea-admin \
    && ln -s /usr/local/sbin/kea-dhcp-ddns /usr/sbin/kea-dhcp-ddns
