import argparse
import dataclasses
import sys
from typing import NoReturn

from internal.env import available_tags


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        """Print the full help message instead of the usage message on an
        error.
        """
        self.print_help(sys.stderr)
        self.exit(2, f"\n{self.prog}: error: {message}\n")


@dataclasses.dataclass
class Config:
    tag: str
    with_initial_user_setup: bool = False
    _require_x_display: bool = True


def parse_args() -> Config:
    argparser = ArgumentParser()
    argparser.add_argument(
        "tag",
        type=str,
        metavar="TAG",
        choices=available_tags(),
        help=f"One of {available_tags()}",
    )
    argparser.add_argument(
        "--with-initial-user-setup",
        action="store_true",
        help="[Beta] (Build only) Also set up initial ROS packages.",
    )

    args = argparser.parse_args()
    config = Config(**vars(args))
    return config
