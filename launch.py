#! /usr/bin/env python3

import argparse
import subprocess
import sys
from typing import NoReturn

from noetic.env import _get_container_user, available_tags, get_env

# TODO: auto-detect which tag to use
# docker images --filter "reference=$USER*" --format '{{json .}}'

# TODO: auto build the image if necessary


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_help(sys.stderr)
        self.exit(2, f"\n{self.prog}: error: {message}\n")


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
    argparser = ArgumentParser()
    argparser.add_argument(
        "tag",
        type=str,
        metavar="TAG",
        choices=available_tags(),
        help=f"One of {available_tags()}",
    )

    args = argparser.parse_args()

    launch(args.tag)
