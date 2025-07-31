import os
from dotenv import load_dotenv
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from google.cloud import logging as google_cloud_logging
from pydantic import BaseModel
from typing import Literal
# from tracing import CloudTraceLoggingSpanExporter
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, export

# Load env
load_dotenv()

# Logging
logging_client = google_cloud_logging.Client()
logger = logging_client.logger("weather-agent")

# Tracing
# provider = TracerProvider()
# processor = export.BatchSpanProcessor(CloudTraceLoggingSpanExporter())
# provider.add_span_processor(processor)
# trace.set_tracer_provider(provider)

# Use Cloud SQL if provided
AGENT_DIR = os.path.dirname(os.path.abspath(__file__))
session_uri = os.getenv("SESSION_SERVICE_URI")
app_args = {"agents_dir": "adk_agent", "web": True}
if session_uri:
    app_args["session_service_uri"] = session_uri
else:
    logger.log_text("SESSION_SERVICE_URI not set. Using in-memory session service.", severity="WARNING")

# App
app: FastAPI = get_fast_api_app(**app_args)

# Feedback route
class Feedback(BaseModel):
    score: int | float
    text: str | None = ""
    invocation_id: str
    log_type: Literal["feedback"] = "feedback"
    service_name: Literal["weather-agent"] = "weather-agent"
    user_id: str = ""

@app.post("/feedback")
def collect_feedback(feedback: Feedback):
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}
