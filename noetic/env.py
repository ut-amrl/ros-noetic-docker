#! /usr/bin/env python3

import getpass
import json
import os
import os.path
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any


def _get_container_user() -> str:
    return getpass.getuser()


def _get_container_uid() -> str:
    return str(os.getuid())


def _get_container_host() -> str:
    return platform.node()


def _get_container_runtime() -> str:
    # https://docs.docker.com/engine/reference/commandline/info/#format-the-output
    subprocess_args = ["docker", "info", "--format={{json .}}"]

    result = subprocess.run(subprocess_args, stdout=subprocess.PIPE, text=True)
    info: "dict[str, Any]" = json.loads(result.stdout)

    if "nvidia" in info["Runtimes"].keys():
        return "nvidia"
    else:
        return info["DefaultRuntime"]


def _get_x_display_device() -> str:
    # Sometimes an X display device can be opened, but applications cannot use
    # it. If this display device is used inside the Docker container, k4a_ros
    # will launch without printing any errors, but no messages will be
    # published. This happens when multiple users are logged into the computer's
    # GUI and the chosen display device does not belong to the user who last
    # logged into the GUI. We can can detect this ahead of time with "glxinfo",
    # which will hang indefinitely after opening the display device, unable to
    # query information about the display device.
    #
    # "xdpyinfo" is an alternative command from the x11-utils package that is
    # generally already installed with the system, but it is unable to detect
    # this case.
    display_device = ""

    if shutil.which("glxinfo") is None:
        print(
            """Error: command not found: glxinfo
    This script uses the glxinfo command from the mesa-utils package to detect
    accessible X display devices. An X display device is required for GUI
    applications and the Azure Kinect DK SDK.

    Steps to resolve:
        - Install glxinfo with 'sudo apt install mesa-utils'
"""
        )

        continue_anyway = input("Continue anyway? [y/n]: ")
        if not continue_anyway.lower().startswith("y"):
            return ""
        else:
            raise FileNotFoundError("glxinfo")
    else:
        for display_num in range(100):
            subprocess_args = ["glxinfo", "-display", f":{display_num}"]

            try:
                result = subprocess.run(
                    subprocess_args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=0.5,
                )
                if result.returncode == 0:
                    display_device = subprocess_args[2]
                    break
            except subprocess.TimeoutExpired:
                pass

    if display_device == "":
        print(
            """Warning: Unable to access an X display device.
    An X display device is required for GUI applications and the Azure Kinect DK
    SDK.

    Steps to resolve for building over ssh:
        - Log into the computer's GUI
        - Verify that the $DISPLAY environment variable is set in the GUI
        - Allow any host to access the X server by running 'xhost +' in a
          terminal
        - Lock, but do not log out of, the computer's GUI
"""
        )

        continue_anyway = input("Continue anyway? [y/n]: ")
        if continue_anyway.lower().startswith("y"):
            return ""
        else:
            raise RuntimeError("No X display device detected.")

    return display_device


def available_tags() -> "list[str]":
    tags = []

    noetic_dir = Path(__file__).parent
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


def get_env() -> "dict[str, str]":
    return {
        "CONTAINER_HOST": _get_container_host(),
        "CONTAINER_RUNTIME": _get_container_runtime(),
        "CONTAINER_UID": _get_container_uid(),
        "CONTAINER_USER": _get_container_user(),
        "DISPLAY": _get_x_display_device(),
        "DOCKER_SCAN_SUGGEST": "false",
    }


if __name__ == "__main__":
    for k, v in get_env().items():
        print(f"{k}={v}")
