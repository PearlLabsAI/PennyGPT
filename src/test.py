from openai import OpenAI
import instructor
from enum import Enum
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from pydantic import BaseModel, Field

# Initialize the console for rich printing
console = Console()


class Models(Enum):
    GPT_4o = "gpt-4o"
    GPT_1106 = "gpt-4-1106-preview"


client = instructor.from_openai(OpenAI())


class Scratchpad(BaseModel):
    """The assistant's scratchpad is useful when they need to think deeply about a question before responding. Information here will be kept for future messages."""

    scratchpad: str = Field(
        ..., description="The scratchpad to be processed by the AI model"
    )


class BasicResponse(BaseModel):
    response: str = Field(..., description="The response from the AI model")


class ClarrifyingQuestion(BaseModel):
    """
    A question that the user can ask to clarify the response
    """

    question: str = Field(..., description="The question for the user.")


class ModelResponse(BaseModel):
    response: Scratchpad | BasicResponse | ClarrifyingQuestion = Field(
        ...,
        description="Either a scratchpad, clarrifying question, or a basic response",
    )


if __name__ == "__main__":
    response = client.chat.messsages.create(
        model=Models.GPT_4o.value,
        response_model=ModelResponse,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an advanced AI assistant designed to provide insightful and accurate responses. "
                    "For complex and challenging questions, utilize the scratchpad to document your thought process "
                    "before delivering a final answer. Always aim to be helpful, clear, and concise."
                ),
            },
            {"role": "user", "content": "Can you tell me more about the project?"},
        ],
    )

    if isinstance(response.response, Scratchpad):
        console.print(
            Panel(Markdown(response.response.scratchpad), title="Scratchpad Response")
        )
    elif isinstance(response.response, BasicResponse):
        console.print(
            Panel(Markdown(response.response.response), title="Basic Response")
        )
    elif isinstance(response.response, ClarrifyingQuestion):
        console.print(
            Panel(Markdown(response.response.question), title="Clarrifying Question")
        )
