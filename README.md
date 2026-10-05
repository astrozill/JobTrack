# JobTrack

A Django web application for keeping track of job applications.

## Features

- User registration, login, and logout.
- Create, view, update, and delete your own job applications.
- Track companies, positions, locations, job links, statuses, dates, salary, and notes.
- Search by company or position and filter by application status.
- Dashboard with application counts and recent activity.

## Run locally on Windows

Install Python 3.10 or newer, then run these commands in PowerShell from the project directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ and register an account to start tracking applications.

To create an optional admin account:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

The admin interface is available at http://127.0.0.1:8000/admin/.

## Configuration

The application uses SQLite for local development. The database, virtual environment,
and local secrets are excluded from Git.

Set the `DJANGO_SECRET_KEY` environment variable to provide your own secret key.
When it is unset, the app creates and reuses a local `.django-secret-key` file.
Keep this file private.

The current settings enable debug mode for local development. Before production
deployment, configure a production secret, disable debug mode, set allowed hosts,
and follow Django's deployment checklist.

## Checks

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```
