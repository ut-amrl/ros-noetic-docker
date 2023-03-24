#! /usr/bin/env python3

from internal.config import parse_args
from internal.docker import launch_container


if __name__ == "__main__":
    launch_container(parse_args())
