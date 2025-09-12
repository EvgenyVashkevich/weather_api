# base image
FROM python:3.13-slim AS builder-image

# add service user
ARG PROJECT_USER
RUN adduser --disabled-password ${PROJECT_USER}
WORKDIR /home/${PROJECT_USER}
USER ${PROJECT_USER}

# create project dir
ARG PROJECT_SLUG
WORKDIR /home/${PROJECT_USER}/${PROJECT_SLUG}

# install requirements
ARG VIRTUAL_ENV
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m pip install --upgrade --no-cache-dir pip setuptools wheel
COPY requirements/prod.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# main image
FROM python:3.13-slim AS main-image

# add service user
ARG PROJECT_USER
RUN adduser --disabled-password ${PROJECT_USER}
WORKDIR /home/${PROJECT_USER}
USER ${PROJECT_USER}

# create project dir
ARG PROJECT_SLUG
WORKDIR /home/${PROJECT_USER}/${PROJECT_SLUG}
RUN mkdir logs

# copy `venv` from builder-image to main-image
ARG VIRTUAL_ENV
COPY --from=builder-image ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# activate virtual env
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# copy project files
COPY --chown=${PROJECT_USER} LICENSE *.py *.in ./
COPY --chown=${PROJECT_USER} weather_api weather_api
