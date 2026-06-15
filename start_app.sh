#!/bin/bash

nohup python3 /home/ubuntu/claude_integration_repo/claude_integration_app.py > /home/ubuntu/claude_integration_repo/flask_app.log 2>&1 &
