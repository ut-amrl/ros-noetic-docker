FROM osrf/ros:noetic-desktop-full-focal

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago

# Package installation tools
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    python-is-python3 \
    python3-catkin-tools \
    python3-pip \
    software-properties-common

# https://github.com/ut-amrl/amrl_shared_lib
RUN apt-get update && apt-get install -y \
    libgtest-dev libgoogle-glog-dev cmake build-essential

# https://github.com/ut-amrl/graph_navigation
RUN apt-get update && apt-get install -y \
    libgoogle-glog-dev libgflags-dev liblua5.1-0-dev

# https://github.com/ut-amrl/enml
RUN apt-get update && apt-get install -y \
    liblua5.1-dev libeigen3-dev \
    libjpeg8-dev libgoogle-perftools-dev \
    libsuitesparse-dev libblas-dev liblapack-dev libopenmpi-dev \
    libgoogle-glog-dev libgflags-dev libceres-dev libtbb-dev \
    libncurses5-dev libpopt-dev

# Development tools
RUN apt-get update && apt-get install -y \
    build-essential \
    clang-12 \
    clang-format \
    cmake \
    g++ \
    gdb \
    git \
    nano \
    valgrind \
    vim

# Additional utilities to make things easier inside the container.
RUN apt-get update && apt-get install -y \
    iputils-ping \
    less \
    mesa-utils \
    net-tools \
    rsync \
    tmux \
    tree \
    unzip \
    usbutils \
    zip \
    zsh \
    wget

# Opencv 
RUN sudo apt update && sudo apt install -y cmake g++ wget unzip \
    && cd ~ && git clone https://github.com/Itseez/opencv.git && \ 
    cd ~ && git clone https://github.com/Itseez/opencv_contrib.git && \
    cd ~/opencv && mkdir -p build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D INSTALL_C_EXAMPLES=ON \ 
    -D INSTALL_PYTHON_EXAMPLES=ON \ 
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \ 
    -D BUILD_EXAMPLES=OFF .. && \
    make -j8 && \
    make install && \ 
    ldconfig

# ensure rosbuild is in place
RUN sudo apt update && sudo apt install -y \
    python3-rosdep \
    python3-rosinstall \
    python3-rosinstall-generator \
    python3-wstool \
    build-essential

# For yolo-ros
RUN pip install numpy>=1.18.5 \
    && pip install opencv-python>=4.1.1 \
    && pip install Pillow>=7.1.2 \
    && pip install PyYAML>=5.3.1 \
    && pip install requests>=2.23.0 \
    && pip install scipy>=1.4.1  \
    && pip install torch>=1.7.0 \
    && pip install torchvision>=0.8.1 \
    && pip install tqdm>=4.41.0 \
    && pip install protobuf \
    && pip install tensorboard>=2.4.1 \
    && pip install pandas>=1.1.4 \
    && pip install seaborn>=0.11.0 \
    && pip install ipython  \
    && pip install psutil \
    && pip install thop \
    && sudo apt update && sudo apt-get install -y python3-tk

# Pangolin for ORB_SLAM2
RUN sudo apt update && sudo apt install -y \
    libgl1-mesa-dev libwayland-dev libxkbcommon-dev wayland-protocols libegl1-mesa-dev \
    libc++-dev libglew-dev libeigen3-dev cmake g++ ninja-build \
    libjpeg-dev libpng-dev \
    libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev \
    && cd ~ && git clone --recursive https://github.com/stevenlovegrove/Pangolin.git \
    && cd ~/Pangolin && git checkout v0.6 \
    && cmake -B build && cmake --build build \
    && cd ~/Pangolin/build && make install

# dlib for OA-SLAM
RUN cd ~ && git clone https://github.com/davisking/dlib.git \
    && cd ~/dlib && mkdir build && cd build && cmake .. && cmake --build . && make install

RUN echo "[[ -e /.dockerenv ]] && source /.dockerenv" >> /root/.bashrc

# TODO: "roscore" is shared between containers with the current network
# configuration. The container will fail to start if an instance of roscore is
# already running, whether on the host or within a different container. Users
# will need to manually check and launch roscore within the Docker environment
# until proper container network isolation is implemented. In the meantime, the
# sleep command keeps the container running.
CMD sleep infinity
# CMD roscore