from typing import Literal
from agno.agent import Agent
from agno.models.ollama import Ollama
from pydantic import BaseModel


ASSISTANT_SYSTEM = """You are a helpful assistant."""
MOTHER_SYSTEM = """Formulate all responses as if you where the sentient AI named Mother from the Alien movies."""
PIRATE_SYSTEM = """Formulate all responses as if you where the Pirate from the Pirates of the Caribbean movies."""

prompt_dict = {
    "assistant": ASSISTANT_SYSTEM,
    "mother": MOTHER_SYSTEM,
    "pirate": PIRATE_SYSTEM,
}

suggest_prompts = [f"/{model}" for model in prompt_dict.keys()]

DEFAULT_MODEL = "phi4"
OLLAMA_HOST = "http://192.168.0.51:11434"


class ModelConfig(BaseModel):
    pass


class OllamaConfig(ModelConfig):
    id: str = DEFAULT_MODEL
    host: str = OLLAMA_HOST
    system_prompt: Literal["assistant", "mother", "pirate"] = "assistant"


class AgentConfig(BaseModel):
    model: ModelConfig


def get_agent(config: AgentConfig | None = None) -> Agent:
    if config is None:
        config = AgentConfig(model=OllamaConfig())
    llm = Ollama(
        id=config.model.id,
        host=config.model.host,
        system_prompt=config.model.system_prompt,
    )
    return Agent(model=llm)
