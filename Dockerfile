# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.10-alpine

# Set the timezone to São Paulo
ENV TZ=America/Sao_Paulo

# Install tzdata for timezone configuration
RUN apk add --no-cache tzdata

# Set the timezone to São Paulo
RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
    && echo "America/Sao_Paulo" > /etc/timezone

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
ADD uv.lock pyproject.toml /app/
RUN uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Run the application
CMD ["gunicorn", "--config", "gunicorn.conf.py", "portfolio_website.wsgi:application"]