#!/bin/bash
# Create a virtualenv and install the dependencies into that virtualenv.

## Configuration ##
ENV=env
## End Configuration ##

virtualenv --no-site-packages $ENV
source $ENV/bin/activate
easy_install pip
deactivate
source $ENV/bin/activate
pip install -r requirements.txt

