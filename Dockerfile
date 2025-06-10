FROM python:3.11-slim

WORKDIR /app

COPY holiday-calendar/pyproject.toml holiday-calendar/uv.lock ./
COPY data/ ./data/

RUN pip install uv && \
    uv sync --frozen

COPY holiday-calendar/ ./

EXPOSE 8080

CMD ["uv", "run", "python", "main.py"]