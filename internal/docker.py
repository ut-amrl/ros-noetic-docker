import importlib
import os
import subprocess
import sys
from pathlib import Path

import internal.git
import internal.ros
from internal import logger
from internal.config import Config
from internal.env import _get_container_user, get_env


class InitialUserSetup:
    @classmethod
    def get_catkin_package_urls(cls) -> "list[str]":
        return []

    @classmethod
    def get_rosbuild_package_urls(cls) -> "list[str]":
        """These must be specified in build dependency order."""
        return []

    @classmethod
    def clone_packages(cls) -> None:
        # Log the Git SHA for build failure reproducibility.
        logger.info("git hash: " + internal.git.get_repository_hash(__file__))

        github_protocol = internal.git.get_user_protocol_preference()

        for catkin_pkg in cls.get_catkin_package_urls():
            internal.ros.clone_catkin_package(catkin_pkg, github_protocol)

        for rosbuild_pkg in cls.get_rosbuild_package_urls():
            internal.ros.clone_amrl_package(rosbuild_pkg, github_protocol)

        logger.success("Cloned package repositories")

    @classmethod
    def post_clone_packages(cls) -> None:
        pass  # override me!

    @classmethod
    def build_packages(cls) -> None:
        """This must be called in the overriding file with:

        if __name__ == "__main__":
            if internal.docker.are_we_in_the_container():
                InitialUserSetup.build_packages()
        """
        logger.info("We're inside the docker container now")

        source_dockerrc()

        internal.ros.rosdep_update()

        internal.ros.build_catkin_packages()
        # We need to grab new environment variables after the catkin build.
        source_dockerrc()

        for rosbuild_pkg in cls.get_rosbuild_package_urls():
            internal.ros.build_amrl_package(
                Path.home() / "ut-amrl" / Path(rosbuild_pkg).stem
            )

        logger.success("Build finished")

    @classmethod
    def post_build_packages(cls) -> None:
        """This is run on the host."""
        pass  # override me!


def build_image(config: Config) -> None:
    subprocess_args = ["make", "-f", f"noetic/{config.tag}/Makefile"]

    config._require_x_display = False
    subprocess.run(subprocess_args, env=get_env(config))
    # todo: check return code, log error and terminate if nonzero

    if config.with_initial_user_setup:
        try:
            tag_spec = importlib.import_module(
                f"noetic.{config.tag}.initial_user_setup"
            )
            tag_spec.InitialUserSetup.clone_packages()
            tag_spec.InitialUserSetup.post_clone_packages()

            logger.info(
                "Moving execution into the Docker container to build packages..."
            )
            config._require_x_display = False
            launch_container(config)
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    "--tty",
                    "--workdir",
                    internal.git.get_repository_root(__file__),
                    f"{_get_container_user()}-noetic-{config.tag}-app-1",
                    "python3",
                    "-m",
                    f"noetic.{config.tag}.initial_user_setup",
                ]
            )
            stop_container(config)
            if result.returncode != 0:
                sys.exit(result.returncode)

            tag_spec.InitialUserSetup.post_build_packages()
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

    subprocess.run(
        subprocess_args,
        env=get_env(config),
    )


def stop_container(config: Config) -> None:
    subprocess_args = [
        "docker",
        "stop",
        "--time",
        "0",
        f"{_get_container_user()}-noetic-{config.tag}-app-1",
    ]

    subprocess.run(subprocess_args, stdout=subprocess.DEVNULL)


def source_dockerrc() -> None:
    """Grab shell environment variables after sourcing ROS-related files."""

    result = subprocess.run(
        "SHELL=bash source /dockerrc && env",
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
