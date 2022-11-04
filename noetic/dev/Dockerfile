ARG CONTAINER_USER
FROM ${CONTAINER_USER}-noetic:see-spot-run

# Poetry python package manager
RUN pip3 install -U virtualenv
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/pypoetry python3 -
RUN ln -s /usr/local/pypoetry/bin/* /usr/local/bin/

RUN apt-get update && apt-get install -y \
    ffmpeg \
    mpv \
    xxhash
