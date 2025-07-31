import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.runners import Runner
from google.genai import types
from root_agent import create_agent  # assumes you have agent.py in same directory

async def run_agent():
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    # Start a session
    session = await session_service.create_session(
        state={}, app_name="echo_mcp_app", user_id="user1"
    )

    agent = await create_agent() if asyncio.iscoroutinefunction(create_agent) else create_agent()

    # Prepare the query
    query = "Echo back: Hello World"
    message = types.Content(role="user", parts=[types.Part(text=query)])

    runner = Runner(
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service,
        app_name="echo_mcp_app",
    )

    print(f"🟢 Sending query: {query}\n")
    events = runner.run_async(session_id=session.id, user_id=session.user_id, new_message=message)

    async for event in events:
        print(f"🔹 Event: {event}")

if __name__ == "__main__":
    asyncio.run(run_agent())
