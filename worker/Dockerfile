# our base image
FROM ngap/alpine-fortran

# Install python and pip
RUN apk add --update python2 py2-pip  python2-dev
RUN apk add --update mariadb-dev

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

# copy files required for the app to run
COPY DBCommunicator.py /usr/src/app/
COPY worker.py /usr/src/app/

# tell the port number the container should expose
#EXPOSE 5200

# run the application
CMD ["python", "/usr/src/app/worker.py"]