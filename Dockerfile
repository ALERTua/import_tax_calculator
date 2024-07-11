FROM python:3.12-slim AS python-base

ENV \
    BASE_DIR=/app

WORKDIR $BASE_DIR

ENV \
    # Python
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # poetry
    POETRY_HOME="$BASE_DIR/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    # venv and requirements path
    VIRTUAL_ENV="$BASE_DIR/venv" \
    # cache path is HOME/.cache
    CACHE_PATH="/root/.cache"

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

RUN python -m venv $VIRTUAL_ENV

ENV PYTHONPATH="$BASE_DIR:$PYTHONPATH"


FROM python-base AS builder-base

RUN apt-get update && \
    apt-get install -y curl

RUN --mount=type=cache,target=$CACHE_PATH \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR $BASE_DIR

COPY poetry.lock pyproject.toml ./

RUN --mount=type=cache,target=$CACHE_PATH \
    poetry install --no-root --only main --compile


FROM builder-base AS development

WORKDIR $BASE_DIR

RUN --mount=type=cache,target=$CACHE_PATH \
    poetry install --no-root --compile

CMD ["bash"]


FROM python-base AS production

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $VIRTUAL_ENV $VIRTUAL_ENV

RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $BASE_DIR

COPY . ./

RUN chmod +x ./*.sh

VOLUME /data

ENV \
    PYTHONPATH="$BASE_DIR/apps:$PYTHONPATH" \
    PORT=8000 \
    PYTHONIOENCODING=utf-8 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

EXPOSE $PORT

HEALTHCHECK --interval=10s --timeout=5s --start-period=10s --retries=5 \
        CMD curl localhost:${PORT}/health || exit 1

CMD ["./entrypoint.sh"]
