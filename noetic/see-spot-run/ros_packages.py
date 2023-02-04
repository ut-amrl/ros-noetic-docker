import os
import subprocess
import sys
from pathlib import Path

import internal.docker
import internal.git
import internal.ros
from internal import logger
from internal.config import Config
from internal.env import _get_container_user

catkin_pkgs = [
    "https://github.com/ut-amrl/spot_ros",
    "https://github.com/dawonn/vectornav",
]

# These must be topologically sorted according to the dependency graph.
amrl_pkgs = [
    "https://github.com/ut-amrl/amrl_msgs",
    "https://github.com/ut-amrl/spot_autonomy",
    "https://github.com/ut-amrl/k4a_ros",
]


def check_clearpath_launch() -> None:
    if not os.path.exists(
        Path.home() / "ut-amrl/spot_autonomy/launch/start_clearpath_spot.launch"
    ):
        logger.warning(
            """Manual setup is required in ~/ut-amrl/spot_autonomy:
    Replicate launch/start_clearpath_spot.launch.example to
    launch/start_clearpath_spot.launch, filling in your Spot
    robot username, password, and IP address."""
        )


def host_entrypoint(config: Config) -> None:
    # Log the Git SHA for build failure reproducibility.
    logger.info("git hash: " + internal.git.get_repository_hash(__file__))

    github_protocol = internal.git.get_user_protocol_preference()

    for catkin_pkg in catkin_pkgs:
        internal.ros.clone_catkin_package(catkin_pkg, github_protocol)

    for amrl_pkg in amrl_pkgs:
        internal.ros.clone_amrl_package(amrl_pkg, github_protocol)

    # TODO: should we just add ~/ut-amrl/graph_navigation to ROS_PACKAGE_PATH instead?
    if not os.path.exists(Path.home() / "ut-amrl/graph_navigation"):
        logger.info(
            "Symlinking ~/ut-amrl/spot_autonomy/graph_navigation to ~/ut-amrl/graph_navigation"
        )
        os.symlink(
            Path.home() / "ut-amrl/spot_autonomy/graph_navigation",
            Path.home() / "ut-amrl/graph_navigation",
            target_is_directory=True,
        )

    logger.success("Cloned package repositories")
    logger.info("Moving execution into the Docker container to build packages...")

    internal.docker.launch_container(config)

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
            f"noetic.{config.tag}.ros_packages",
        ]
    )
    if result.returncode != 0:
        sys.exit(result.returncode)

    check_clearpath_launch()


def container_entrypoint() -> None:
    logger.info("We're inside the docker container now")

    internal.docker.source_dockerrc()
    for k, v in os.environ.items():
        if k.startswith("ROS"):
            logger.info(f"{k}={v}")

    internal.ros.rosdep_update()

    # http://www.clearpathrobotics.com/assets/guides/melodic/spot-ros/ros_setup.html
    subprocess.run(
        ["rosdep", "install", "--from-paths", "src", "--ignore-src", "-y"],
        cwd=Path.home() / "catkin_ws",
    )

    internal.ros.build_catkin_packages()
    # We need to grab new environment variables after the catkin build.
    internal.docker.source_dockerrc()

    for amrl_pkg in amrl_pkgs:
        internal.ros.build_amrl_package(Path.home() / "ut-amrl" / Path(amrl_pkg).stem)

    logger.success("Build finished")


if __name__ == "__main__":
    if internal.docker.are_we_in_the_container():
        container_entrypoint()
