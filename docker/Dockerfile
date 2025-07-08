FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Update system packages for security
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Install Poetry
RUN pip install poetry==1.7.1

# Copy only dependency files first for better caching
COPY ../pyproject.toml ../poetry.lock* /app/

# Configure Poetry to not use a virtual environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy rest of the source code and set proper ownership
COPY --chown=appuser:appuser ../ /app/

# Switch to non-root user
USER appuser

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Default command (will be overridden by Docker Compose)
CMD ["python", "src/main.py"] 
