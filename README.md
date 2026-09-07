# Pilot Terminal

An AI-driven terminal assistant. Talk in natural language, and Pilot can read/write local files, run shell commands, search the web, and list project structure — from a small dark TUI.

Built as a personal coding companion: debug a file, inspect a folder, run a command, or just ask a question.

## Features

- **Natural language in the terminal** — describe what you want; the agent picks tools when needed
- **File tools** — read and write local files
- **Shell execution** — run commands and get stdout / stderr / exit code
- **Web search** — look up docs and current info (skipped when the model already knows the answer)
- **Directory tree** — list a folder as a readable tree in the UI
- **Session memory** — previous turns stay in the conversation for the life of the process
- **OpenAI-compatible API** — any provider with a chat-completions endpoint (set `base_url`)
- **Textual TUI** — dark screen, Enter to send, Backspace on an empty prompt clears the transcript

## Requirements

- Python 3.10+
- An API key for an OpenAI-compatible chat model

## Setup

```bash
git clone https://github.com/Devansh-debug344/Pilot-terminal---AI-DRIVEN-TERMINAL.git
cd Pilot-terminal---AI-DRIVEN-TERMINAL
```

Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install openai python-dotenv rich textual typer googlesearch-python
```

Create a `.env` in the project root (this file is gitignored):

```env
API_KEY=your_api_key_here
model=your_model_name
base_url=https://api.openai.com/v1
```

| Variable   | Meaning |
|------------|---------|
| `API_KEY`  | Provider key |
| `model`    | Model id the client should call |
| `base_url` | OpenAI-compatible base URL |

Any provider that speaks the OpenAI chat-completions + tools API works — swap `base_url` and `model` accordingly.

## Run

From the project root:

```bash
python main.py
```

That starts the Textual app (`PilotApp`). Type a request, press **Enter**.

- **Enter** — send the current prompt
- **Backspace** with an empty prompt — clear the output log

A simpler Typer CLI path exists in `AI/UI/cli.py` but is commented out in `main.py`.

## What you can ask

```
Fix fun.py
What's in storage.py?
Show structure of .
Show structure of /home/you/project
Run the tests
What's the latest Python version?
Tell me a joke
```

The system prompt tells the model to use tools only when they help: read/write/run for local work, search for current or unknown facts, and answer casual questions directly.

## Project structure

```
Pilot-terminal---AI-DRIVEN-TERMINAL/
├── main.py                      # Entry: Client → Agent → PilotApp
├── .gitignore
└── AI/
    ├── Agent/agent.py           # Conversation loop + tool dispatch
    ├── Config/config.py         # Loads API_KEY, model, base_url from .env
    ├── LLM/client.py            # OpenAI-compatible chat client with tools
    ├── SystemInstruction/prompt.py
    ├── tool/tools.py            # read / write / shell / web_search / list_directory
    └── UI/
        ├── cliscreen.py         # Textual TUI
        └── cli.py               # Optional Typer one-shot CLI
```

### How a request flows

1. `main.py` builds an `API` config, an LLM `Client`, and an `Agent`, then runs `PilotApp`.
2. Your message is appended to the in-memory history (system prompt on the first turn).
3. The client calls `chat.completions.create` with the tool schemas and `tool_choice="auto"`.
4. If the model returns tool calls, `Agent.tool_request` runs them and feeds results back until the model replies in text.
5. The TUI prints the reply. Directory listings are rendered as a Rich tree when possible.

## Tools

| Tool | What it does |
|------|----------------|
| `read_from_file(filepath)` | Read a local file |
| `write_in_file(filepath, content)` | Overwrite / create a file |
| `shell_commands(command)` | `subprocess.run(..., shell=True)` — returns stdout, stderr, returncode |
| `web_search(query)` | Top search results via `googlesearch` |
| `list_directory(path)` | Tree of a directory (skips `__pycache__`, `.git`, `.venv`, `node_modules`, …) |

## Safety notes

This is a local agent with **unrestricted** file write and shell access on your machine. Treat it like handing the model your keyboard.

- Do not point it at secrets you would not type into a terminal yourself
- Review write and shell actions before you trust them on important paths
- Keep `.env` out of git (already ignored)

## Notes / limitations

- Conversation memory lives in process RAM only — it resets when you quit
- `shell_commands` uses `shell=True`; quotes and chaining behave like a normal shell
- Default home path in the system prompt is hardcoded (`/home/devansh`) — change it in `AI/SystemInstruction/prompt.py` if your machine differs
- No `requirements.txt` in the repo yet; install the packages listed above

## License

Not specified. Add one if you want others to reuse this.
