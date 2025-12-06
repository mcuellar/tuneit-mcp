# tuneit-mcp

TuneIt MCP Server to expose tools that format, save, and integrate with OpenAI to automate resume tailoring actions.

## Features

This MCP server provides the following tools:

- **format_to_markdown**: Formats a job description into well-structured markdown with proper headers and sections
- **tailor_resume**: Tailors a resume to match a specific job description using AI
- **save_job**: Saves a job description to the `output/jobs/` folder
- **save_tailored_resume**: Saves a tailored resume to the `output/tailored_resumes/` folder

## Prerequisites

- Python 3.10 or higher
- OpenAI API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mcuellar/tuneit-mcp.git
   cd tuneit-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Create a .env file or export directly
   export OPENAI_API_KEY=your_openai_api_key_here
   
   # Optional: customize output directory (defaults to ./output)
   export OUTPUT_DIR=./output
   ```

## Usage

### Running the Server

Start the MCP server:
```bash
python server.py
```

### Configuring with Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "tuneit-mcp": {
      "command": "/path/to/your/.venv/bin/python",
      "args": ["/path/to/tuneit-mcp/server.py"],
      "env": {
        "OPENAI_API_KEY": "your_openai_api_key_here"
      }
    }
  }
}
```

### Tool Descriptions

#### format_to_markdown
Formats a raw job description into clean, well-structured markdown with proper headers including job title, company, responsibilities, requirements, and more.

**Parameters:**
- `job_description` (string): The raw job description text to format

#### tailor_resume
Tailors an existing resume to better match a specific job description while maintaining truthfulness and professional formatting.

**Parameters:**
- `base_resume` (string): The original resume text to tailor
- `job_description` (string): The job description to tailor the resume for

#### save_job
Saves a job description (preferably already formatted in markdown) to the jobs folder.

**Parameters:**
- `job_content` (string): The job description content to save
- `filename` (string): The filename to save as (without extension)

#### save_tailored_resume
Saves a tailored resume to the tailored resumes folder.

**Parameters:**
- `resume_content` (string): The tailored resume content to save
- `filename` (string): The filename to save as (without extension)

## Output Directory Structure

```
output/
├── jobs/
│   ├── software_engineer_acme.md
│   └── data_scientist_techcorp.md
└── tailored_resumes/
    ├── software_engineer_acme_resume.md
    └── data_scientist_techcorp_resume.md
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | - |
| `OUTPUT_DIR` | Directory for saved files | `./output` |

## License

MIT
