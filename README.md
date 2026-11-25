# MindForge AI: M-Pesa Expense Coach

**Group:** [MindForgeAi]
**Members:**
- Wilford (Will): Application Development Lead
- Mayah: AI Integration Lead
- Daniel (Dan): Financial Systems Lead

## What the tool does

MindForge is a Python command-line assistant that helps Kenyan users track
and understand their spending. The user talks to the AI coach over several
turns, reporting expenses and asking questions such as "How much have I spent
on transport so far?". The coach remembers everything said earlier in the
session by sending the full message history with every API call to Claude.

Each AI reply is returned as JSON and checked by the code before the user
sees it. If the check fails, the tool retries once and then shows a clear
error message. When the user saves the session, a final AI call summarises
the whole conversation, and the conversation and summary are saved to a
dated file in `sessions/`.

Other features: M-Pesa SMS import, automatic categorisation, financial
analytics report, and AI financial insights.

## How to run

1. Install the packages (from the project root):

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Set your API key (see the next section).

3. Start the app:

   ```bash
   cd Mindforge-Development
   python main.py
   ```

## How to set the API key

Create a file named `.env` in the project root (the same folder as this
README) containing one line:

```
ANTHROPIC_API_KEY=your-key-here
```

The `.env` file is listed in `.gitignore`, so it is never committed. Never
type the key directly into the code.

## How to use it

In the menu:

- **6**: Ask MINDFORGE AI (the multi-turn chat with memory)
- **7**: Save the session (creates the AI summary and a dated `.json` and `.md` file in `sessions/`)
- **8**: Open a previous session
- **5**: Exit

Other options: record expenses, import an M-Pesa SMS, view the analytics
report, and generate AI financial insights.

## Sample session

A saved 4-turn session from our own testing is in the `samples/` folder.

## Project structure

- `Mindforge-Development/`: the main app (menu, chat, prompts, session saving)
- `financial_systems/`: M-Pesa SMS parsing, categorisation, analytics
- `ai_engine/`: AI financial insights module
- `samples/`: sample saved session