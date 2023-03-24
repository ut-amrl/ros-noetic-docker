import os
from pathlib import Path

import internal.docker
from internal import logger


def safe_symlink(source: Path, destination: Path) -> None:
    if os.path.exists(source) and not os.path.exists(destination):
        # os.path.exists returns False for broken symbolic links, but we still
        # need to remove them
        if os.path.lexists(destination):
            os.remove(destination)

        logger.info(f"Symlinking {source} to {destination}")
        os.symlink(source, destination)


class RosPackages(internal.docker.RosPackages):
    @classmethod
    def get_catkin_package_urls(cls) -> "list[str]":
        return [
            "https://github.com/ut-amrl/spot_ros",
            "https://github.com/dawonn/vectornav",
        ]

    @classmethod
    def get_rosbuild_package_urls(cls) -> "list[str]":
        return [
            "https://github.com/ut-amrl/amrl_msgs",
            "https://github.com/ut-amrl/spot_autonomy",
            "https://github.com/ut-amrl/k4a_ros",
        ]

    @classmethod
    def post_clone_packages(cls) -> None:
        # TODO: should we just add ~/ut-amrl/graph_navigation to ROS_PACKAGE_PATH instead?
        safe_symlink(
            Path.home() / "ut-amrl/spot_autonomy/graph_navigation",
            Path.home() / "ut-amrl/graph_navigation",
        )

        safe_symlink(
            Path.home() / "ut-amrl/spot_autonomy/maps",
            Path.home() / "ut-amrl/amrl_maps",
        )

    @classmethod
    def post_build_packages(cls) -> None:
        if not os.path.exists(
            Path.home() / "ut-amrl/spot_autonomy/launch/start_clearpath_spot.launch"
        ):
            logger.attention(
                """Additional manual setup is required in ~/ut-amrl/spot_autonomy:
        1. Copy "launch/start_clearpath_spot.launch.example" to
        "launch/start_clearpath_spot.launch"
        2. In the new file, fill in your Spot robot username, password,
        and IP address.
        Never git add, commit, or push this new file."""
            )


if __name__ == "__main__":
    if internal.docker.are_we_in_the_container():
        RosPackages.build_packages()
