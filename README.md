# Python Backend Starter

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Uvicorn](https://www.uvicorn.org/)
- [Jinja2](https://jinja.palletsprojects.com/en/latest/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
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

1. Ensure that pdm is installed. You can install it via pip:

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
3. To start the worker, run the following command:

   ```
   pdm run worker
   ```
