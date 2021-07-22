#!/bin/bash
cd /home/ubuntu/cyclegan
pipenv run uvicorn backend:app --host 0.0.0.0 --reload