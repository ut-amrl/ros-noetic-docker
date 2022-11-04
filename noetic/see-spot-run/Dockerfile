ARG CONTAINER_USER
FROM ${CONTAINER_USER}-noetic:amrl-base

# https://github.com/ut-amrl/robofleet_client
RUN apt-get update && apt-get install -y \
    cmake qt5-default libqt5websockets5-dev

# https://github.com/ut-amrl/k4a_ros
RUN apt-get update && apt-get install -y \
    liblua5.1-0-dev libgflags-dev libgoogle-glog-dev libgoogle-perftools-dev cimg-dev
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
RUN apt-add-repository "deb https://packages.microsoft.com/ubuntu/18.04/prod bionic main"
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    k4a-tools \
    libk4a1.4 \
    libk4a1.4-dev
COPY ../99-k4a.rules /etc/udev/rules.d/

# https://github.com/ut-amrl/spot_autonomy
RUN apt-get update && apt-get install -y \
    qt5-default libqt5websockets5-dev libgoogle-glog-dev libgflags-dev

# https://github.com/ut-amrl/spot_ros
RUN apt-get update && apt-get install -y \
    ros-noetic-velodyne-pointcloud
# 2022-06-07: protobuf v4.x breaks pipeline, freeze to v3.20.1
RUN pip3 install protobuf==3.20.1
RUN pip3 install cython empy \
    bosdyn-client==3.1.1 bosdyn-mission==3.1.1 bosdyn-api==3.1.1 bosdyn-core==3.1.1

# Packages to enable audio playback and forwarding
RUN apt-get update && apt-get install -y \
    alsa-base \
    alsa-utils \
    pulseaudio

# Additional utilities
RUN apt-get update && apt-get install -y \
    joystick
