#!/usr/bin/env bash
set -euo pipefail

# Config
BACKUP_DIR="/opt/backups/portfolio-website/postgres"
DATE=$(date +%F_%H-%M-%S)
ENV_FILE="/app/portfolio-website/.env"
RETENTION_DAYS=30

mkdir -p "$BACKUP_DIR"

# Load variables
set -a
source "$ENV_FILE"
set +a

# Backup
docker exec postgres_portfolio_app \
  pg_dump -U "$POSTGRES_USER" "$POSTGRES_DB" \
  | gzip > "$BACKUP_DIR/postgres_$DATE.sql.gz"

# Delete backups older than retention period
find "$BACKUP_DIR" \
  -type f \
  -name "postgres_*.sql.gz" \
  -mtime +"$RETENTION_DAYS" \
  -delete
