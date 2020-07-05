FROM python:3.7

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./ ./

ENV PYTHONPATH=/app
ENV SERVER_WORKERS=1
CMD python -m sanic autoapp.app --host=0.0.0.0 --port=${SERVER_PORT} --workers=${SERVER_WORKERS}
