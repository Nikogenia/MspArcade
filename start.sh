#!/bin/bash
export DISPLAY=:0
cd /home/maker/MspArcade || exit
source venv/bin/activate
python3 main.py
