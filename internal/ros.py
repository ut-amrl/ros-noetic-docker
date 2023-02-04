import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

import internal.docker
import internal.git
from internal import logger


def clone_catkin_package(url: str, protocol: internal.git.GitHubProtocol) -> None:
    stem = Path(url).stem
    dest = Path.home() / "catkin_ws/src" / stem

    if not dest.exists():
        logger.info(f"Cloning {url}")
        internal.git.clone_repository(url, dest, protocol)


def clone_amrl_package(url: str, protocol: internal.git.GitHubProtocol) -> None:
    stem = Path(url).stem
    dest = Path.home() / "ut-amrl" / stem

    # TODO: what if the script exits before a clone finishes? git will refuse to
    # clone the repository since the directory already exists.
    if not dest.exists():
        logger.info(f"Cloning {url}")
        internal.git.clone_repository(url, dest, protocol)

    # Always run git submodule update when applicable, just in case the script
    # exited unexpectedly. This is part of the reason we aren't running
    # submodule as part of the git clone command
    if (dest / ".gitmodules").exists():
        import time

        t_start = time.time()
        logger.info(f"Updating submodules for {stem}")
        internal.git.update_submodules(dest)
        t_end = time.time()

        logger.success(f"Submodule update took {t_end-t_start:.3f}s")


def rosdep_update() -> None:
    if not os.path.exists(Path.home() / ".ros/rosdep"):
        logger.info("Running rosdep update")
        subprocess.run(["rosdep", "update"])


def _critical_build_failure() -> NoReturn:
    logger.critical("Build failed. Check build logs.")
    logger.critical("Please include the full build log if you create a GitHub issue.")
    logger.critical("https://github.com/ut-amrl/ros-noetic-docker/issues")
    sys.exit(1)


def build_catkin_packages() -> None:
    logger.info("Building catkin packages")

    # catkin_make has a tendency to not follow the dependency graph when
    # building Spot packages, so use catkin build
    try:
        subprocess.run(
            ["catkin", "build"],
            check=True,
            cwd=Path.home() / "catkin_ws",
        )

        subprocess.run(["rospack", "find", "spot_msgs"], check=True)
    except subprocess.CalledProcessError:
        _critical_build_failure()


def build_amrl_package(pkg_dir: Path) -> None:
    logger.info(f"Building {pkg_dir.stem}")
    try:
        subprocess.run(
            ["make", "-j", str(len(os.sched_getaffinity(0)))],
            check=True,
            cwd=pkg_dir.absolute(),
        )
    except subprocess.CalledProcessError:
        _critical_build_failure()
