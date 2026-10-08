# JobTrack

A Django app for keeping track of job applications, from saved roles to offers
or rejections. Each user has their own applications, notes, and job links.

[Try the live demo](https://jobtrack-hx94.onrender.com)

## Features

- Add and update applications with company, role, location, dates, and salary.
- Track application status and see a summary on the dashboard.
- Search by company or position and filter by status.
- Register an account and manage your own applications.

## Built with

Django, PostgreSQL, and Django templates. Docker handles the local environment;
Gunicorn and WhiteNoise serve the app on Render. Application queries are scoped
to the signed-in user.

## Screenshots

The screenshots use demo data.

![Dashboard](docs/screenshots/dashboard.png)

![Application list](docs/screenshots/application-list.png)

## Run locally

With Docker installed, copy `.env.example` to `.env` if needed. Set the Django
secret key and database credentials, and leave `DATABASE_URL` unset to use the
local Compose database. Then run:

```powershell
docker compose up --build
```

Open http://localhost:8000/ and register an account.

See [local setup](docs/setup.md) for the Windows Python option, environment
variables, and development commands.

## Checks

With the local Compose services running:

```powershell
docker compose exec web python manage.py check
docker compose exec web python manage.py test
```

[Render deployment](docs/deployment.md) | [Deployment checklist](docs/production-release-checklist.md)
