FROM dolfinx/dev-env-real:latest
WORKDIR /tmp
# Install dependencies available via apt-get.
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get -qq update