FROM osrf/ros:noetic-desktop-full-focal

ENV DEBIAN_FRONTEND noninteractive
ENV DIRPATH /root
WORKDIR $DIRPATH

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago

#Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update && apt-get install -y git cmake

# Development tools
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    wget \
    software-properties-common \
    git cmake pkg-config build-essential \
    g++ gdb git vim valgrind nano clang-format 

# Install Eigen
RUN apt-get install -y libeigen3-dev

# Install xvfb to provide a display to container for GUI related testing.
RUN apt-get update && apt-get install -y xvfb

#install google flags/logs/tests
RUN apt-get update && apt-get install -y \
    libgtest-dev libgoogle-glog-dev libgflags-dev liblua5.1-0-dev

# Install OpenCV for Ubuntu 18.04
RUN apt-get update && apt-get install -y \
      build-essential cmake unzip pkg-config \
      libjpeg-dev libpng-dev libtiff-dev \
      libvtk6-dev \
      libgtk-3-dev \
      libatlas-base-dev gfortran
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

# Pangolin
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

# Additional libraries for ut_vslam

# Intel MKL for ut_vslam (Optional)
# RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | sudo tee /usr/share/keyrings/oneapi-archive-keyring.gpg > /dev/null \
#     && echo "deb [signed-by=/usr/share/keyrings/oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main" | sudo tee /etc/apt/sources.list.d/oneAPI.list \
#     && apt update && apt install -y intel-oneapi-mkl && echo "hello"

# Compile Ceres with Intel MKL for ut_vslam
# RUN . /opt/intel/oneapi/setvars.sh \
#     && cd ~ && git clone https://github.com/ceres-solver/ceres-solver.git \
#     && cd ~/ceres-solver && git checkout 1.14.x && mkdir build && cd build \
#     && cmake .. && make -j8 && sudo make install

# Ceres
RUN cd ~ && git clone https://github.com/ceres-solver/ceres-solver.git \
    && cd ~/ceres-solver && git checkout 1.14.x && mkdir build && cd build \
    && cmake .. && make -j8 && sudo make install

RUN sudo apt-get install -y \
    ros-noetic-pcl-ros \
    libsuitesparse-dev

# ensure rosbuild is in place
RUN apt update && apt install -y \
    python-is-python3 \
    python3-catkin-tools \
    python3-pip \
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

CMD sleep infinity