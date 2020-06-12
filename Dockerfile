FROM python:3.7-alpine

RUN adduser -D absences

WORKDIR /home/absences

RUN python -m venv venv

COPY requirements.txt requirements.txt
RUN ./venv/bin/pip install -r requirements.txt
# RUN pip install -r requirements.txt
RUN ./venv/bin/pip install gunicorn

COPY absences.py ./
COPY migrations migrations
COPY app app
RUN chown -R absences:absences .

COPY boot.sh ./
RUN chmod u+x boot.sh
RUN chown absences:absences boot.sh

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
# Mozliwe, ze zamiast tego mozna uzyc flask run -h 0.0.0.0.
# Analogicznie dla portu mamy FLASK_RUN_PORT i opcje -p.
# ENV FLASK_RUN_HOST 0.0.0.0

# shell form - child shell spawned
# ENTRYPOINT ./boot.sh

# exec form - this shell will run - similar to source ... - preferred
ENTRYPOINT ["./boot.sh"]

# Build:
# docker build -t alekscorrugatedcontainers/absences:0.01 .

# Run:
# docker run --rm -d -e MAIL_PASSWORD="wiadomoJakie" -p 8000:5000 alekscorrugatedcontainers/absences:0.03
# docker run --rm -d -t -e MAIL_PASSWORD="wiadomoJakie" -p 8000:5000 -v /home/aleks/Archiwum/DataScientist/Python/PythonVirtEnvs/absences/database:/home/absences/database alekscorrugatedcontainers/absences:0.03
# rm: delete after stop; d: background; t: create TTY (print output is saved to docker logs); e: environment variable; p: port mapping
# Bez opcji t wyniki print( "..." ) nie pokazuja sie ani na konsoli ani w docker logs.

# See logs:
# docker logs <hash>

# List containers:
# docker container ls

# List running containers:
# docker container ps

# Stop running container:
# docker stop <hash>

# List images (tagged and intermediate):
# docker images

# Inne polecenia Docker uzyte w eksperymentach:

# Zawartosc katalogu /var/tmp/testb wewnatrz kontenera:
# docker run --rm -v /home/aleks/Archiwum/DataScientist/Python/PythonVirtEnvs/absences/gitignored/:/var/tmp/testb --entrypoint="" alekscorrugatedcontainers/absences:0.02 ls -l /var/tmp/testb
# v: mount host directory inside container at given location; entrypoint: set to empty to enable command line arguments;

# Jak wyzej, ale uruchamia python z argumentem skrypt, ktory z kolei przyjmuje kolejny napis jako swoj argument.
# docker run --rm -v /home/aleks/Archiwum/DataScientist/Python/PythonVirtEnvs/absences/gitignored/:/var/tmp/testb --entrypoint="" alekscorrugatedcontainers/absences:0.02 python /var/tmp/testb/testBazy.py /home/absences/app/app.db

# W wersji 0.02 template mielismy zmienna PARAMETR_WYKONANIA uzyta wewnatrz skryptu boot.sh.
# docker run --rm -v /home/aleks/Archiwum/DataScientist/Python/PythonVirtEnvs/absences/gitignored/:/var/tmp/testb -e PARAMETR_WYKONANIA=/var/tmp/testb alekscorrugatedcontainers/absences:0.02
# Ten kontener nie biegnie w background

# Czy biblioteka flask jest dostepna dla python wewnatrz kontenera
# docker run --rm -e MAIL_PASSWORD="wiadomoJakie" -p 8000:5000 --entrypoint="" alekscorrugatedcontainers/absences:0.03 python -m flask

# Czy venv activate ustala nowa zawartosc zmiennej PATH:
# docker run --rm -e MAIL_PASSWORD="wiadomoJakie" -p 8000:5000 --entrypoint="" alekscorrugatedcontainers/absences:0.03 source venv/bin/activate; echo $PATH
# Tylko ze nie dziala, bo srednik konczy polecenie dla docker. W rezultacie echo $PATH wykonuje sie lokalnie a nie w kontenerze.
# Rowniez source nie jest rozpoznawane jako polecenie (executable file not found).

# docker run --rm -e MAIL_PASSWORD="wiadomoJakie" -p 8000:5000 --entrypoint="" alekscorrugatedcontainers/absences:0.03 /bin/sh source venv/bin/activate
# Teraz source dziala ok.
# Nie wiem jak podac wiele kolejnych polecen do wykonania
