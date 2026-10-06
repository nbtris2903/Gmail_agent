# Trisagent

Trisagent is a personal AI agent built with **OpenAI, LangChain, LangGraph, Gmail API, Telegram, and Docker**.

The project is designed to explore how AI Agents can understand natural-language requests, decide when external tools are needed, execute those tools, observe the results, and continue reasoning until a final response can be returned to the user.

Currently, Trisagent can interact with Gmail through a Telegram bot and a terminal interface. The application can also be packaged and run using Docker and Docker Compose.

---

## Architecture

The current system follows this architecture:

```text
User
  |
  v
Telegram / Terminal
  |
  v
LangGraph Agent
  |
  v
OpenAI
  |
  v
Gmail Tools
  |
  v
Gmail API
```

The AI Agent follows an Agent Loop:

```text
Decide
  |
  v
Act
  |
  v
Observe
  |
  v
Decide again
  |
  v
Final Answer
```

For example, when the user asks:

```text
Read my latest email and summarize it.
```

the Agent may perform:

```text
User Request
     |
     v
OpenAI decides to use a tool
     |
     v
get_latest_emails()
     |
     v
Email metadata + message ID
     |
     v
OpenAI decides more information is required
     |
     v
read_email(message_id)
     |
     v
Full email content
     |
     v
OpenAI summarizes the email
     |
     v
Final Answer
```

---

## Features

Current features include:

- Chat with Trisagent through Telegram
- Chat with the Agent through the terminal
- Telegram user whitelist for access control
- Retrieve recent Gmail messages
- Search Gmail using natural-language requests
- Read the full content of an email
- Convert HTML email content into readable plain text
- Summarize and analyze email content using OpenAI
- Multi-step tool calling
- Agent Loop using LangGraph
- Short-term conversation memory
- Gmail authentication using OAuth 2.0
- Debug mode for observing Agent workflow
- Docker containerization
- Docker Compose support

---

## Gmail Tools

Trisagent currently provides three Gmail tools.

### `get_latest_emails`

Retrieves recent emails and returns information such as:

- Message ID
- Sender
- Subject
- Date
- Snippet

### `search_emails`

Searches Gmail using Gmail search queries.

This allows the Agent to find emails based on user requests.

### `read_email`

Reads the full content of a specific email using its Gmail message ID.

The tool extracts the email body and converts HTML content into readable plain text when necessary.

---

## Tech Stack

Trisagent currently uses:

- **Python**
- **OpenAI API**
- **LangChain**
- **LangGraph**
- **Gmail API**
- **Google OAuth 2.0**
- **Telegram Bot API**
- **python-telegram-bot**
- **BeautifulSoup**
- **python-dotenv**
- **Docker**
- **Docker Compose**

---

## Project Structure

```text
gmail_agent/
|
|-- agent.py
|-- agent_graph.py
|-- gmail_tools.py
|-- telegram_bot.py
|-- debug_workflow.py
|
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- Dockerfile
|-- .dockerignore
|-- compose.yaml
|
|-- .env                # Not committed
|-- credentials.json    # Not committed
|-- token.json          # Not committed
`-- .venv/              # Not committed
```

### Main Files

**`agent_graph.py`**

Defines the core AI Agent, including:

- OpenAI model
- Gmail tools
- LangGraph workflow
- Tool execution
- Agent Loop
- Short-term memory

**`gmail_tools.py`**

Contains Gmail API integration and Gmail tools used by the Agent.

**`agent.py`**

Provides a terminal interface for interacting with Trisagent.

**`telegram_bot.py`**

Connects the LangGraph Agent to Telegram and restricts access using a Telegram user whitelist.

**`debug_workflow.py`**

Displays the internal Agent workflow, including:

```text
USER
  |
AGENT -> TOOL
  |
TOOL RESULT
  |
AGENT -> TOOL
  |
TOOL RESULT
  |
AGENT FINAL
```

This is useful for understanding and debugging the Agent Loop.

**`Dockerfile`**

Defines how the Trisagent Docker image is built.

The Docker image includes the Python runtime, application dependencies, and Trisagent source code.

**`compose.yaml`**

Defines how the Trisagent container is started, including environment variables, Gmail authentication files, and container restart behavior.

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_ALLOWED_USER_ID=your_telegram_user_id
```

`TELEGRAM_ALLOWED_USER_ID` restricts access to the authorized Telegram user.

Do not expose or commit API keys and tokens.

The following files and directories are excluded from Git:

```text
.env
credentials.json
token.json
.venv/
__pycache__/
```

---

## Gmail Authentication

The project uses Google OAuth 2.0 to access Gmail.

A Google OAuth credential file is required:

```text
credentials.json
```

After successful authentication, Google generates:

```text
token.json
```

Both files contain sensitive authentication information and must **never be committed to GitHub**.

The current Gmail permission is read-only:

```text
gmail.readonly
```

Therefore, the current version of Trisagent can read Gmail data but cannot send or delete emails.

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
```

Enter the project directory:

```bash
cd Gmail_agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Then configure:

```text
.env
credentials.json
token.json
```

before running the Agent.

---

## Running Trisagent Locally

### Telegram Interface

Run:

```bash
python telegram_bot.py
```

The terminal should display:

```text
Trisagent đang chạy...
```

You can then communicate with the Agent through Telegram.

### Terminal Interface

For direct terminal testing:

```bash
python agent.py
```

### Debug Agent Workflow

To observe the Agent Loop:

```bash
python debug_workflow.py
```

This mode shows when the Agent:

1. receives a user request,
2. decides to call a tool,
3. receives a tool result,
4. calls another tool if necessary,
5. generates the final answer.

---

## Running Trisagent with Docker

Trisagent can be packaged and run inside a Docker container.

### Build the Docker Image

```bash
docker build -t trisagent:v1 .
```

This creates the Docker image:

```text
trisagent:v1
```

### Run with Docker Compose

Make sure the following local files are configured:

```text
.env
credentials.json
token.json
```

Then start Trisagent:

```bash
docker compose up
```

To run Trisagent in the background:

```bash
docker compose up -d
```

Check the container status:

```bash
docker compose ps
```

View container logs:

```bash
docker compose logs -f
```

Stop and remove the Compose container:

```bash
docker compose down
```

After source code or dependency changes, rebuild and restart:

```bash
docker compose up -d --build
```

The Docker workflow is:

```text
Source Code
     |
     v
Dockerfile
     |
     | docker build
     v
Docker Image
trisagent:v1
     |
     | compose.yaml
     v
Container
trisagent-bot
     |
     v
Trisagent
```

Sensitive files such as `.env`, `credentials.json`, and `token.json` are not stored inside the Docker image. They are provided to the container at runtime.

---

## Memory

Trisagent currently uses LangGraph's in-memory checkpointer:

```text
InMemorySaver
```

This provides short-term conversation memory while the application process is running.

Current limitation:

```text
Trisagent running
      |
Conversation memory available
      |
Container / process restarted
      |
Memory is lost
```

Docker does not make this memory persistent.

Persistent memory will be added in a future version.

---

## Security

Sensitive information is stored locally and excluded through `.gitignore` and `.dockerignore`.

Never commit:

```text
OPENAI_API_KEY
TELEGRAM_BOT_TOKEN
credentials.json
token.json
```

Trisagent currently uses a Telegram user whitelist.

The bot checks:

```text
Telegram User ID
       |
       v
Authorized?
   /       \
 YES       NO
  |         |
  v         v
Agent     Access denied
```

Only the configured `TELEGRAM_ALLOWED_USER_ID` is allowed to access the Agent through Telegram.

The current Gmail integration uses read-only access.

---

## Current Status

Current architecture:

```text
Telegram / Terminal
        |
        v
LangGraph Agent
        |
        v
OpenAI
        |
        v
Gmail Tools
        |
        v
Gmail API
```

The application can run locally or inside Docker:

```text
Dockerfile
    |
    v
trisagent:v1
    |
    v
Docker Compose
    |
    v
trisagent-bot
```

Working components:

- OpenAI integration
- LangChain tools
- LangGraph workflow
- Agent Loop
- Gmail API integration
- Gmail OAuth authentication
- Gmail read/search tools
- Email body extraction
- HTML-to-text conversion
- Short-term memory
- Terminal interface
- Telegram interface
- Telegram user whitelist
- Agent workflow debugging
- Docker image
- Docker Compose

---

## Roadmap

Completed:

- [x] Gmail API integration
- [x] OpenAI integration
- [x] LangChain tools
- [x] LangGraph Agent workflow
- [x] Multi-step Agent Loop
- [x] Short-term conversation memory
- [x] Terminal interface
- [x] Telegram interface
- [x] Telegram user authorization / whitelist
- [x] Docker containerization
- [x] Docker Compose

Planned improvements:

- [ ] Improved error handling
- [ ] Persistent conversation memory
- [ ] Long-term user memory
- [ ] Google Calendar integration
- [ ] Gmail draft and send tools
- [ ] FastAPI backend
- [ ] Web interface
- [ ] Cloud deployment
- [ ] Logging and monitoring

---

## Project Goal

The goal of Trisagent is not only to build a chatbot, but to understand and develop a complete AI Agent system capable of:

```text
Understanding
     +
Reasoning
     +
Tool Calling
     +
Memory
     +
External Services
     +
Multiple Interfaces
```

The project will gradually evolve from a Gmail assistant into a more complete personal AI assistant.