from google.adk.tools.function_tool import FunctionTool

def echo_tool(input: dict) -> dict:
    return {"output": f"Echo: {input.get('input', '')}"}

echo_adk_tool = FunctionTool(
    fn=echo_tool,
    name="echo",
    description="Echo input back."
)
