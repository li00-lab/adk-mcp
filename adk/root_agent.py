from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams

def create_agent():
    return LlmAgent(
        model="gemini-2.0-pro",
        name="echo_client_agent",
        instruction="Use the echo tool to repeat input.",
        tools=[
            MCPToolset(
                connection_params=SseServerParams(
                    url="http://mcp:5000/tools"  # Your FastAPI MCP server
                )
            )
        ]
    )
