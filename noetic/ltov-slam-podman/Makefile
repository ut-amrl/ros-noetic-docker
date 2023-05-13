# MAKEFILE_PATH may not necessarily be this makefile
MAKEFILE_PATH := ${abspath ${lastword ${MAKEFILE_LIST}}}
NOETIC_DIR := ${realpath ${dir ${MAKEFILE_PATH}}/..}

.DEFAULT_GOAL := ltov-slam-podman

.PHONY: ltov-slam-podman
ltov-slam:
	cd ${NOETIC_DIR}/$@ && IMAGE_TAG=$@ podman compose build
