Environment Variables
Create a .env file:
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

Do not commit .env, credentials.json, or token.json to GitHub.
Run
Activate the virtual environment and run:
python telegram_bot.py

For terminal testing:
python agent.py

For debugging the Agent workflow:
python debug_workflow.py

Current Status
Trisagent currently supports read-only Gmail access.
Current Gmail tools:
- get_latest_emails
- search_emails
- read_email
Future versions may include:
- Telegram user authorization
- Google Calendar integration
- Persistent memory
- Additional Gmail actions
- Web interface
- Cloud deployment