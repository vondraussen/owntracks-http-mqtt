FROM python:alpine

RUN apk add --no-cache tzdata
ENV TZ=Europe/Berlin
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt
COPY app.py /opt/app/

CMD [ "python", "-u", "/opt/app/app.py" ]