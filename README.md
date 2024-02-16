# Python Backend Starter

## Features

- [x] User registration
   - [x] Authentication tokens are sha256 hashed
   - [x] Passwords are securely hashed with Argon2
   - [x] Email notifications for onboarding
- [x] Password strength validation using the [ZXCVBN](https://github.com/dropbox/zxcvbn) algorithm
- [x] Email verification on user registration
- [x] Verified email change requests
- [x] Email verification tokens are sha256 hashed
- [ ] Secure password changes
- [x] User login
   - [x] Login based on either email or username
   - [x] Passwords are rehashed upon login
- [x] Password resets
   - [x] Password reset tokens are sha256 hashed
   - [x] Email notifications for password reset requests
   - [x] Email notifications when password changes
- [ ] User session tracking
   - [x] IP address, User agent and geolocation data storage
   - [ ] Email notifications when new login location is detected
- [x] The following metadata are attached with security notifications for enhanced user security:
   - Requester IP address
   - Requester device (based on the user agent)
   - Geolocation data (based on IP)
- [ ] Sign in with Google
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

### Oauth2 app configuration (Google)

To obtain the Google Client ID and Client Secret, follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. [Create a new project](https://console.cloud.google.com/projectcreate) or select an existing one.
3. Navigate to the *Credentials* tab.
4. Click on *Create credentials* and select *OAuth client ID*.
5. Choose *Web application* as the application type.
6. Enter the appropriate information for your application.
   The authorized redirect URIs used when creating the credentials must include the following URL *(assuming you are running at port 8000 on localhost)*:

   **http://localhost:8000/api/oauth/google/callback**

7. Once created, copy the generated Client ID and Client Secret.
8. Paste the Client ID and Client secret into the `.env` file as follows:

    ```
    SERVER_GOOGLE_CLIENT_ID=<Client ID>
    SERVER_GOOGLE_CLIENT_SECRET=<Client Secret>
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
