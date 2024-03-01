ARG BASE_IMAGE=python:3.11.8-slim

# build stage
FROM $BASE_IMAGE AS builder

WORKDIR /app

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock ./

# install dependencies and project into the local packages directory
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

# development stage
FROM $BASE_IMAGE AS development

ENV PYTHONPATH=/app

ARG SERVER_DEBUG
ARG SERVER_ENVIRONMENT
ARG SERVER_HOST
ARG SERVER_PORT
ARG SERVER_LOG_LEVEL
ARG SERVER_CORS_ALLOW_ORIGINS
ARG SERVER_ROOT_PATH
ARG SERVER_OPENAPI_URL
ARG SERVER_RP_ID
ARG SERVER_RP_NAME
ARG SERVER_RP_EXPECTED_ORIGIN
ARG SERVER_DATABASE_URL
ARG SERVER_DATABASE_POOL_SIZE
ARG SERVER_REDIS_URL
ARG SERVER_SAQ_BROKER_URL
ARG SERVER_SAQ_CONCURRENCY
ARG SERVER_EMAIL_HOST
ARG SERVER_EMAIL_PORT
ARG SERVER_EMAIL_USERNAME
ARG SERVER_EMAIL_PASSWORD
ARG SERVER_EMAIL_FROM
ARG SERVER_GEOLITE2_DATABASE_PATH


# Set up development environment
WORKDIR /app

RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock ./

RUN pdm install

COPY . .

CMD ["pdm", "run", "server"]


# production stage
FROM $BASE_IMAGE as production

# retrieve packages from build stage
ENV PYTHONPATH=/app/pkgs

COPY --from=builder /app/__pypackages__/3.11/lib /app/pkgs

# retrieve executables
COPY --from=builder /app/__pypackages__/3.11/bin/* /bin/

# set command/entrypoint, adapt to fit your needs
CMD ["python", "-m", "app/server.py"]
