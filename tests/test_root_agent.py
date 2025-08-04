from agents.root_agent import root_agent, get_weather

def test_get_weather_success():
    assert get_weather("London") == {
        "status": "success",
        "report": "Cloudy, 15°C",
    }

def test_get_weather_not_found():
    reply = get_weather("Mars")
    assert reply["status"] == "error"
    assert "No data" in reply["error_message"]

def test_agent_metadata():
    # Smoke-test Agent object created in root_agent.py
    assert root_agent.name == "weather_agent"
    assert any(t.__name__ == "get_weather" for t in root_agent.tools)
