import os
from pathlib import Path

import google.auth
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.cloud import logging as google_cloud_logging

# Load environment variables from .env
root_dir = Path(__file__).parent.parent
load_dotenv(dotenv_path=root_dir / ".env")

# Default fallbacks
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# Cloud logging setup
logging_client = google_cloud_logging.Client()
logger = logging_client.logger("weather-agent")

def get_weather(city: str) -> dict:
    logger.log_text(f"Weather requested for {city}", severity="INFO")
    mock_weather = {
        "newyork": "Sunny, 25°C",
        "london": "Cloudy, 15°C",
        "tokyo": "Light rain, 18°C",
    }
    city_key = city.lower().replace(" ", "")
    if city_key in mock_weather:
        return {"status": "success", "report": mock_weather[city_key]}
    return {"status": "error", "error_message": f"No data for {city}"}

root_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant designed to give weather reports.",
    tools=[get_weather],
)
