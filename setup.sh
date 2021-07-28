#!/bin/bash
sudo apt update
sudo apt -y upgrade
sudo apt install -y python3-pip
sudo apt install -y python3-venv
source env/bin/activate
pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install -r requirements.txt
deactivate
