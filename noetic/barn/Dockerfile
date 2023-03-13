ARG CONTAINER_USER
FROM ${CONTAINER_USER}-noetic:amrl-base

# https://github.com/ut-amrl/BARNChallenge2023
RUN apt-get update && apt-get install -y \
    ros-noetic-jackal-gazebo
RUN apt-get update && apt-get install -y \
    ros-noetic-move-base
