#! /usr/bin/env python3

import argparse
import subprocess
import os
import sys
from typing import NoReturn

from noetic.env import available_tags, get_env


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        self.print_help(sys.stderr)
        self.exit(2, f"\n{self.prog}: error: {message}\n")


def build(tag: str, with_initial_setup: bool) -> None:
    subprocess_args = ["make", "-f", f"noetic/{tag}/Makefile"]

    subprocess.run(subprocess_args, env=get_env())

    if with_initial_setup and os.path.isfile(f"noetic/{tag}/initial-setup.sh"):
        subprocess.run([f"noetic/{tag}/initial-setup.sh"])


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument(
        "tag",
        type=str,
        metavar="TAG",
        choices=available_tags(),
        help=f"One of {available_tags()}",
    )
    argparser.add_argument(
        "--with-initial-setup",
        action="store_true",
        help="Clone and build initial setup packages. (Not applicable to all tags)"
    )

    args = argparser.parse_args()

    build(args.tag, args.with_initial_setup)
