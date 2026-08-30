#!/usr/bin/env bash
# Copyright 2026 Kevin Fisher. All rights reserved.
# SPDX-License-Identifier: AGPL-3.0-only

# Dumps the housecarl Postgres database from the running `db` compose service
# and rotates old dumps. Intended to be run via cron.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${1:-${BACKUP_DIR:-$REPO_DIR/backups}}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_FILE="$BACKUP_DIR/housecarl-$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"

cd "$REPO_DIR"
docker compose exec -T db pg_dump -U housecarl -Fp housecarl > "$OUT_FILE"

find "$BACKUP_DIR" -name 'housecarl-*.sql' -mtime "+$RETENTION_DAYS" -delete

echo "Backed up to $OUT_FILE"

