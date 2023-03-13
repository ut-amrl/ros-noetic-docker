# Noetic Build Details

The Docker images are designed in such a way that multiple users can share the
same underlying image, with container instances acting as namespaces. The only
user inside each container is the user who launched the docker and only this
user's home directory is mounted in the container.

## [`env.py`](env.py)

This script retrieves environment variables used by the build and launch
scripts. Running the script as a file prints the list of environment variables.

```shell
python3 env.py

# or from the top-level directory,
python3 noetic/env.py
```

## Tags

The base name for images is $USER-noetic, and each directory specifies specifies
an image "tag" under the image repository. Although images may have different
names, they can share the same id

```
$ docker images

REPOSITORY      TAG            IMAGE ID       CREATED      SIZE
user2-noetic    see-spot-run   000000000002   5 days ago   4.6GB
elvin-noetic    see-spot-run   000000000002   5 days ago   4.6GB
user2-noetic    amrl-base      000000000001   5 days ago   4.44GB
elvin-noetic    amrl-base      000000000001   5 days ago   4.44GB
```

Images may diverge if one user makes a change and rebuilds; the image used
by another user will remain unchanged.

```
$ docker images

REPOSITORY      TAG            IMAGE ID       CREATED          SIZE
user2-noetic    see-spot-run   000000000004   10 seconds ago   4.61GB
user2-noetic    amrl-base      000000000003   30 seconds ago   4.45GB
elvin-noetic    see-spot-run   000000000002   5 days ago       4.6GB
elvin-noetic    amrl-base      000000000001   5 days ago       4.44GB
```

Each tag directory is expected to contain the following files:

```text
<tag>/
├── compose.yaml
├── Dockerfile
└── Makefile
```

Builds are organized into a dependency chain using Makefiles.

## Compose Files

user-specific configuration exists in the compose file instead of the Dockerfile
(sort of like specifying at runtime instead of compile time)

### Build Context

context in the noetic/ dir ; since files mounted as volumes must be in the context;
and some files may be shared between tags (e.g. dockerrc)

### Volumes

user directory
dockerrc

cuda, libtorch
binds /etc/passwd and /etc/group into the container


### User

bind both the uid and gid otherwise the user will have a gid of 0, assume they're the same

Since user binding is done at commpose-time, we can't do some things inside the container
(like running rosdep update), because we're mapping the entire user folder
