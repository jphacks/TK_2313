FROM python:3.11.6-slim AS builder
LABEL version="0.1"
LABEL description="api server"

ENV POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false \
  \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  \
  PYSETUP_PATH="/opt/pysetup"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update && \
  apt-get install --no-install-recommends -y curl && \
  apt-get clean

RUN curl -sSL https://install.python-poetry.org/ | python -

# packages install
RUN mkdir /app
WORKDIR /app
COPY ./pyproject.toml /app/pyproject.toml
RUN apt install -y portaudio19-dev gcc
RUN poetry install --only main

# Python script
COPY ./api/ /app/

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]