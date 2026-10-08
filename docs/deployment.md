# Deployment on Render

[Production site](https://jobtrack-hx94.onrender.com)

The app runs as a Docker web service backed by PostgreSQL. The image uses
Gunicorn and WhiteNoise to serve the application and collected static files.

## Service configuration

Use Docker as the runtime, with `./Dockerfile` and the repository root as the
build context. Leave the Docker Command override empty to use the image's CMD.
Select the branch containing the release and set the Health Check Path to
`/ready/`. See [Render's Docker guide](https://render.com/docs/docker).

Set these variables in the production service:

| Variable | Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | A strong, stable secret kept across deployments. |
| `DJANGO_DEBUG` | `False` |
| `USE_HTTPS` | `True` |
| `DATABASE_URL` | The production PostgreSQL connection URL. |
| `LOG_LEVEL` | `INFO`, or another level when troubleshooting. |
| `DJANGO_ALLOWED_HOSTS` | Any additional custom hostnames, separated by commas. |

The `.env.example` values are for local development. Provide deployed secrets
through Render's environment settings.

Render supplies `RENDER_EXTERNAL_HOSTNAME` and `PORT`. Django adds the hostname
to `ALLOWED_HOSTS`, and Gunicorn binds to `0.0.0.0` on that port. The local port
fallback is `8000`.

## Startup

The Dockerfile's CMD runs these steps in order:

1. Apply database migrations with `migrate --noinput`.
2. Collect and process static assets with `collectstatic --noinput`.
3. Start Gunicorn with `jobtrack.wsgi:application` and two workers.

Gunicorn starts only after both Django commands succeed. It runs as the container's
main process so it receives shutdown signals. Docker Compose overrides this CMD
with Django's development server for local use.

## HTTPS and health checks

With `USE_HTTPS=True`, Django redirects application pages to HTTPS and enables
secure session and CSRF cookies. It trusts the proxy's `X-Forwarded-Proto` header;
the proxy must strip client-supplied values and set the original request scheme.

| Endpoint | Check | Response |
| --- | --- | --- |
| `/health/` | The app can handle a request. | HTTP 200 with `OK`. |
| `/ready/` | The database responds to `SELECT 1`. | HTTP 200 with `OK`, or HTTP 503 with `Not ready`. |

Neither endpoint requires a login. Both are exempt from HTTPS redirects so HTTP
probes reach their checks directly. Readiness responses are not cached.
See [Render health checks](https://render.com/docs/health-checks).

Before a release, run `python manage.py check --deploy` with the production
settings and review any warnings. Use the [deployment checklist](production-release-checklist.md)
to verify the deployed site.
