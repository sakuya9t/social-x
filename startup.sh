#!/bin/bash
nohup pipenv run python3 service/app.py > backend.log &
cd web-app
nohup npm run start > frontend.log &
