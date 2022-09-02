#! /usr/bin/env bash

set -e

# Use the current user's name and UID during build and inside the Docker
# container to:
#  - Allow multiple users on the same machine to build their own copy of
#    this container using the same configuration files.
#  - Launch directly into the current user's home directory inside Docker.
#  - Share the host user's audio socket.
#  - Have files created within the docker container have the same owner
#    instead of root.
#
# $USER is an environment variable, but $UID is generally a shell variable
# that we don't have access to here.
export CONTAINER_UID="$(id -u)"
export CONTAINER_USER=$USER

export CONTAINER_RUNTIME="runc"
if [[ "$(docker info |& grep 'Runtimes:')" == *"nvidia"* ]]; then
    export CONTAINER_RUNTIME="nvidia"
fi

# Libtorch is pretty large (~3-4 GB) and can be shared by multiple
# containers, so it's mounted as a volume in the docker container.
# Check if it exists on the host filesystem.
if [[ ! -d /opt/libtorch ]]; then
    # Check the installed CUDA runtime version by parsing nvidia-smi output.
    if command -v nvidia-smi &> /dev/null; then
        CUDA_VERSION="$(
            nvidia-smi --query --unit |
            grep "CUDA Version" |
            grep --perl-regex --only-matching "\d+(\.\d+)*"
        )"
        TORCH_PLATFORM="CUDA (<= $CUDA_VERSION)"
    else
        TORCH_PLATFORM="CPU"
    fi

    echo "Warning: Missing dependency: /opt/libtorch does not exist"
    echo "  Required for https://github.com/ut-amrl/graph_navigation"
    echo ""
    echo "  From https://pytorch.org, download"
    echo "    [Stable] [Linux] [LibTorch] [C++] [$TORCH_PLATFORM] [cxx11 ABI]"
    echo "  Unzip the file to /opt (may require sudo), e.g."
    echo "    unzip -q -d /opt libtorch.zip"
    echo ""
    read -p "Continue anyway? [y/n]: " user_input
    if [[ "$user_input" != [Yy]* ]]; then
        exit 1
    fi
fi

# Make sure --project-name matches the image name prefix in docker-compose.yml
docker compose --project-name ${CONTAINER_USER}-ros-noetic up --build --detach
