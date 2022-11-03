# MAKEFILE_PATH may not necessarily be this makefile
MAKEFILE_PATH := ${abspath ${lastword ${MAKEFILE_LIST}}}
NOETIC_DIR := ${realpath ${dir ${MAKEFILE_PATH}}/..}

.DEFAULT_GOAL := amrl-base

.PHONY: amrl-base
amrl-base:
	cd ${NOETIC_DIR}/$@ && docker compose build
