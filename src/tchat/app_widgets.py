from textual.widgets import Markdown


class Prompt(Markdown):
    """Markdown for the user prompt."""


class Response(Markdown):
    """Markdown base for a response."""

    BORDER_TITLE = "response"


CSS = """
    Prompt {
        background: $primary 10%;
        color: $text;
        margin: 1;
        margin-right: 8;
        padding: 1 2 0 2;
    }

    Response {
        border: wide $success;
        background: $success 10%;
        color: $text;
        margin: 1;
        margin-left: 8;
        padding: 1 2 0 2;
    }

    """
