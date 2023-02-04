import enum
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import NoReturn, Union

from internal import logger


class GitHubProtocol(enum.Enum):
    HTTPS = "https"
    SSH = "ssh"


def check_github_ssh_auth() -> Union[bool, NoReturn]:
    logger.info("Checking GitHub SSH authentication...")

    # Try to detect if the user has to enter a password for their ssh key using
    # the duration of the ssh command as a heuristic. Assume the user had to
    # enter a password if the duration is large enough (not resilient against
    # high latency to GitHub, short passwords, or fast typers).
    t_start = time.time()

    result = subprocess.run(
        ["ssh", "-T", "git@github.com"],
        capture_output=True,
        text=True,
    )

    t_end = time.time()
    password_likely = t_end - t_start > 1.5

    if "success" in result.stderr:
        logger.success("Authenticated with GitHub.")
        if password_likely:
            logger.warning(
                """You may be prompted to enter your SSH key password several times.
        Recommended: https://docs.github.com/en/developers/overview/using-ssh-agent-forwarding"""
            )
        return True
    else:
        print(result.stderr, end="")
        logger.critical(
            """Unable to authenticate with GitHub with SSH.
        Please follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
        Or forward an agent: https://docs.github.com/en/developers/overview/using-ssh-agent-forwarding"""
        )
        sys.exit(1)


def get_user_protocol_preference() -> GitHubProtocol:
    # If the user has a Personal Access Token set up then they'll have
    # [public+private] and [pull+push] via HTTPS as well, but this is too much
    # information to put in a simple prompt. If the user has a PAT set up,
    # they'll probably know this information anyway.
    print(
        """How would you like to clone repositories from GitHub?

    (1) SSH             [public + private]      [pull + push]
    (2) HTTPS           [public only]           [pull only]
"""
    )

    user_input = input("[1 or 2]: ")

    if user_input == "1":
        protocol = GitHubProtocol.SSH
    elif user_input == "2":
        protocol = GitHubProtocol.HTTPS
    else:
        logger.info(f"Unrecognized input '{user_input}'. Falling back to HTTPS.")
        protocol = GitHubProtocol.HTTPS

    if protocol == GitHubProtocol.SSH:
        check_github_ssh_auth()

    return protocol


def convert_url_protocol(
    url: str, protocol: GitHubProtocol = GitHubProtocol.HTTPS
) -> str:
    path = url[url.index("github.com") + len("github.com") + 1 :]

    if protocol == GitHubProtocol.HTTPS:
        return "https://github.com/" + path
    elif protocol == GitHubProtocol.SSH:
        return "git@github.com:" + path
    else:
        logger.warning("Unhandled GitHub protocol")
        return url


def clone_repository(url: str, dest: Path, protocol: GitHubProtocol) -> None:
    url = convert_url_protocol(url, protocol)

    subprocess_args = [
        "git",
        "clone",
        url,
        str(dest.absolute()),
    ]

    subprocess.run(subprocess_args)


def update_submodules(repo_dir: Path) -> None:
    subprocess_args = [
        "git",
        "submodule",
        "update",
        "--init",
        "--recursive",
        "--jobs",
        "8",
    ]

    subprocess.run(subprocess_args, cwd=repo_dir)


def get_repository_hash(repo_dir_or_file: Path) -> str:
    if os.path.isfile(repo_dir_or_file):
        repo_dir_or_file = repo_dir_or_file.parent

    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        capture_output=True,
        text=True,
        cwd=repo_dir_or_file,
    )

    git_hash = result.stdout.strip()

    result = subprocess.run(
        ["git", "diff", "--quiet", "HEAD"],
        text=True,
        cwd=repo_dir_or_file,
    )
    if result.returncode == 1:
        git_hash += "-dirty"

    return git_hash
