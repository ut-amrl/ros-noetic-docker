import subprocess
import os

from internal.config import Config
from internal.env import get_env, _get_container_user


def build_image(config: Config) -> None:
    subprocess_args = ["make", "-f", f"noetic/{config.tag}/Makefile"]

    subprocess.run(subprocess_args, env=get_env())
    # todo: check return code, log error and terminate if nonzero

    if config.build_ros_packages and os.path.isfile(
        f"noetic/{config.tag}/initial-setup.sh"
    ):
        subprocess.run([f"noetic/{config.tag}/initial-setup.sh"])


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


def are_we_in_the_container() -> bool:
    return os.path.exists("/dockerrc")
