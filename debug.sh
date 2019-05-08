#!/bin/bash
# debug flask server

source ./venv/bin/activate
export FLASK_ENV=development
flask run
