#
# Base image
#

FROM python:3.11-slim-bullseye AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y make

#
# Development image
#

FROM base AS development 
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN apt-get install curl -y
RUN curl -sSL https://install.python-poetry.org | python -
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-interaction --no-ansi -vvv
RUN poetry export --only main -f requirements.txt > requirements.txt
COPY src /app/src 
COPY test /app/test
COPY Makefile /app
CMD ["poetry", "run", "make", "run"]



#
# Production image
#

FROM base AS production
COPY src /app/src
COPY --from=development /app/requirements.txt ./
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD ["poetry", "run", "make", "run"]