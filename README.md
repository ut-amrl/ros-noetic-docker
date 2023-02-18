# ROS Noetic Docker Container

This repository houses configuration files to build and run
Docker containers tied to individual users on a shared machine.

## Prerequisites

Install Docker Engine: <https://docs.docker.com/engine/install/ubuntu>

Install the Docker Compose V2 Plugin: <https://docs.docker.com/compose/install/linux/>

If applicable, install the NVIDIA Container Toolkit: <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>

Add users to the `docker` group: <https://docs.docker.com/engine/install/linux-postinstall>

## Usage

### Add /dockerrc to your shell file

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
