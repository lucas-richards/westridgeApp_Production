#!/bin/bash

# Activate the virtual environment
source /home/bc/path/to/venv/bin/activate
#/Users/lucasrichards/desktop/projects/westridge_django/westridgeApp/run_collect_kpi.sh

# Navigate to the project directory
cd ~/westridgeApp

# Run the Django management command
python3 collect_kpi.py

# backup database
pg_dumpall > /home/bc/database_backup/backup.sql

# backup all files to backup server ECHO
date > ~/hotel_backup_trace.txt
rsync -a /home/bc am@10.1.1.20:/mnt/drobo/systembackup/training_backup_rs
