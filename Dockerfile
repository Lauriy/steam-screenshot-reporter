FROM python:3.9

LABEL maintainer="Lauri Elias <lauri.elias@indoorsman.ee>"

RUN apt-get update && apt-get install uwsgi -y

WORKDIR /home/docker/steam-screenshot-reporter

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH /root/.local/bin:$PATH

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY manage.py uwsgi.ini ./

COPY docker-entrypoint.sh docker-entrypoint-dev.sh /usr/bin/

COPY reporter ./reporter

COPY classifier_model.onnx /root/.NudeNet/classifier_model.onnx

RUN chmod +x /usr/bin/docker-entrypoint.sh && \
    chmod +x /usr/bin/docker-entrypoint-dev.sh

EXPOSE 8000

# No single quotes!
ENTRYPOINT ["docker-entrypoint.sh"]
