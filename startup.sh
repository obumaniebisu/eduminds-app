#!/bin/bash
cd backend
gunicorn -c gunicorn.conf.py app.main:app
