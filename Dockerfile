### https://gist.github.com/usr-ein/c42d98abca3cb4632ab0c2c6aff8c88a

FROM python:3.12-slim AS python-base

# Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Pip
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PIP_DEFAULT_TIMEOUT 100

# Poetry
ENV POETRY_VERSION 1.8.3
ENV POETRY_HOME "/opt/poetry"
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ENV POETRY_NO_INTERACTION 1

# Paths
ENV PYSETUP_PATH "/opt/pysetup"
ENV VENV_PATH "/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base AS builder-base

RUN apt-get update && apt-get install --no-install-recommends -y curl build-essential

RUN --mount=type=cache,target=/root/.cache curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache poetry install --only=main --no-root --no-directory

FROM python-base AS development

ENV DEBUG=True

WORKDIR $PYSETUP_PATH

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN --mount=type=cache,target=/root/.cache poetry install

WORKDIR /revity

COPY ./revity /revity

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
