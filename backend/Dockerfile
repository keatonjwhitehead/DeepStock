FROM debian:stable

RUN apt-get -qq update 
RUN apt-get -qq install build-essential python3-pip rsync
RUN apt-get -qq install nginx
RUN apt-get -qq install python3-venv

WORKDIR /flask-backend
ADD . /flask-backend

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip3 install -r requirements.txt
RUN echo "environment=\"prod\"" > ./.env
RUN echo "GOOGLE_APPLICATION_CREDENTIALS"=\"./deep-stock-268818-fce7b0e95509.json\" >> ./.env

EXPOSE 8080

CMD ["gunicorn", "main:app", "-b", ":8080", "--timeout", "300", "--workers", "4"]

