import enum
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import NoReturn, Union

import internal.ansi as ansi
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

    subprocess_args = ["ssh", "-T", "git@github.com"]

    logger.info(
        f"Running `{' '.join(subprocess_args)}`. You may be prompted for a password."
    )
    result = subprocess.run(
        subprocess_args,
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
        f"""How would you like to clone repositories from GitHub?

    Your options are:
{ansi.BOLD}
    (1) SSH   : pull and push access to public and private repositories
    (2) HTTPS : pull access to public repositories only
{ansi.NO_BOLD}
    This choice will not affect how git submodules are cloned. Submodules
    specified as SSH addresses will be cloned using SSH.
"""
    )

    user_input = input("[SSH or HTTPS] ? ").strip().lower()

    if user_input in ["1", "ssh"]:
        protocol = GitHubProtocol.SSH
    elif user_input in ["2", "https"]:
        protocol = GitHubProtocol.HTTPS
    else:
        logger.warning(f"Unrecognized input '{user_input}'. Falling back to HTTPS.")
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

    try:
        subprocess.run(subprocess_args, check=True)
    except subprocess.CalledProcessError:
        logger.error(f"Unable to clone {url} to {dest}")


def update_submodules(repo_dir: Path) -> None:
    # Do not parallelize with --jobs since the user may need to enter an ssh key password
    # TODO: if the user has an ssh-agent, then go ahead and parallelize
    subprocess_args = [
        "git",
        "submodule",
        "update",
        "--init",
        "--recursive",
        "--progress",
    ]

    try:
        subprocess.run(subprocess_args, cwd=repo_dir, check=True)
    except subprocess.CalledProcessError:
        logger.error(f"Unable to update submodules for {repo_dir}")


def get_repository_hash(repo_dir_or_file: Union[str, Path]) -> str:
    repo_dir_or_file = Path(repo_dir_or_file)
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


def get_repository_root(repo_dir_or_file: Union[str, Path]) -> str:
    repo_dir_or_file = Path(repo_dir_or_file)
    if os.path.isfile(repo_dir_or_file):
        repo_dir_or_file = repo_dir_or_file.parent

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        cwd=repo_dir_or_file,
    )

    return result.stdout.strip()
