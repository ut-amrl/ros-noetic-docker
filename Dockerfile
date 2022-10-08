FROM osrf/ros:noetic-desktop-full-focal

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago

# Installation tools
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    software-properties-common

# Code packaging and compilation tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    g++ \
    python3-catkin-tools \
    python-is-python3 \
    python3-pip

# https://github.com/ut-amrl/amrl_shared_lib
RUN apt-get update && apt-get install -y \
    libgtest-dev libgoogle-glog-dev cmake build-essential

# https://github.com/ut-amrl/graph_navigation
RUN apt-get update && apt-get install -y \
    libgoogle-glog-dev libgflags-dev liblua5.1-0-dev

# https://github.com/ut-amrl/enml
RUN apt-get update && apt-get install -y \
    liblua5.1-dev libeigen3-dev \
    libjpeg8-dev libgoogle-perftools-dev \
    libsuitesparse-dev libblas-dev liblapack-dev libopenmpi-dev \
    libgoogle-glog-dev libgflags-dev libceres-dev libtbb-dev \
    libncurses5-dev libpopt-dev

# Utilities to make things easier inside the container. This list may be changed
# somewhat frequently, so keep it near the end of the Dockerfile to make
# rebuilds faster.
RUN apt-get update && apt-get install -y \
    clang-12 \
    clang-format \
    gdb \
    git \
    iputils-ping \
    less \
    mesa-utils \
    net-tools \
    rsync \
    tmux \
    tree \
    unzip \
    usbutils \
    vim \
    zip \
    zsh

# Add a user inside the Docker container with the same username and UID as the
# user building the container. The CONTAINER_USER and CONTAINER_UID arguments
# need to be exported accordingly in the launch-container.sh build script and
# listed again as build arguments in the docker-compose.yml file.
ARG CONTAINER_UID
ARG CONTAINER_USER
ARG CONTAINER_PASSWORD="docker"
ARG CONTAINER_HOME="/home/$CONTAINER_USER"

RUN useradd -u $CONTAINER_UID $CONTAINER_USER && \
    echo "$CONTAINER_USER:$CONTAINER_PASSWORD" | chpasswd

# /.dockerrc provides some default commands to initialize ROS and export some
# PATH environment variables. Users can source /.dockerrc in their shell init
# file, e.g.
#
#   [[ -e /.dockerrc ]] && source /.dockerrc
#
# or specify their own configuration in their shell init file.
COPY .dockerrc /.dockerrc
RUN chown $CONTAINER_USER /.dockerrc

USER $CONTAINER_USER

# TODO: "roscore" is shared between containers with the current network
# configuration. The container will fail to start if an instance of roscore is
# already running, whether on the host or within a different container. Users
# will need to manually check and launch roscore within the Docker environment
# until proper container network isolation is implemented. In the meantime, the
# sleep command keeps the container running.
CMD sleep infinity
# CMD roscore

WORKDIR $CONTAINER_HOME
