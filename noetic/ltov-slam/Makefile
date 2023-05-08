# MAKEFILE_PATH may not necessarily be this makefile
MAKEFILE_PATH := ${abspath ${lastword ${MAKEFILE_LIST}}}
NOETIC_DIR := ${realpath ${dir ${MAKEFILE_PATH}}/..}

.DEFAULT_GOAL := ltov-slam

.PHONY: ltov-slam
ltov-slam:
	cd ${NOETIC_DIR}/$@ && IMAGE_TAG=$@ docker compose build
