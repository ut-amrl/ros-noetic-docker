ARG CONTAINER_USER
FROM ${CONTAINER_USER}-noetic:amrl-base

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
## https://github.com/ut-amrl/spot_ros/blob/main/spot_driver/package.xml
RUN apt-get update && apt-get install -y \
    ros-noetic-twist-mux \
    ros-noetic-interactive-marker-twist-server \
    ros-noetic-velodyne-pointcloud
## 2022-06-07: protobuf v4.x breaks pipeline, freeze to v3.20.1
RUN pip3 install protobuf==3.20.1
RUN pip3 install cython empy \
    bosdyn-client==3.1.1 bosdyn-mission==3.1.1 bosdyn-api==3.1.1 bosdyn-core==3.1.1
RUN pip3 install gTTs pydub

## For object detection 3d PCDet package
RUN pip install torch==1.10.0 --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip install cumm-cu113 spconv-cu113 wandb
RUN pip install llvmlite numba
RUN pip install tensorboardX==2.5.1
RUN pip install easydict pyyaml
RUN pip install tqdm
RUN pip install scikit-image==0.18.0
RUN pip install SharedArray==3.1.0
RUN pip install open3d mayavi
RUN pip install numpy==1.21
RUN pip install more-itertools
RUN pip install rospkg
RUN pip install pycryptodomex
RUN pip install gnupg
RUN pip install setuptools==68.0.0
RUN pip install --upgrade Pillow
RUN pip install rosnumpy
RUN chmod 777 /usr/local/lib/python3.8/dist-packages/
RUN mkdir -p /usr/lib/python3.8/site-packages
RUN chmod 777 /usr/lib/python3.8/site-packages
RUN chmod 777 /usr/bin

# Packages to enable audio playback and forwarding
RUN apt-get update && apt-get install -y \
    alsa-base \
    alsa-utils \
    pulseaudio

# Additional utilities
RUN apt-get update && apt-get install -y \
    joystick \
    ffmpeg \
    espeak \
    mpg123
