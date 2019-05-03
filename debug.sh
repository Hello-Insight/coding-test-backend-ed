#!/bin/bash
# debug flask server

source ./venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=src/app.py
flask run
