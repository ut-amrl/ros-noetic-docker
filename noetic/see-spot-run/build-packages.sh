#! /usr/bin/env bash

set -o errexit
set -o nounset

# This script will proceed in two stages:
# 1. Clone all packages on the host
#   design decision: use ssh-agent if possible,
#   don't want to mount ssh-agent inside docker containers - potential security risk
# 2. Build all packages inside the docker container

function info {
    tput setaf 6
    echo "[INFO] $*"
    tput sgr0
}

function warn {
    tput setaf 3
    echo "[WARN] $*"
    tput sgr0
}

function success {
    tput setaf 2
    echo "[SUCCESS] $*"
    tput sgr0
}

function error {
    tput setaf 1
    echo "[ERROR] $*"
    tput sgr0
}

function build_failure {
    error "Build failed. Check build logs."
    error "Please include the full build log if you create a GitHub issue."
    error "https://github.com/ut-amrl/ros-noetic-docker/issues"
    exit 1
}


if [[ ! -e /dockerrc ]]; then
    # Log the Git SHA for build failure reproducibility.
    info "git hash: $(git rev-parse --verify HEAD)"

    # Test whether the user has ssh access to GitHub.
    info "Checking GitHub SSH authentication..."
    GITHUB_SSH_RESULT="$(ssh -T git@github.com 2>&1 || true)"
    if ! grep --silent "success" <<< "$GITHUB_SSH_RESULT"; then
        echo "$GITHUB_SSH_RESULT"
        error "Unable to authenticate with GitHub.
        Please follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
        Or forward an agent: https://docs.github.com/en/developers/overview/using-ssh-agent-forwarding"
        exit 1
    fi
    success "Authenticated with GitHub."
    warn "You may need to enter your SSH key password several times if you do not have an active ssh-agent.
        More info: https://docs.github.com/en/developers/overview/using-ssh-agent-forwarding"

    # Clone repositories.
    # Always run git submodule update when applicable, just in case the script exited while updating.
    if [[ ! -e $HOME/catkin_ws/src/spot_ros ]]; then
        info "Cloning https://github.com/ut-amrl/spot_ros"
        git clone git@github.com:ut-amrl/spot_ros $HOME/catkin_ws/src/spot_ros
    fi

    if [[ ! -e $HOME/catkin_ws/src/vectornav ]]; then
        info "Cloning https://github.com/dawonn/vectornav"
        git clone https://github.com/dawonn/vectornav $HOME/catkin_ws/src/vectornav
    fi

    if [[ ! -e $HOME/ut-amrl/amrl_msgs ]]; then
        info "Cloning https://github.com/ut-amrl/amrl_msgs"
        git clone git@github.com:ut-amrl/amrl_msgs $HOME/ut-amrl/amrl_msgs
    fi

    if [[ ! -e $HOME/ut-amrl/spot_autonomy ]]; then
        info "Cloning https://github.com/ut-amrl/spot_autonomy"
        git clone git@github.com:ut-amrl/spot_autonomy $HOME/ut-amrl/spot_autonomy
    fi

    info "Updating submodules for spot_autonomy"
    (cd $HOME/ut-amrl/spot_autonomy && git submodule update --init --recursive)

    if [[ ! -e $HOME/ut-amrl/graph_navigation && ! -L $HOME/ut-amrl/graph_navigation ]]; then
        info "Symlinking $HOME/ut-amrl/spot_autonomy/graph_navigation to $HOME/ut-amrl"
        ln -rs $HOME/ut-amrl/spot_autonomy/graph_navigation $HOME/ut-amrl
    fi

    if [[ ! -e $HOME/ut-amrl/k4a_ros ]]; then
        info "Cloning https://github.com/ut-amrl/k4a_ros"
        git clone git@github.com:ut-amrl/k4a_ros $HOME/ut-amrl/k4a_ros
    fi

    info "Updating submodules for k4a_ros"
    (cd $HOME/ut-amrl/k4a_ros && git submodule update --init --recursive)

    success "Cloned repositories"
    info "Moving execution into the Docker container to build packages..."

    # Start the docker container if it is not running already.
    yes | ./launch.py see-spot-run

    # Run this script in the Docker container to build packages.
    docker exec -t $USER-noetic-see-spot-run-app-1 "$(realpath $BASH_SOURCE)"

    if [[ ! -e $HOME/ut-amrl/spot_autonomy/launch/start_clearpath_spot.launch ]]; then
        warn "Manual setup is required in $HOME/ut-amrl/spot_autonomy:
        Replicate launch/start_clearpath_spot.launch.example to
        launch/start_clearpath_spot.launch, filling in your Spot
        robot username, password, and IP address."
    fi
else
    info "We're inside the Docker container now"

    # Initialize ROS env
    SHELL=bash source /dockerrc

    if [[ ! -e $HOME/.ros/rosdep ]]; then
        info "Running rosdep update"
        rosdep update
    fi

    # http://www.clearpathrobotics.com/assets/guides/melodic/spot-ros/ros_setup.html
    info "Running rosdep install for spot_ros"
    cd $HOME/catkin_ws &&
        rosdep install --from-paths src --ignore-src -y ||
        build_failure

    info "Building catkin packages"
    cd $HOME/catkin_ws &&
        catkin_make --cmake-args -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/python3 ||
        build_failure

    # Re-initialize ROS_PACKAGE_PATH
    SHELL=bash source /dockerrc

    info "Building amrl_msgs"
    cd $HOME/ut-amrl/amrl_msgs && make -j "$(nproc)" || build_failure

    info "Building spot_autonomy"
    cd $HOME/ut-amrl/spot_autonomy && make -j "$(nproc)" || build_failure

    info "Building k4a_ros"
    cd $HOME/ut-amrl/k4a_ros && make -j "$(nproc)" || build_failure

    success "Build finished"
fi
