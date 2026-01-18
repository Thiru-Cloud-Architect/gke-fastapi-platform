# --------
# Builder stage
# --------
FROM python:3.11-slim AS builder

WORKDIR /build

COPY app/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# --------
# Runtime stage
# --------
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (security best practice)
RUN useradd -m appuser

# Copy pre-built wheels
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy app code
COPY app/ .

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
