# Architecture

This document outlines how this repository is organized and (functions?).

## Repository Overview

```text
├── build.py                    # Wrapper around `docker compose build`
├── internal/                   # TODO: wrapper package around docker
├── launch.py                   # Wrapper around `docker compose up`
└── noetic/
    ├── amrl-base/              # Build spec for `amrl-base` tag
    │   ├── Dockerfile
    │   ├── Makefile
    │   └── compose.yaml
    ├── dockerrc                # (pending deprecation and renaming to .dockerenv)
    └── see-spot-run/           # Build spec for `see-spot-run` tag
        ├── Dockerfile
        ├── Makefile
        ├── compose.yaml
        └── ros_packages.py     # Post-`docker build` script
```

## Design Decisions

This development of this repository is closely tied to the usage of the laptop
onboard the AMRL Spot.

### Home Directory Mounting

The primary purpose of using Docker containers on the Spot laptop is to simply
have an environment with ROS rather than the typical use cases of
containerization for isolation. We wanted the following:

- Changes to files inside the Docker container persist past the container.
  - e.g. Quick changes to a config file should not be lost if the container
    is rebuilt.
- Changes to files on the host are reflected immediately inside the Docker
  container and vice versa.
  - e.g. You cloned a repository on the host instead of inside the Docker
    container, but you want it to also just appear in the Docker container.

Thus, we mount the user's home directory on the host machine as a volume at the
same location inside the Docker container. Doing so results in some positive
side-effects:

- The Docker container exists as essentially a transparent environment on top of
  the user's home directory. The user's shell configuration on the host (e.g.
  oh-my-bash, oh-my-zsh) is available inside the Docker container without having
  to reconfigure anything. Rosbags recorded to `~/.ros` are accessible outside
  of the Docker container, e.g. to sync them to a storage server.

And some negative side-effects:

-

###


The laptop onboard the AMRL spot transitioned away from a single, shared account
towards individual accounts functioning as isolated namespaces for different
projects,

- Use the same repository for multiple accounts with minimal reconfiguration.
 -> need to discover and set user-specific properties
 -> python-based build system

- we wanted changes to files inside the container to persist outside the docker containers
 -> mounting the user's home directory as a volume inside the docker container rather than
    using an ADD/COPY
 -> also means that rosbags recorded to ~/.ros are accessible outside the Docker container, e.g. to sync them to a storage server
 -> also means that the user's shell configuration on the host is available inside the docker container, e.g if the user is using omb or omz

- fix annoying file permission errors inside the docker container
 -> mirror the user's UID on the host inside the docker container



why makefiles

each image tag might be dependent on another image tag; in Dockerfile syntax:
the "FROM" command; The FROM command does not work unless the specified image is
present. Usually, packages are downloaded from docker hub, but since we're doing
everything locally, we must build the dependence too. The docker syntax doesn't
have an instruction to do this; Makefiles have been traditionally used to
specify dependencies and are generally already installed

why python

- already installed on most linux distributions
- doesn't require the user to build anything before running
- more organized than a collection of shell scripts
- caveat: we can't depend on any packages outside the stdlib in our internal
  code

## Build Specifications (noetic/)

## Internal Build System (internal/)
