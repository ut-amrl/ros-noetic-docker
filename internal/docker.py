import importlib
import os
import subprocess

from internal import logger
from internal.config import Config
from internal.env import _get_container_user, get_env


def build_image(config: Config) -> None:
    subprocess_args = ["make", "-f", f"noetic/{config.tag}/Makefile"]

    subprocess.run(subprocess_args, env=get_env())
    # todo: check return code, log error and terminate if nonzero

    if config.build_ros_packages:
        try:
            tag_spec = importlib.import_module(f"noetic.{config.tag}.ros_packages")
            tag_spec.host_entrypoint(config)
        except ImportError:
            logger.error(f"No build spec for {config.tag}")


def launch_container(config: Config) -> None:
    subprocess_args = [
        "docker",
        "compose",
        "--project-directory",
        f"noetic/{config.tag}",
        "--project-name",
        f"{_get_container_user()}-noetic-{config.tag}",
        "up",
        "-t",
        "0",
        "--detach",
    ]

    subprocess.run(subprocess_args, env=get_env())


def source_dockerrc() -> None:
    """Grab shell environment variables after sourcing ROS-related files."""

    result = subprocess.run(
        "source /dockerrc && env",
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True,
    )
    for line in result.stdout.splitlines():
        key, _, value = line.partition("=")
        os.environ[key] = value


def are_we_in_the_container() -> bool:
    return os.path.exists("/dockerrc")
