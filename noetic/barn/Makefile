# MAKEFILE_PATH may not necessarily be this makefile
MAKEFILE_PATH := ${abspath ${lastword ${MAKEFILE_LIST}}}
NOETIC_DIR := ${realpath ${dir ${MAKEFILE_PATH}}/..}

include ${NOETIC_DIR}/amrl-base/Makefile

.DEFAULT_GOAL := barn

.PHONY: barn
barn:
	cd ${NOETIC_DIR}/$@ && docker compose build
