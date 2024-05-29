#!/bin/bash
#
# Description: 
# Tags: Bill
# Date: 2024-05-26
#
python3 -m venv ai_agent_env
source ai_agent_env/bin/activate
pip install openai

source ai_agent_env/bin/activate
python3 magents.py
