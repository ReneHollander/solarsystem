#!/bin/bash

virtualenv --python=python3.5 venv
source venv/bin/activate
pip3 install -r requirements.txt