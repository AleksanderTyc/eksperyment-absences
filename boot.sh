#!/bin/sh
# used to boot Docker container

# terminate at first error
#~ set -e

source venv/bin/activate

# export FLASK_APP=absences.py
exec flask run
#~ exec flask run -h 0.0.0.0
#~ echo "Jestem w boot.sh i FLASK_APP jest " $FLASK_APP
#~ echo "Wykonuje pwd" $PWD
#~ ls -la $PARAMETR_WYKONANIA
