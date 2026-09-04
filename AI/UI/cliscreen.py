"""A small input/output terminal for the Pilot agent."""

from __future__ import annotations

import json
from typing import Any

from rich.tree import Tree
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.events import Key
from textual.widgets import Label, RichLog, TextArea


class TerminalUI(App[None]):
    """A deliberately minimal conversational terminal."""

    TITLE = "Pilot"
    CSS = """
    Screen { background: #101114; color: #e5e7eb; }
    #output { height: 1fr; padding: 1 2; background: #101114; color: #e5e7eb; }
    #input-area { height: 7; padding: 1 2; border-top: solid #30333a; background: #17181d; }
    #prompt { height: 4; border: solid #555b6b; background: #202228; color: #f8fafc; }
    #prompt:focus { border: solid #a78bfa; }
    #hint { height: 1; color: #8b919e; margin: 0 1; }
    """

    BINDINGS = [
        Binding("enter", "submit", "Send", priority=True),
    ]

    def __init__(self, agent: Any | None = None) -> None:
        super().__init__()
        self.agent = agent
        self._request_in_flight = False

    def compose(self) -> ComposeResult:
        with Vertical():
            yield RichLog(id="output", wrap=True, markup=True)
            with Container(id="input-area"):
                yield TextArea("", id="prompt", show_line_numbers=False)
                yield Label("Enter to send  ·  Backspace clears output when the prompt is empty", id="hint")

    def on_mount(self) -> None:
        self.query_one("#output", RichLog).write("[bold #c4b5fd]Pilot[/bold #c4b5fd] ready.")
        self.query_one("#prompt", TextArea).focus()

    def action_submit(self) -> None:
        prompt = self.query_one("#prompt", TextArea)
        query = prompt.text.strip()
        if not query or self._request_in_flight:
            return
        self._request_in_flight = True
        prompt.text = ""
        self._write_user(query)
        self._request_agent(query)

    def action_clear(self) -> None:
        self.query_one("#output", RichLog).clear()

    def on_key(self, event: Key) -> None:
        """Clear the transcript with Backspace only when there is nothing to edit."""
        if event.key == "backspace" and not self.query_one("#prompt", TextArea).text:
            event.stop()
            self.action_clear()

    def _write_user(self, query: str) -> None:
        self.query_one("#output", RichLog).write(f"[bold #a78bfa]You[/bold #a78bfa]\n{query}\n")

    def _request_agent(self, query: str) -> None:
        output = self.query_one("#output", RichLog)
        try:
            if self.agent is None:
                response = "Demo mode — create `PilotApp(agent=agent)` to connect your AI agent."
            else:
                response = self.agent.request(query)
            self._write_response(str(response))
        except Exception as error:
            output.write(f"[red]Agent error:[/red] {error}\n")
        finally:
            self._request_in_flight = False

    def _write_response(self, response: str) -> None:
        """Render directory listings as a Rich tree, otherwise write normal text."""
        output = self.query_one("#output", RichLog)
        tree = self._directory_tree(response)
        output.write("[bold #c4b5fd]Pilot[/bold #c4b5fd]")
        output.write(tree if tree is not None else response)
        output.write("")

    @staticmethod
    def _directory_tree(response: str) -> Tree | None:
        """Turn the list_directory tool's text format into a readable tree."""
        try:
            payload = json.loads(response)
            if isinstance(payload, dict):
                response = str(payload.get("structure", response))
        except (TypeError, json.JSONDecodeError):
            pass

        lines = [line for line in response.splitlines() if "📁" in line or "📄" in line]
        if not lines or not lines[0].lstrip().startswith("📁"):
            return None

        root_name = lines[0].strip().removeprefix("📁 ")
        root = Tree(f"[bold #a78bfa]📁 {root_name}[/bold #a78bfa]", guide_style="dim #71717a")
        parents: list[Tree] = [root]

        for line in lines[1:]:
            branch_at = max(line.find("├── "), line.find("└── "))
            if branch_at < 0:
                continue
            depth = branch_at // 4 + 1
            label = line[branch_at + 4 :].strip()
            is_directory = label.startswith("📁")
            style = "#a78bfa" if is_directory else "#cbd5e1"
            node = parents[min(depth - 1, len(parents) - 1)].add(f"[{style}]{label}[/{style}]")
            if len(parents) <= depth:
                parents.append(node)
            else:
                parents[depth] = node
                del parents[depth + 1 :]
        return root


PilotApp = TerminalUI


if __name__ == "__main__":
    PilotApp().run()
