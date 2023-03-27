# MAKEFILE_PATH may not necessarily be this makefile
MAKEFILE_PATH := ${abspath ${lastword ${MAKEFILE_LIST}}}
NOETIC_DIR := ${realpath ${dir ${MAKEFILE_PATH}}/..}

include ${NOETIC_DIR}/amrl-base/Makefile

.DEFAULT_GOAL := see-spot-run

.PHONY: see-spot-run
see-spot-run: amrl-base
	cd ${NOETIC_DIR}/$@ && IMAGE_TAG=$@ docker compose build
