#!/bin/bash
sleep 10
uvicorn main:api --host 0.0.0.0 --port 80 --reload &> /app/logs/api/api_logs_$(date -I)_.txt
