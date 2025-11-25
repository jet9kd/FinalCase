FROM python:3.11-slim

WORKDIR /app

# system deps for matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6-dev libjpeg62-turbo-dev libpng-dev build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY src/ ./src
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# copy assets if present in build context
COPY assets/ ./assets

# output dir (will be served)
RUN mkdir -p /app/output

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
