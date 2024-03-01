# Stage 1: Base
FROM python:3.11.8-alpine AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#     build-essential \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install pdm

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to optimize caching
COPY pyproject.toml pdm.lock ./

# Stage 2: Development
FROM base AS development

# Install project dependencies
RUN pdm install

# Copy the rest of the application code
COPY . .

# Expose port for development (if applicable)
EXPOSE 8000

# Set up entry point
ENTRYPOINT ["pdm", "run", "server"]

# Stage 3: Production
FROM base AS production

# Install project dependencies for production
RUN pdm install --no-dev

# Copy the rest of the application code
COPY . .

# Expose port for production (if applicable)
EXPOSE 8000

# Set up entry point
ENTRYPOINT ["pdm", "run", "server"]
