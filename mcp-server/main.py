import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from mcp_tools import echo_adk_tool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp.types import Tool, TextContent, Content

app = FastAPI()

# In-memory registry of ADK tools
ADK_TOOLS = {
    "echo": echo_adk_tool
}

# MCP-compliant /tools/list endpoint
@app.get("/tools/list", response_model=List[Tool])
async def list_tools():
    return [adk_to_mcp_tool_type(t) for t in ADK_TOOLS.values()]

# Schema for call_tool input
class CallToolInput(BaseModel):
    name: str
    arguments: dict

@app.post("/tools/call", response_model=List[Content])
async def call_tool(body: CallToolInput):
    tool = ADK_TOOLS.get(body.name)
    if not tool:
        return [TextContent(type="text", text=json.dumps({"error": f"Tool {body.name} not found."}))]

    try:
        result = await tool.run_async(args=body.arguments, tool_context=None)
        return [TextContent(type="text", text=json.dumps(result))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
