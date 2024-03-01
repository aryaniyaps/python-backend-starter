ARG BASE_IMAGE=python:3.11.8-slim-bookworm

# build stage
FROM $BASE_IMAGE AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock /project/

# install dependencies and project into the local packages directory
WORKDIR /project
RUN mkdir __pypackages__ && pdm sync --prod --no-editable

# development stage
FROM $BASE_IMAGE AS development

# Set up development environment
WORKDIR /project

RUN pip install pdm

# copy files
COPY pyproject.toml pdm.lock ./

RUN pdm install

CMD ["pdm", "run", "server"]


# production stage
FROM $BASE_IMAGE as production

# retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs

COPY --from=builder /project/__pypackages__/3.11/lib /project/pkgs

# retrieve executables
COPY --from=builder /project/__pypackages__/3.11/bin/* /bin/

# set command/entrypoint, adapt to fit your needs
CMD ["python", "-m", "app/server.py"]
