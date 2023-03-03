import io
import os
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

import internal.ansi as ansi
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
        logger.info(f"Updating submodules for {stem}")
        internal.git.update_submodules(dest)


def _critical_build_failure() -> NoReturn:
    logger.critical("Build failed. Check build logs.")
    logger.critical("Please include the full build log if you create a GitHub issue.")
    logger.critical("https://github.com/ut-amrl/ros-noetic-docker/issues")
    sys.exit(1)


def _capture_process_output(process: subprocess.Popen) -> None:
    """The caller should redirect stdout to pipe and stderr to stdout."""
    if process.stdout is None:
        # no output to capture
        return

    # We'll dump all of the output if the build command fails.
    all_output_lines = []

    lines_to_clear = 0
    MAX_QUEUE_SIZE = min(10, os.get_terminal_size().lines - 2)
    MAX_LINE_WIDTH = os.get_terminal_size().columns - 4

    sentinel = b""  # bytes mode by default
    if isinstance(process.stdout, io.TextIOWrapper):
        sentinel = ""  # type: ignore

    for line in iter(process.stdout.readline, sentinel):
        if isinstance(line, bytes):
            line = line.decode()
        all_output_lines.append(line.rstrip())

        if MAX_QUEUE_SIZE > 0:
            print(
                f"{ansi.PREV_LINE}{ansi.CLEAR_LINE}" * lines_to_clear,
                end="",
                flush=True,
            )
            tail = all_output_lines[-MAX_QUEUE_SIZE:]
            tail = [line[:MAX_LINE_WIDTH] for line in tail]
            print("\n".join(tail))
            lines_to_clear = len(tail)

    print(f"{ansi.PREV_LINE}{ansi.CLEAR_LINE}" * lines_to_clear, end="", flush=True)

    if process.wait() != 0:
        print("\n".join(all_output_lines))


def rosdep_update() -> None:
    if os.path.exists(Path.home() / ".ros/rosdep"):
        return

    logger.info("Running rosdep update")

    process = subprocess.Popen(
        ["rosdep", "update"],
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )
    _capture_process_output(process)
    if process.wait() != 0:
        _critical_build_failure()


def build_catkin_packages() -> None:
    if not os.path.exists(Path.home() / "catkin_ws/src"):
        return

    logger.info("Building catkin packages")

    # catkin_make has a tendency to not follow the dependency graph when
    # building Spot packages in parallel, so build using one job
    process = subprocess.Popen(
        ["catkin_make", "-C", str(Path.home() / "catkin_ws"), "-j", "1"],
        cwd=Path.home() / "catkin_ws",
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )

    _capture_process_output(process)
    if process.wait() != 0:
        _critical_build_failure()


def build_amrl_package(pkg_dir: Path) -> None:
    logger.info(f"Building {pkg_dir.stem}")

    process = subprocess.Popen(
        ["/usr/bin/make", "-j", str(len(os.sched_getaffinity(0)))],
        cwd=pkg_dir.absolute(),
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE,
    )

    _capture_process_output(process)
    if process.wait() != 0:
        _critical_build_failure()
