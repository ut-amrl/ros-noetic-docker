# MAKEFILE_PATH may not necessarily be this makefile
MAKEFILE_PATH := ${abspath ${lastword ${MAKEFILE_LIST}}}
NOETIC_DIR := ${realpath ${dir ${MAKEFILE_PATH}}/..}

include ${NOETIC_DIR}/see-spot-run/Makefile

.DEFAULT_GOAL := dev

.PHONY: dev
dev: see-spot-run
	cd ${NOETIC_DIR}/$@ && IMAGE_TAG=dev docker compose build
