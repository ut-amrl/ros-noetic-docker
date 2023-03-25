# ROS Noetic Docker Container

This repository houses configuration files to build and run
Docker containers tied to individual users on a shared machine.

## Prerequisites

Install Docker Engine: <https://docs.docker.com/engine/install/ubuntu>

Install the Docker Compose V2 Plugin: <https://docs.docker.com/compose/install/linux/>

If applicable, install the NVIDIA Container Toolkit: <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>

Add users to the `docker` group: <https://docs.docker.com/engine/install/linux-postinstall>

## Usage

### Source `/.dockerenv` in your shell file

`/.dockerenv` contains recommended default ROS-related environment variables for
the Docker container.

```shell
# This line checks for the existence of /.dockerenv and sources the file only if
# it exists. Add it to your shell initialization file manually or using one of #
# the commands below.
[[ -e /.dockerenv ]] && source /.dockerenv

# Bash
echo "[[ -e /.dockerenv ]] && source /.dockerenv" >> ~/.bashrc

# Zsh
echo "[[ -e /.dockerenv ]] && source /.dockerenv" >> ~/.zshrc
```

Alternatively, you may specify your own ROS environment variables in your shell
file.

### Build and start your Docker container

```shell
./build.py <tag>
```

```shell
./launch.py <tag>
```

### Verify that your Docker container is running

```shell
$ docker container ls

# Or its shorthand
$ docker ps
```

Under the `NAMES` column, there should be a container with the name
`${YOUR_USERNAME}-noetic-<tag>-app-1`.

### Start a shell session in your Docker container

```shell
docker exec -it $USER-noetic-<tag>-app-1 [bash|zsh]
```

If you run into missing ROS packages, set the ROS_PACKAGE_PATH appropriately:

```shell
export ROS_PACKAGE_PATH=$ROS_PACKAGE_PATH:<path_containing_package>
```

### Stop your Docker container

This might take a few seconds to finish running.

```shell
docker stop $USER-noetic-<tag>-app-1
```
