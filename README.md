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

## Project Setup

This project uses the Maxmind GeoLite2-City database (for getting the locations of IP addresses).

To setup the project for downloading and automatically updating the Maxmind GeoLite2-City database, follow these steps:

1. Sign up for a Maxmind account if you haven't already done so.
2. Retrieve your Account ID and License Key from your Maxmind account dashboard.
3. Copy the following files into your project directory:
```
/project_root
│
├── secrets
│   ├── GEOIPUPDATE_ACCOUNT_ID.txt
│   └── GEOIPUPDATE_LICENSE_KEY.txt
│
└── ...
```
