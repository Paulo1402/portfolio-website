# Repository Guidelines

## Project Structure & Module Organization

This is a Django 5 portfolio application. The Django project configuration lives in `portfolio_website/`, with settings, root URLs, ASGI, and WSGI modules. Main application code is in `app/`: models are split under `app/models/`, admin registrations under `app/admin/`, forms under `app/forms/`, utilities under `app/utils/`, and page templates under `app/templates/pages/`. Shared base/error templates are in `templates/global/`. Static CSS, JavaScript, and icons are in `static/global/`. Tests live in `app/tests/`. Deployment files include `Dockerfile`, `docker-compose.dev.yml`, `docker-compose.prod.yml`, `gunicorn.conf.py`, and `scripts/deploy-app.sh`.

## Build, Test, and Development Commands

- `uv sync --frozen`: install the exact locked dependencies from `uv.lock`.
- `uv run python manage.py runserver`: start the local Django development server.
- `uv run python manage.py check`: run Django configuration checks.
- `uv run python manage.py test`: run the Django test suite.
- `uv run ruff check .`: lint Python code with Ruff.
- `uv run python manage.py makemigrations` / `migrate`: create and apply database migrations.
- `docker compose -f docker-compose.dev.yml up -d --build`: run the local development stack with PostgreSQL.

## Coding Style & Naming Conventions

Use Python 3.10+ and follow Django conventions. Keep indentation at 4 spaces, prefer clear snake_case names for functions, variables, modules, and migration files, and use PascalCase for classes and Django models. Keep model/admin/form concerns in their existing package areas instead of growing `views.py` or a single large module. Run Ruff before opening a PR; no separate formatter configuration is currently defined.

## Testing Guidelines

Tests use Django's built-in test runner and `django.test.TestCase`. Add tests under `app/tests/`, naming files `test_<feature>.py` and test methods `test_<expected_behavior>`. Cover model behavior, views, health checks, and regressions for bug fixes. Run `uv run python manage.py test` locally before pushing.

## Commit & Pull Request Guidelines

Recent history uses Conventional Commit-style messages such as `feat(health): add db-backed health route` and `fix(compose): use container env for postgres healthcheck`. Keep commit subjects imperative, scoped, and concise. Pull requests should include a short description, the reason for the change, test results, linked issues when applicable, and screenshots for visible template or styling changes.

## Security & Configuration Tips

Copy `.env.example` to `.env` for local development and keep secrets out of git. Management commands require settings such as `DJANGO_SECRET_KEY`, `DJANGO_ENV`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and `GITHUB_TOKEN`. Host-side commands use SQLite by default outside production; the Docker development service sets `USE_POSTGRES=true` so the compose stack uses PostgreSQL.
