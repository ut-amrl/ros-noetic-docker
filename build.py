#! /usr/bin/env python3

from internal.config import parse_args
from internal.docker import build_image


if __name__ == "__main__":
    build_image(parse_args())
