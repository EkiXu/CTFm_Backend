FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /backend
WORKDIR /backend

COPY ./requirements.txt /backend/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install supervisor \
    && pip install uwsgi  \
    && pip install daphne

COPY . /backend

COPY supervisord.conf /etc/supervisord.conf

EXPOSE 8086
CMD ["supervisord","-n","-c","/etc/supervisord.conf"]