import asyncio
from fastmcp import Client

client = Client("http://localhost:8000/mcp")

async def call_tool():
    async with client:
        job_description = "Software engineer position at Boston Dynamics requiring experience in Python and FastAPI."
        result = await client.call_tool("format_to_markdown", {"job_description": job_description})
        print(result)

asyncio.run(call_tool())