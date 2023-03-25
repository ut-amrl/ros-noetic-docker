#! /usr/bin/env python3

import getpass
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any

import internal.ansi as ansi
from internal import logger
from internal.config import Config


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
        return info["DefaultRuntime"]  # type: ignore


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

    SKIP_INDICATOR_FILE = Path("internal/.skip_get_x_display_device")
    if SKIP_INDICATOR_FILE.exists():
        logger.info("Skipping DISPLAY check.")
        return display_device

    if shutil.which("glxinfo") is None:
        logger.warning(
            f"""Command not found: glxinfo
    This script uses the glxinfo command from the mesa-utils package to detect
    accessible X display devices. An X display device is required for GUI
    applications and the Azure Kinect DK Camera SDK.
{ansi.BOLD}{ansi.WHITE}
    Would you like to ignore this warning?

    If you do not use GUI applications or the Azure Kinect DK Camera, you may
    ignore this warning.

    Your options are:
        YES    : Ignore once. This warning will appear again in the future.
        ALWAYS : Always ignore this warning.
        NO     : Follow the steps below to resolve this warning.
{ansi.NO_BOLD}{ansi.YELLOW}
    Steps to resolve this warning:
        - Install glxinfo with 'sudo apt install mesa-utils'
"""
        )

        ignore_warning = input("Ignore this warning? [YES/ALWAYS/NO]: ").strip().lower()
        if ignore_warning.startswith("a"):
            SKIP_INDICATOR_FILE.touch(exist_ok=True)
            return display_device
        elif ignore_warning.startswith("y"):
            return display_device
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
        logger.warn(
            f"""Unable to remotely access an X display device.
    An X display device is required for GUI applications and the Azure Kinect DK
    Camera SDK.
{ansi.BOLD}{ansi.WHITE}
    Would you like to ignore this warning?

    If you do not use GUI applications or the Azure Kinect DK Camera, you may
    ignore this warning.

    Your options are:
        YES    : Ignore once. This warning will appear again in the future.
        ALWAYS : Always ignore this warning.
        NO     : Follow the steps below to resolve this warning.
{ansi.NO_BOLD}{ansi.YELLOW}
    Steps to resolve this warning:
        - Create an X session on "{_get_container_host()}" by logging into the
          GUI on the physical machine.
        - Run "xhost +" in a terminal on the physical machine. This allows any
          host to access the running X server.
        - Lock the screen on the physical machine. Do not log out of the GUI
          session. Logging out of the GUI session will close the X session.
"""
        )

        ignore_warning = input("Ignore this warning? [YES/ALWAYS/NO]: ").strip().lower()
        if ignore_warning.startswith("a"):
            SKIP_INDICATOR_FILE.touch(exist_ok=True)
            return display_device
        elif ignore_warning.startswith("y"):
            return display_device
        else:
            raise RuntimeError("No X display device detected.")

    return display_device


def get_env(config: Config) -> "dict[str, str]":
    env = {
        "CONTAINER_HOST": _get_container_host(),
        "CONTAINER_RUNTIME": _get_container_runtime(),
        "CONTAINER_UID": _get_container_uid(),
        "CONTAINER_USER": _get_container_user(),
        "DOCKER_SCAN_SUGGEST": "false",
        "IMAGE_TAG": config.tag,
    }

    if config._require_x_display:
        env["DISPLAY"] = _get_x_display_device()
    else:
        env["DISPLAY"] = ""

    return env


if __name__ == "__main__":
    for k, v in get_env(Config(tag="")).items():
        print(f"{k}={v}")
