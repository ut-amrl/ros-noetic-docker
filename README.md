# ROS Noetic Docker Container

This repository houses configuration files to build and run
Docker containers tied to individual users on a shared machine.

## Table of Contents

TODO

## Host Machine Setup

Install Docker Engine: <https://docs.docker.com/engine/install/ubuntu>

(as opposed to Docker Desktop, unless you already have it installed)
on robots you'll typically want docker engine, as docker desktop creates a VM that
can take unnecessary RAM

Install the Docker Compose V2 Plugin: <https://docs.docker.com/compose/install/linux/>

(this is usually installed already on newer docker versions, check whether `docker compose version`)
outputs a version number or tells you that it does not know what "compose" means; if the latter,
you'll need to install docker compose

If you intend to use CUDA within the Docker container, install the NVIDIA Container Toolkit: <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>

Add users to the `docker` group: <https://docs.docker.com/engine/install/linux-postinstall>

## Usage

### [Recommended] Source `/.dockerenv` to your shell file

`/.dockerenv` initializes some default ROS-related environment variables.

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

### [Deprecated] Add /dockerrc to your shell file

`/dockerrc` provides default commands to initialize ROS and associated PATH
environment variables. Users can use these defaults by sourcing `/dockerrc` in
their shell files, e.g.

```shell
[[ -e /dockerrc ]] && source /dockerrc
```

or specify their own configuration in their shell init file.

### Build and start your Docker container

```shell
./build.py <tag>
# e.g. `./build.py see-spot-run`
# Run `./build.py -h` to view a list of available tags
```

```shell
./launch.py <tag>
# e.g. `./launch.py see-spot-run`
# Run `./launch.py -h` to view a list of available tags
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

### When opening a new shell in the container
re-run
```shell
[[ -e /dockerrc ]] && source /dockerrc
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
