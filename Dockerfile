FROM python:3.12

WORKDIR /app

RUN pip install poetry==2.1.3
ENV POETRY_NO_INTERACTION=1 \
	POETRY_VIRTUALENVS_IN_PROJECT=1 \
	POETRY_VIRTUALENVS_CREATE=1 \
	PYTHONUNBUFFERED="true"


COPY pyproject.toml poetry.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/pypoetry poetry install 

COPY . /app/

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000
CMD ["fastapi", "run", "./src/main.py", "--port", "8000", "--workers", "2"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]