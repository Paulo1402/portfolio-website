# Portfolio App

This is a Django portfolio application that displays information about me and my projects.

The application is built with Python, Django templates, and Bootstrap for frontend styling.

## Technologies

- Python
- Django
- HTML
- CSS
- JavaScript
- Bootstrap
- PostgreSQL
- Nginx

## CI/CD

The repository uses GitHub Actions to:

- validate code with Ruff and `manage.py check`
- run the Django test suite
- build the Docker image and publish it to GHCR
- access the VPS over SSH and update the Docker Compose stack

## Docker Compose

The project uses separate Compose files per environment:

- `docker-compose.dev.yml`: local development stack with a locally built image, PostgreSQL, and Django's development server.
- `docker-compose.prod.yml`: versioned production template copied to the VPS as `docker-compose.yml`.

Start the local development stack with:

```bash
docker compose -f docker-compose.dev.yml up -d --build
```

The local `django` service runs migrations and starts `python manage.py runserver 0.0.0.0:8000`.
After startup, open `http://localhost:8000/`.

Production deploys do not copy the application source code to the VPS. The pipeline publishes the image to GHCR,
copies `docker-compose.prod.yml` to the VPS as `docker-compose.yml`, copies `scripts/deploy-app.sh` as `deploy-app.sh`,
and runs the remote script to update the stack.

## Repository Variables And Secrets

Repository variables, configured in GitHub Settings -> Variables:

- `VPS_HOST`: VPS IP address or domain.
- `VPS_USER`: deployment user, for example `deployer`.
- `VPS_APP_DIR`: application directory on the VPS, for example `/app`.

Secrets, configured in GitHub Settings -> Secrets:

- `VPS_SSH_KEY`: private SSH key for the deploy user.
- `VPS_KNOWN_HOSTS`: contents of the VPS `known_hosts` entry.

## VPS Setup

1. Create the deployment user and SSH key:

   ```bash
   sudo useradd -m -s /bin/bash -c "Portfolio app deployment" deployer
   sudo usermod -aG docker deployer
   sudo mkdir -p /app
   sudo chown deployer:deployer /app
   sudo -u deployer ssh-keygen -t ed25519 -f /home/deployer/.ssh/id_ed25519 -N ""
   ```

2. Create the shared Docker network:

   ```bash
   docker network create proxy_network
   ```

3. Create the shared volumes used by `nginx-proxy`:

   ```bash
   docker volume create portfolio_app_static_data
   docker volume create portfolio_app_media_data
   ```

4. Create `.env` on the VPS:

   ```bash
   # Create /app/.env with the required variables, using .env.example as reference.
   ```

5. Run an initial manual deploy, if needed:

   ```bash
   cd /app
   # The pipeline creates or updates docker-compose.yml, deploy-app.sh, and .env.cicd.
   # After those files exist on the VPS:
   ./deploy-app.sh
   ```

## Notes

- The deployment assumes Docker Compose is already installed and working on the VPS.
- For simplicity, publish the GHCR image as public. If the image is private, the VPS must authenticate with GHCR.
- The application service is expected to be named `django`; do not rename it in `docker-compose.prod.yml`.
- On the VPS, the versioned production Compose file is published as `docker-compose.yml`.
- The VPS Compose stack shares `portfolio_app_static_data` and `portfolio_app_media_data` with `nginx-proxy`.
- The deploy script runs `migrate`, `compilemessages`, and `collectstatic` inside the app container after `up -d`.
- `nginx-proxy` remains separate from this application stack to make maintenance and future migrations easier.
