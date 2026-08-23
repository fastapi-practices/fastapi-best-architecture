# Python environment from uv
FROM ghcr.io/astral-sh/uv:python3.10-trixie-slim AS builder

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc make python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /fba
WORKDIR /fba

ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/usr/local

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-default-groups --group server --no-install-project

# Preinstall plugin dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    python -c "from backend.plugin.requirements import install_requirements; install_requirements(None)"

# Single FastAPI server image
FROM ghcr.io/astral-sh/uv:python3.10-trixie-slim

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /fba /fba
COPY --from=builder /usr/local /usr/local
COPY deploy/backend/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY deploy/backend/supervisor/fba_server.conf /etc/supervisor/conf.d/

RUN mkdir -p /var/log/fba
EXPOSE 8001
CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
