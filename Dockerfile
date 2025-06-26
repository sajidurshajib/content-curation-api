FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/src


RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    gcc \
    libpq-dev \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY mount/ .


COPY mount/scripts /scripts
RUN chmod u+x /scripts/*.sh

RUN sed -i 's/\r$//g' /scripts/start.sh

EXPOSE 80

CMD ["/scripts/start.sh"]

