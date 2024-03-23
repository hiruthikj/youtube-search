# https://testdriven.io/blog/docker-best-practices/#use-multi-stage-builds
ARG PYTHON_VERSION=3.10 \
    LINUX_VERSION=slim

FROM python:${PYTHON_VERSION}${LINUX_VERSION:+-$LINUX_VERSION} AS final

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH="${PYTHONPATH}:/code/src" \
    # For pipenv
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PIPENV_VENV_IN_PROJECT=1

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential

WORKDIR /code
COPY Pipfile Pipfile.lock /code/

# PIPENV_VERSION=2023.9


RUN pip install pipenv \
    && python -m pipenv requirements --hash > /code/requirements.txt \
    && python -m pip install --no-cache-dir -r /code/requirements.txt \
    && rm requirements.txt

COPY ./src /code/src

# Create a non-root user
RUN addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home --disabled-password appuser
USER appuser

RUN ls
# RUN ls && sd

EXPOSE 8089
ENTRYPOINT ["uvicorn", "src.youtube_app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8089"]


# NOTE: --shell /bin/false will remove shell access
