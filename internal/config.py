import argparse
import dataclasses
import os
import sys
from pathlib import Path
from typing import NoReturn


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


def available_tags() -> "list[str]":
    tags = []

    noetic_dir = Path(__file__).parent.parent / "noetic"
    for entry in os.listdir(noetic_dir):
        entry_path = noetic_dir / entry
        if (
            os.path.isdir(entry_path)
            and os.path.isfile(entry_path / "Dockerfile")
            and os.path.isfile(entry_path / "Makefile")
            and os.path.isfile(entry_path / "compose.yaml")
        ):
            tags.append(entry)

    return tags


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
