#!/bin/bash

virtualenv --python=python3.5 venv
source venv/bin/activate
pip3 install -r requirements.txt
pip3 install git+https://github.com/brad/pyeuclid.git
pip3 install git+https://github.com/jorgecarleitao/pyglet-gui.git