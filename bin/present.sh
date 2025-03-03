#!/bin/bash

cd docs 
python3 -m http.server 8000 & SERVER_PID=$!
trap "kill $SERVER_PID" SIGINT
firefox --kiosk http://localhost:8000
