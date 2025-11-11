FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app
COPY requirements.txt /app

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Install dependencies
#RUN pip install --no-cache-dir --default-timeout=300 -r requirements.txt
#RUN pip install --no-cache-dir --default-timeout=600 --retries 10 -i https://pypi.org/simple -r requirements.txt
RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir --default-timeout=1200 --retries 15 \
    -i https://pypi.org/simple \
    fastapi uvicorn[standard] sqlalchemy psycopg2-binary alembic \
    pydantic jinja2 weasyprint python-multipart sqlalchemy-utils \
    email-validator python-dotenv

# Copy entrypoint if you have one
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Expose port for FastAPI
EXPOSE 8000

# Run the application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
