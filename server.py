"""
TuneIt MCP Server

An MCP server using FastMCP that exposes tools for formatting job descriptions,
tailoring resumes, and saving both to predefined folders.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("tuneit-mcp")

# Lazy initialization of OpenAI client
_client = None


def get_openai_client() -> OpenAI:
    """Get or create the OpenAI client."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        _client = OpenAI(api_key=api_key)
    return _client

# Define output directories
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "./output"))
JOBS_DIR = OUTPUT_DIR / "jobs"
RESUMES_DIR = OUTPUT_DIR / "tailored_resumes"


def ensure_directories():
    """Ensure output directories exist."""
    JOBS_DIR.mkdir(parents=True, exist_ok=True)
    RESUMES_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str, default: str) -> str:
    """Sanitize a filename by removing invalid characters.

    Args:
        filename: The filename to sanitize.
        default: Default filename if sanitized result is empty.

    Returns:
        A sanitized filename safe for use in file paths.
    """
    safe_filename = "".join(c for c in filename if c.isalnum() or c in ("-", "_", " ")).strip()
    return safe_filename if safe_filename else default


def get_unique_filepath(directory: Path, filename: str) -> Path:
    """Get a unique filepath, appending a counter if needed.

    Args:
        directory: The directory to save the file in.
        filename: The base filename (without extension).

    Returns:
        A unique filepath with .md extension.
    """
    filepath = directory / f"{filename}.md"
    counter = 1
    while filepath.exists():
        filepath = directory / f"{filename}_{counter}.md"
        counter += 1
    return filepath


def extract_response_content(response) -> str:
    """Extract content from OpenAI response with validation.

    Args:
        response: The OpenAI chat completion response.

    Returns:
        The content from the response.

    Raises:
        ValueError: If the response is invalid or empty.
    """
    if not response.choices:
        raise ValueError("OpenAI returned an empty response")
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("OpenAI response content is empty")
    return content


@mcp.tool()
def format_to_markdown(job_description: str) -> str:
    """
    Format a job description into well-structured markdown with proper headers.

    Args:
        job_description: The raw job description text to format.

    Returns:
        The job description formatted as markdown with proper headers and sections.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an expert at formatting job descriptions into clean, well-structured markdown.
Format the job description with proper markdown headers and sections including:
- Job Title (as H1)
- Company (if mentioned)
- Location (if mentioned)
- Job Type (if mentioned)
- About the Role / Overview
- Responsibilities
- Requirements / Qualifications
- Nice to Have / Preferred Qualifications (if applicable)
- Benefits (if mentioned)
- How to Apply (if mentioned)

Use proper markdown formatting including headers (##, ###), bullet points, and bold text where appropriate.
Maintain all the original information while improving readability.""",
            },
            {"role": "user", "content": job_description},
        ],
        temperature=0.3,
    )
    return extract_response_content(response)


@mcp.tool()
def tailor_resume(base_resume: str, job_description: str) -> str:
    """
    Tailor a resume to match a specific job description using AI.

    Args:
        base_resume: The original resume text to tailor.
        job_description: The job description to tailor the resume for.

    Returns:
        A tailored version of the resume optimized for the job description.
    """
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an expert resume writer and career coach.
Your task is to tailor the provided resume to better match the job description while:
1. Maintaining truthfulness - only reorganize and emphasize existing skills/experience
2. Using keywords from the job description where they honestly apply
3. Reordering sections to highlight most relevant experience first
4. Adjusting bullet points to emphasize relevant accomplishments
5. Keeping the resume concise and professional
6. Preserving the original format/structure as much as possible

Return the tailored resume in the same format as the input.""",
            },
            {
                "role": "user",
                "content": f"## Base Resume:\n{base_resume}\n\n## Job Description:\n{job_description}",
            },
        ],
        temperature=0.4,
    )
    return extract_response_content(response)


@mcp.tool()
def save_job(job_content: str, filename: str) -> str:
    """
    Save a job description to the jobs folder.

    Args:
        job_content: The job description content to save (preferably markdown formatted).
        filename: The filename to save as (without extension, .md will be added).

    Returns:
        A confirmation message with the saved file path.
    """
    ensure_directories()
    safe_filename = sanitize_filename(filename, "job")
    filepath = get_unique_filepath(JOBS_DIR, safe_filename)
    filepath.write_text(job_content, encoding="utf-8")
    return f"Job description saved successfully to: {filepath.absolute()}"


@mcp.tool()
def save_tailored_resume(resume_content: str, filename: str) -> str:
    """
    Save a tailored resume to the tailored resumes folder.

    Args:
        resume_content: The tailored resume content to save.
        filename: The filename to save as (without extension, .md will be added).

    Returns:
        A confirmation message with the saved file path.
    """
    ensure_directories()
    safe_filename = sanitize_filename(filename, "tailored_resume")
    filepath = get_unique_filepath(RESUMES_DIR, safe_filename)
    filepath.write_text(resume_content, encoding="utf-8")
    return f"Tailored resume saved successfully to: {filepath.absolute()}"


if __name__ == "__main__":
    mcp.run()
