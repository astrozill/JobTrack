# JobTrack

A Django web application for keeping track of job applications.

## Features

- User registration, login, and logout.
- Create, view, update, and delete your own job applications.
- Track companies, positions, locations, job links, statuses, dates, salary, and notes.
- Search by company or position and filter by application status.
- Dashboard with application counts and recent activity.

## Screenshots

These screenshots show the application with demo data.

### Dashboard

![Dashboard with application status totals and recent activity](docs/screenshots/dashboard.png)

### Application list

![Application list with search, status filtering, and pagination](docs/screenshots/application-list.png)

### Application detail

![Application detail showing the company, status, dates, salary, and notes](docs/screenshots/application-detail.png)

### Create application

![Form for creating a job application](docs/screenshots/create-application.png)

### Edit application

![Form for editing an existing job application](docs/screenshots/edit-application.png)

### Login

![JobTrack login page](docs/screenshots/login.png)

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

## Run with Docker

If `.env` does not exist, copy `.env.example` to `.env` and fill in your Django
secret key and database credentials. Start the application with:

```powershell
docker compose up --build
```

Open http://localhost:8000/. Compose starts PostgreSQL, waits for it to be ready,
and runs migrations before starting Django's development server.

The single `compose.yaml` shares your project folder at `/app` and enables
debug mode for local development, so Python edits
reload automatically and template/static asset edits are available on refresh.
WhiteNoise serves static assets from their source folders in this mode; a local
`staticfiles/` folder is not required. Rebuild after changing dependencies or the
Dockerfile. After adding migrations, apply them with:

```powershell
docker compose exec web python manage.py migrate
```

The Dockerfile runs migrations and collects static files at startup, then starts
Gunicorn with `jobtrack.wsgi:application`, bound to `0.0.0.0` on the `PORT`
environment variable (provided by Render), or port 8000 when it is unset.
Compose overrides that command with Django's `runserver` for local development.

## Configuration

Configure PostgreSQL with `DATABASE_URL` in the environment or `.env`, for example:

```dotenv
DATABASE_URL=postgresql://jobtrack_user:your-database-password@127.0.0.1:5432/jobtrack_db
```

A nonempty `DATABASE_URL` takes precedence over `DB_NAME`, `DB_USER`,
`DB_PASSWORD`, `DB_HOST`, and `DB_PORT`. When it is unset or empty, those five
variables are used as before. URL-encode special characters in credentials;
append `?sslmode=require` if your database provider requires SSL.

Local Docker Compose still requires the `DB_*` credentials to start its PostgreSQL
service. Leave `DATABASE_URL` unset to use that service; Compose sets the database
host to `db` and keeps its data in the `postgres_data` volume. The virtual
environment and local secrets are excluded from Git.

Set the `DJANGO_SECRET_KEY` environment variable to provide your own secret key.
When it is unset, the app creates and reuses a local `.django-secret-key` file.
Keep this file private.

Set `DJANGO_ALLOWED_HOSTS` to a comma-separated list of any additional hostnames.
For staging on Render, the app automatically adds `RENDER_EXTERNAL_HOSTNAME`
to `ALLOWED_HOSTS`. Render supplies this variable with the service's
`onrender.com` hostname, so you do not need to configure it manually.

Set `USE_HTTPS=False` for local HTTP development. Set `USE_HTTPS=True` after
configuring HTTPS for the deployment to redirect HTTP requests to HTTPS and
require secure session and CSRF cookies.
With HTTPS enabled, Django trusts the proxy's `X-Forwarded-Proto` header. The
deployment proxy must strip client-supplied values and set it to the original
request scheme.

Set `LOG_LEVEL` to `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL` to control
Django and application console logs. The default is `INFO`; Docker logs are
available with `docker compose logs -f web`.

The current settings enable debug mode for local development. Before production
deployment, configure a production secret, disable debug mode, set allowed hosts,
and follow Django's deployment checklist.

## Checks

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```
