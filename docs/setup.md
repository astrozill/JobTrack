# Local setup

Run commands from the project directory. Copy `.env.example` to `.env` if you
haven't already, and fill in your Django secret key and database credentials.

## Docker

Install Docker with Compose, then run:

```powershell
docker compose up --build
```

Open http://localhost:8000/ and register an account. Compose starts PostgreSQL,
waits for it to be ready, applies migrations, and starts Django's development
server. Keep `DATABASE_URL` unset to use the Compose database.

Your project folder is mounted at `/app`, so Python changes reload automatically.
Refresh the browser for template or static file changes. Rebuild after changing
dependencies or the Dockerfile.

After changing models, create and apply migrations:

```powershell
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

Useful commands:

```powershell
docker compose exec web python manage.py check
docker compose exec web python manage.py test
docker compose exec web python manage.py createsuperuser
docker compose logs -f web
docker compose down
```

The admin interface is at http://localhost:8000/admin/. PostgreSQL data is kept
in the `postgres_data` volume when containers are stopped or recreated.

## Python on Windows

Install Python 3.10 or newer and PostgreSQL. Create a database and user matching
the `DB_*` values in `.env`, or set `DATABASE_URL` to an existing database.
The database must be reachable from Windows; Compose's `db` hostname is only
available inside its Docker network.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/. Use the same Python executable for `check`, `test`,
`makemigrations`, and `createsuperuser`.

## Environment variables

The app loads `.env` from the project root. Existing environment variables take
precedence over the file.

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django's signing key. When unset locally, the app creates and reuses `.django-secret-key`. |
| `DJANGO_DEBUG` | Enables development debugging. `.env.example` uses `True`; the settings default is `False`. |
| `USE_HTTPS` | Enables HTTPS redirects and secure cookies. Use `False` for local HTTP. |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames, such as `localhost,127.0.0.1,[::1]`. |
| `DATABASE_URL` | Database connection URL; takes precedence over `DB_*` when nonempty. |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | PostgreSQL settings used when `DATABASE_URL` is unset or empty. |
| `LOG_LEVEL` | Console log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. Defaults to `INFO`. |

Example database URL:

```dotenv
DATABASE_URL=postgresql://jobtrack_user:your-database-password@127.0.0.1:5432/jobtrack_db
```

URL-encode special characters in credentials. Append `?sslmode=require` when
your database provider requires SSL.

Compose requires `DB_NAME`, `DB_USER`, and `DB_PASSWORD` to create its PostgreSQL
service. It sets Django's database host to `db` and port to `5432`.
Local secrets, Python environments, and database files are excluded from Git.

For hosted settings, see [deployment](deployment.md).
