#!/bin/bash
nohup pipenv run python3 service/app.py > ./log/backend.log &
cd web-app
nohup npm run start > ../log/frontend.log &
