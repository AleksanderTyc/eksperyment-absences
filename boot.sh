#!/bin/sh
# used to boot Docker container

# terminate at first error
#~ set -e

source venv/bin/activate

# export FLASK_APP=absences.py
# exec flask run

# Wiemy, ze nie dziala
# exec gunicorn -w 4 -b 127.0.0.1:5000 absences:aplikacja

# Wiemy, ze dziala
# exec gunicorn -w 4 -b :5000 absences:aplikacja
# exec gunicorn -w 4 -b :5001 absences:aplikacja
# Parametr bind (-b) okresla numer portu, na ktorym nasluchuje gunicorn. Konfiguracja 5001 oznacza, ze Docker container exposes port 5001.
# Wtedy uruchomienie kontenera musi nastapic z opcja -p hostport:5001. Dockerfile EXPOSE tez powininen wskazywac 5001, ale, jak wiemy, nie ma to znaczenia.

# Tez dziala
# exec gunicorn -w 4 -b 0.0.0.0:5000 absences:aplikacja
exec gunicorn --access-logfile - -w 2 -b 0.0.0.0:5000 absences:aplikacja


#~ exec flask run -h 0.0.0.0
# Zamiast FLASK_RUN_HOST

#~ echo "Jestem w boot.sh i FLASK_APP jest " $FLASK_APP
#~ echo "Wykonuje pwd" $PWD
#~ ls -la $PARAMETR_WYKONANIA
# Test opcji -e w uruchomieniu kontenera

