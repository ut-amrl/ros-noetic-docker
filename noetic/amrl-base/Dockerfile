FROM osrf/ros:noetic-desktop-full-focal

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago

# Package installation tools
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    python-is-python3 \
    python3-catkin-tools \
    python3-pip \
    software-properties-common

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

# https://github.com/ut-amrl/webviz
# https://github.com/ut-amrl/robofleet_client
RUN apt-get update && apt-get install -y \
    cmake qt5-default libqt5websockets5-dev

# Development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    clang-12 \
    clang-format \
    cmake \
    g++ \
    gdb \
    git \
    valgrind \
    vim

# Additional utilities to make things easier inside the container.
RUN apt-get update && apt-get install -y \
    iputils-ping \
    less \
    mesa-utils \
    net-tools \
    rsync \
    tmux \
    tree \
    unzip \
    usbutils \
    zip \
    zsh

# TODO: "roscore" is shared between containers with the current network
# configuration. The container will fail to start if an instance of roscore is
# already running, whether on the host or within a different container. Users
# will need to manually check and launch roscore within the Docker environment
# until proper container network isolation is implemented. In the meantime, the
# sleep command keeps the container running.
CMD sleep infinity
# CMD roscore
