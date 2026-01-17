from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import logging
from pythonjsonlogger import jsonlogger
import os

# --------------------
# Logging (structured JSON)
# --------------------
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# --------------------
# App
# --------------------
app = FastAPI(title="GKE FastAPI Platform")

# --------------------
# Prometheus metrics
# --------------------
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["endpoint"]
)

# --------------------
# Routes
# --------------------
@app.get("/")
def root():
    logger.info("Root endpoint called")
    REQUEST_COUNT.labels("GET", "/").inc()
    return {"message": "FastAPI running on GKE 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/slow")
def slow_endpoint():
    start = time.time()
    time.sleep(1.5)
    duration = time.time() - start

    REQUEST_LATENCY.labels("/slow").observe(duration)
    REQUEST_COUNT.labels("GET", "/slow").inc()

    return {"message": "This was slow", "duration": duration}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/env")
def env():
    return {
        "project": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "environment": os.getenv("ENV", "dev")
    }
