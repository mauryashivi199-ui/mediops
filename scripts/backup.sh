#!/bin/bash
# MediOps - Auto backup to AWS S3
# Runs every 30 minutes via cron

DATE=$(date +"%Y-%m-%d_%H-%M")
BACKUP_FILE="/tmp/mediops_backup_$DATE.dump"

echo "[$(date)] Starting backup..."

# Dump PostgreSQL DB
pg_dump -h localhost -U admin mediops > $BACKUP_FILE

# Upload to S3
aws s3 cp $BACKUP_FILE s3://mediops-backups/backups/$DATE.dump
aws s3 cp $BACKUP_FILE s3://mediops-backups/latest.dump  # Always keep latest

echo "[$(date)] Backup uploaded to S3 ✅"

# Cleanup local file
rm $BACKUP_FILE
