"""
A simple cl chat app with Textual.
"""
# base for this app - Textual example MotherApp

from typing import Iterator

from agno.agent import RunResponse
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input

from .agent import get_agent, prompt_dict, AgentConfig, OllamaConfig
from .app_widgets import CSS, Prompt, Response


class TChat(App):
    """app."""

    AUTO_FOCUS = "Input"
    CSS = CSS
    prompt_name: str
    model_name: str

    def __init__(self, config: AgentConfig | None = None) -> None:
        super().__init__()
        config = config or AgentConfig(model=OllamaConfig())
        self.agent = get_agent(config)
        self.model_name = config.model.id
        self.prompt_name = config.model.system_prompt

    def set_input_title(self, prompt_name: str) -> None:
        self.prompt_name = prompt_name
        self.query_one(
            Input
        ).border_title = f" {prompt_name} / {self.model_name} / ollama"

    def on_mount(self) -> None:
        """set agent on mount."""
        self.set_input_title(self.prompt_name)

    def set_model(self, prompt_name: str) -> None:
        self.agent.model.system_prompt = prompt_dict[prompt_name]
        self.prompt_name = prompt_name
        self.query_one(Input).border_title = f"  Model: ollama / phi4 / {prompt_name}"

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
        response = Response()
        response.border_title = f"{self.prompt_name}"
        await chat_view.mount(response)
        response.anchor()

        self.send_prompt(event.value, response)

    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:
        """Get the response in a thread."""

        response_content = ""
        response_stream: Iterator[RunResponse] = self.agent.run(prompt, stream=True)
        for chunk in response_stream:
            if chunk.content:
                response_content += chunk.content

            self.call_from_thread(response.update, response_content)


def main():
    config = AgentConfig(
        model=OllamaConfig(
            # id="qwen2.5-coder:1.5b",
        )
    )
    app = TChat(config=config)
    app.run()


if __name__ == "__main__":
    main()
