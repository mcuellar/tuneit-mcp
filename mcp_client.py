import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

# Docs: https://gofastmcp.com/getting-started/quickstart#call-your-server

async def call_tool():
    async with client:
        job_description = "Software engineer position at Boston Dynamics requiring experience in Python and FastAPI."
        result = await client.call_tool("format_to_markdown", {"job_description": job_description})

        # result.content is a list of TextContent objects; get the text from the first one
        output = result.content[0].text if result.content else ""
        return output

print(asyncio.run(call_tool()))