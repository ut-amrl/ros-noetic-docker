# ROS Noetic Docker Container

This repository houses configuration files to build and run
Docker containers tied to individual users on a shared machine.

## Prerequisites

Install Docker Engine: <https://docs.docker.com/engine/install/ubuntu>

Install the Docker Compose V2 Plugin: <https://docs.docker.com/compose/install/compose-plugin>

If applicable, install the NVIDIA Container Toolkit: <https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html>

Add users to the `docker` group: <https://docs.docker.com/engine/install/linux-postinstall>

## Usage

### Add /dockerrc to your shell file

```shell
[[ -e /dockerrc ]] && source /dockerrc
```

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

### Stop your Docker container

This might take a few seconds to finish running.

```shell
docker stop $USER-noetic-<tag>-app-1
```
