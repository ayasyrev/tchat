"""
A simple cl chat app with Textual.
"""

from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown

from .constants import CSS


class Prompt(Markdown):
    """Markdown for the user prompt."""


class Response(Markdown):
    """Markdown base for a response."""

    BORDER_TITLE = "response"


class TChat(App):
    """app."""

    AUTO_FOCUS = "Input"

    CSS = CSS

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id="chat-view"):
            response = Response("Hello")
            response.border_title = "hello message"
            yield response
        text_input = Input(
            placeholder="How can I help you?",
        )
        yield text_input
        yield Footer()

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        """When the user hits return."""
        chat_view = self.query_one("#chat-view")
        event.input.clear()
        input_value = event.value
        await chat_view.mount(Prompt(input_value))
        await chat_view.mount(response := Response())
        response.anchor()

        self.send_prompt(event.value, response)

    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:
        """Get the response in a thread."""

        response_content = "test response"
        self.call_from_thread(response.update, response_content)


def main():
    app = TChat()
    app.run()


if __name__ == "__main__":
    main()
