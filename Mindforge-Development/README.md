# MINDFORGE – M-PESA EXPENSE COACH

## Project Overview
MINDFORGE is a Python-based personal finance assistant that helps users record expenses, analyse spending and receive AI-powered financial guidance.

## Features
1. Record and view expenses.
2. Calculate total spending.
3. Analyse spending by category.
4. Ask MINDFORGE AI questions about spending.
5. Maintain conversation history.
6. Generate AI session summaries.
7. Save and reopen sessions in JSON and Markdown.
8. Import M-PESA confirmation SMS messages.
9. Extract transaction IDs, amounts, fees, dates and recipients.
10. Automatically categorise imported transactions.
11. Prevent duplicate M-PESA transaction imports.
12. Generate financial analytics reports.
13. Generate AI-powered financial insights using Claude.

## Technology
- Python
- Anthropic Claude API
- JSON storage
- python-dotenv

## Installation
Activate your virtual environment and install dependencies:

    pip install -r requirements.txt

Create a `.env` file in the project root with:

    ANTHROPIC_API_KEY=your_api_key
    ANTHROPIC_MODEL=claude-sonnet-5

Never upload your `.env` file or expose your API key.

## Run the application

    python main.py

## Menu
1. Record an expense
2. View all expenses
3. Calculate total spending
4. View spending by category
5. Exit
6. Ask MINDFORGE AI
7. Save current session
8. Open previous session
9. Import M-PESA SMS
10. View financial analytics report
11. Generate AI financial insights

## Project Structure

- `main.py` – Main application and menu
- `expense_manager.py` – Expense recording and management
- `ai_engine.py` – Claude conversation assistant
- `financial_systems/` – SMS parsing, categorisation, storage and analytics
- `financial_advisor_engine/` – AI financial advisor
- `conversation.py` – Conversation history
- `session_manager.py` – Session saving and loading
- `prompts.py` – AI prompts
- `expenses.json` – Expense records
- `sessions/` – Saved sessions
- `samples/` – Sample session files

## Team Responsibilities
- Wil – Application development and integration
- Dan – Financial systems, expense management and M-PESA SMS processing
- Mayah – GitHub repository management and AI integration
## Individual Contributions

### Wilford Eshikumo – Application Development and Integration Lead
- Led development and integration of the main MINDFORGE application.
- Worked on the main application menu and user interaction flow.
- Integrated expense management with the AI assistant.
- Connected the application to financial systems, analytics and session management.
- Contributed to application testing, debugging and overall functionality.

### Dan – Financial Systems Development
- Developed financial management components.
- Worked on M-PESA SMS parsing and transaction processing.
- Contributed to expense categorisation and financial analytics.

### Mayah – AI Integration and Repository Management
- Worked on AI integration and prompt development.
- Managed GitHub repository coordination.
- Contributed to project integration and collaboration.


## Security
API credentials are stored in environment variables and excluded from version control.
