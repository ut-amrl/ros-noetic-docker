# ROS Noetic Docker Container

This repository houses configuration files to build and run
Docker containers tied to individual users on a shared machine.

## Prerequisites

Install Docker Engine: <https://docs.docker.com/engine/install/ubuntu>

Install the Docker Compose V2 Plugin: <https://docs.docker.com/compose/install/compose-plugin>

If applicable, install the NVIDIA Container Toolkit: <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>

Add users to the `docker` group: <https://docs.docker.com/engine/install/linux-postinstall>

## Usage

### Build and start your Docker container

This script always rebuilds the Docker container before starting the
container in detached mode.

```shell
./launch-container.sh
```

### Verify that your Docker container is running

```shell
$ docker container ls

# Or its shorthand
$ docker ps
```

Under the `NAMES` column, there should be a container with the name
`${YOUR_USERNAME}-ros-noetic-app-1`.

### Start a shell session in your Docker container

```shell
docker exec -it $USER-ros-noetic-app-1 [sh|bash|zsh]
```

### Stop your Docker container

This might take a few seconds to finish running.

```shell
docker stop $USER-ros-noetic-app-1
```