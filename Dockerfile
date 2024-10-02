FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV APP_DIR=/app

ENV \
    # OS
    PORT=8000 \
    # uv
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_CACHE_DIR="$APP_DIR/.uv_cache" \
    # Python
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONIOENCODING=utf-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    # LC_ALL=en_US.UTF-8 \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    # venv and requirements path
    VIRTUAL_ENV="$APP_DIR/.venv" \
    PYTHONPATH="$APP_DIR/apps:$PYTHONPATH"

WORKDIR $APP_DIR

# Cache and bind mounts for uv
RUN \
    --mount=type=cache,target=$UV_CACHE_DIR \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . .

# Cache mount again for uv sync
RUN \
    --mount=type=cache,target=$UV_CACHE_DIR \
    uv sync --frozen --no-dev

CMD ["bash"]

FROM builder AS development

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY --from=builder $APP_DIR $APP_DIR

EXPOSE $PORT

VOLUME /data

FROM development AS production

ENV USERNAME=nonroot

RUN useradd -ms /bin/bash $USERNAME

USER $USERNAME

COPY --from=development --chown=$USERNAME:$USERNAME $APP_DIR $APP_DIR

RUN chmod -R +x $APP_DIR/*.sh

HEALTHCHECK \
    --interval=10s --timeout=5s --start-period=10s --retries=5 \
    CMD curl localhost:${PORT}/health || exit 1

CMD ["./entrypoint.sh"]
