#!/bin/bash
sleep 10
python3 /app/app.py --news True --books True --movies True &> /app/logs/etl/etl_logs_$(date -I)_.txt
