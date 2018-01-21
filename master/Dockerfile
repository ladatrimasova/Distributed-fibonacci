# our base image
FROM ngap/alpine-fortran

# Install python and pip
RUN apk add --update python2 py2-pip  python2-dev
RUN apk add --update  mariadb-dev

#RUN apk add --update gcc

# install Python modules needed by the Python app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

RUN rm -rf /usr/src/app/*

# copy files required for the app to run
COPY DBCommunicator.py /usr/src/app/
COPY master.py /usr/src/app/

# tell the port number the container should expose
EXPOSE 1234

# run the application
CMD ["python", "/usr/src/app/master.py"]