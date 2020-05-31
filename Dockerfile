FROM python:3.7-alpine

RUN adduser -D absences

WORKDIR /home/absences

RUN python -m venv venv

COPY requirements.txt requirements.txt
RUN ./venv/bin/pip install -r requirements.txt
# RUN pip install -r requirements.txt

COPY boot.sh absences.py ./
RUN chmod u+x boot.sh

COPY migrations migrations
COPY app app

RUN chown -R absences:absences .
USER absences

EXPOSE 5000
ENV FLASK_APP absences.py

# Wyglada na to, ze w Flask istnieje nieudokumentowana opcja konfiguracyjna. Nie wspomina o niej Flask doc, trafienia na Google dotycza innych stron, np:
# https://docs.docker.com/compose/gettingstarted/
# https://gist.github.com/devhero/bc0789e0ebcfcce457c3e59f5232389f
# https://amgadmadkour.github.io/posts/2020/04/07/start-flask-sudo.html
# https://stackoverflow.com/questions/41940663/why-cant-i-change-the-host-and-port-that-my-flask-app-runs-on
# Moje rozumienie: Bez niej Flask nasluchuje na 127.0.0.1. Jest to wewnetrzny adres maszyny UNIX, tutaj Alpine wewnatrz kontenera.
# Jest on niedostepny dla requests przychodzacych z zewnatrz systemu. Z kolei 0.0.0.0 oznacza, ze serwer przyjmuje requests ze wszystkich kierunkow.
ENV FLASK_RUN_HOST 0.0.0.0

# shell form - child shell spawned
# ENTRYPOINT ./boot.sh

# exec form - this shell will run - similar to source ... - preferred
ENTRYPOINT ["./boot.sh"]

# Build:
# docker build -t alekscorrugatedcontainers/absences:0.01 .
# First test:
# docker run --rm alekscorrugatedcontainers/absences:0.01
# docker run --rm -v /home/aleks/Archiwum/DataScientist/Python/PythonVirtEnvs/absences/gitignored/:/var/tmp/testb --entrypoint="" alekscorrugatedcontainers/absences:0.02 python /var/tmp/testb/testBazy.py /home/absences/app/app.db
# docker run --rm -e MAIL_PASSWORD="wiadomoJakie" -p 8000:5000 alekscorrugatedcontainers/absences:0.03
