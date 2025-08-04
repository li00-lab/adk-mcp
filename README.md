# Weather Agent with Google ADK

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)  
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)  
![Docker](https://img.shields.io/badge/docker-compose-yellow.svg)  
![Google ADK](https://img.shields.io/badge/Google-ADK-red.svg)

A containerized weather information agent built with Google's Agent Development Kit (ADK), exposed through a FastAPI web interface.

## Features

- 🌦️ Get weather information for major cities
- 🤖 Powered by Google's Gemini 2.5 Flash model
- 🐳 Docker container for easy deployment
- 📡 FastAPI web interface with automatic docs
- ☁️ Google Cloud Logging integration
- 🔄 Hot-reload development setup

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Google Cloud credentials (for logging)
- Google ADK installed locally for development

## Core Components

1. Weather Agent (root_agent.py)
   - The main AI agent that provides weather information
   - Uses Google's Gemini 2.5 Flash model
   - Has a built-in get_weather tool that returns mock weather data for New York, London, and Tokyo
   - Logs requests to Google Cloud Logging
2. Web Interface (server.py)
   - Creates a FastAPI web server
   - Uses ADK's get_fast_api_app to automatically:
   - Expose the agent as a web service
   - Generate API documentation
   - Provide a chat interface
3. Containerization
   - Dockerfile and docker-compose.yml package everything to run in an isolated environment
   - Handles dependencies and configuration
   - Makes deployment consistent across different machines

## How It Works

1. User Interaction Flow
   - User accesses localhost:8080 in browser
   - FastAPI serves the ADK web interface
   - User asks questions like "What's the weather in London?"
   - The agent:
     - Processes the request
     - Calls the get_weather tool if needed
     - Returns a formatted response
2. Technical Stack
   - Google ADK: Framework for building AI agents
   - FastAPI: Modern Python web framework
   - UVicorn: ASGI server to run FastAPI
   - Docker: Containerization for easy deployment
   - Google Cloud Logging: For monitoring and debugging

## 🧠 What the FastAPI Server Does in This Setup

### 1. Serves the Agent API

The FastAPI app created with:

```
from google.adk.cli.fast_api import get_fast_api_app
```

is responsible for turning your ADK agent (root_agent) into a running HTTP service. This includes:

1. Accepting user input
2. Routing it through the agent's logic (tools, models, etc.)
3. Returning the response

So instead of running adk chat, you interact with your agent through HTTP.

### 2. Exposes a Web UI for Local Testing

When you pass web=True to get_fast_api_app(...):

```
app = get_fast_api_app(agents_dir=".", web=True)
```

ADK automatically mounts a developer UI at /, allowing you to:

1. Select the agent from a dropdown
2. Submit queries
3. Inspect trace/logs visually

This is super helpful during development and debugging.

### 3. Auto-loads Agent from Your Code

With:

```
agents_dir="."
```

ADK looks for a Python module (**init**.py) in that folder, and expects:

```
from .root_agent import root_agent
```

So the FastAPI app knows exactly:

1. What agent to run (root_agent)
2. What tools it exposes
3. What model it uses

### 4. Makes the Agent Deployable Anywhere

Since the agent runs as a FastAPI app:

1. You can deploy it to Cloud Run, Cloud Functions, GKE, App Engine, or any server
2. Docker + docker-compose makes this portable
3. You can scale it, monitor it, add tracing, etc.

## Test

```
docker compose exec adk_agent bash
pytest -q
```

```
docker compose run --rm --entrypoint "" app \
  bash -c "pytest -q"
```

## 🔁 Summary: Your FastAPI Server

| Function                    | Description                                       |
| --------------------------- | ------------------------------------------------- |
| 🧩 **Agent Loader**         | Dynamically imports `root_agent`                  |
| 🌐 **HTTP Service**         | Exposes endpoints such as `/run_sse`, `/feedback` |
| 💻 **Web UI**               | Developer chat & trace interface                  |
| 🚀 **Deployment Interface** | Container-ready, cloud-native entrypoint          |
