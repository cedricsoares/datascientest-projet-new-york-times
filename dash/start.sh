#!/bin/bash
sleep 10
python main.py &> /app/logs/dash/dash_logs_$(date -I)_.txt
