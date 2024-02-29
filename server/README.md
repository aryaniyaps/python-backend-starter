# Python Backend Starter

## Features

- [x] User registration
   - [x] Authentication tokens are sha256 hashed
   - [x] Email notifications for onboarding
- [x] Email verification on user registration
- [x] 8 digit cryptographically secure email verification codes
- [ ] Email change flow (secured with passkeys)
- [x] Email verification codes are sha256 hashed
- [x] User login (passkeys)
   - [x] Login based on email
   - [x] Email notifications when new login device is detected
- [x] User session tracking
   - [x] IP address, device and geolocation data storage
- [x] The following metadata are attached with security notifications for enhanced user security:
   - Requester IP address
   - Requester device (based on the user agent)
   - Geolocation data (based on IP)
- [x] Structured logging support
- [x] Rate limiting (Moving window strategy)
   - [x] Primary rate limiting (API-wide)
   - [x] Secondary rate limiting (operation-specific)
- [ ] Error reporting with Sentry

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Uvicorn](https://www.uvicorn.org/)
- [Jinja2](https://jinja.palletsprojects.com/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [SAQ](https://saq-py.readthedocs.io/en/latest/)
- [Structlog](https://www.structlog.org/en/stable/)
- [Pytest](https://docs.pytest.org/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)

## Prerequisites

Make sure you have the following installed:

- [Python 3.11](https://www.python.org/downloads/)
- [Docker Engine](https://docs.docker.com/engine/install/)

## Project Setup

### Dependency management

To install dependencies, follow these steps:

1. Ensure that [PDM](https://pdm-project.org/latest/) is installed. You can install it via pip:

    ```
    pip install -U pdm
    ```
2. Install project dependencies with the following command:

   ```
   pdm install
   ```

### Environment variables

To set up environment variables for the project, follow these steps:

1. Create a `.env` file in the root directory.
2. Use the [`.env.example`](./.env.example) file provided in the root directory as a template for defining your environment variables.
3. Ensure that you fill in the required values for each environment variable according to your setup and configuration needs.

### Maxmind GeoLite2-City database

This project uses the Maxmind GeoLite2-City database (to extract geolocation data from IP addresses).

To setup the project for downloading and automatically updating the Maxmind GeoLite2-City database, follow these steps:

1. [Sign up for a Maxmind account](https://www.maxmind.com/en/geolite2/signup) if you haven't already done so.
2. Retrieve your Account ID and License Key from your Maxmind account dashboard.
3. Copy the following files into your project directory:

    ```
    /project_root
    ├── secrets
    │   ├── GEOIPUPDATE_ACCOUNT_ID.txt
    │   └── GEOIPUPDATE_LICENSE_KEY.txt
    └── ...
    ```



## Running the project

To run the project, follow these steps:

1. Start all services with the following command:

   ```
   docker compose up -d
   ```
2. To start the server, run the following command:

   ```
    pdm run server
   ```
3. To start the worker, open another terminal and run the following command:

   ```
   pdm run worker
   ```
