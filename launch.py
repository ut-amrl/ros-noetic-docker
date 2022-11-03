#! /usr/bin/env python3

import argparse
import subprocess

from noetic.env import available_tags, get_env, _get_container_user

# TODO: auto-detect which tag to use
# docker images --filter "reference=$USER*" --format '{{json .}}'

# TODO: auto build the image if necessary


def launch(tag: str) -> None:
    subprocess_args = [
        "docker",
        "compose",
        "--project-directory",
        f"noetic/{tag}",
        "--project-name",
        f"{_get_container_user()}-noetic-{tag}",
        "up",
        "--detach",
    ]

    subprocess.run(subprocess_args, env=get_env())


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("tag", type=str, choices=available_tags())

    args = argparser.parse_args()

    launch(args.tag)
