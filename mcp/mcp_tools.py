from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.base import ToolContext

# Define a basic echo tool as a Python function
def echo_tool(input: dict, tool_context: ToolContext = None) -> dict:
    text = input.get("input", "")
    return {"output": f"Echo: {text}"}

# Wrap it with ADK's FunctionTool
echo_adk_tool = FunctionTool(echo_tool, name="echo", description="Echo input text.")
