#! /usr/bin/env python3

import argparse
import subprocess

from noetic.env import available_tags, get_env


def build(tag: str) -> None:
    subprocess_args = ["make", "-f", f"noetic/{tag}/Makefile"]

    subprocess.run(subprocess_args, env=get_env())


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("tag", type=str, choices=available_tags())

    args = argparser.parse_args()

    build(args.tag)
