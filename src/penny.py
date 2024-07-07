import click
import os
import sys
import openai
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from anthropic import Anthropic
import re

# Initialize OpenAI client and Rich console
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
console = Console()


# Constants for excluded files and directories
EXCLUDE_DIRS = [
    ".git",
    ".venv",
    ".tox",
    ".toxenv",
    ".venv",
    "node_modules",
]

EXCLUDE_FILES = ["package-lock.json", "package.json", "yarn.lock"]
EXCLUDE_EXT = ["pyc"]


def read_data(input_data):
    """
    Load the files under the directory and write the readme.md file.
    """
    file_data = ""
    for root, dirs, files in os.walk(input_data):
        for file in files:
            if file and any(re.search(exclude, file) for exclude in EXCLUDE_FILES):
                continue
            if file and any(re.search(exclude, root) for exclude in EXCLUDE_DIRS):
                continue
            if file and any(re.search(exclude, file) for exclude in EXCLUDE_EXT):
                continue
            try:
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data += (
                        f"<file>{file_path}</file>\n"
                        + "<contents>```\n"
                        + f.read()
                        + "\n```\n</contents>\n"
                    )
            except Exception as e:
                console.print(
                    f"Error reading file '{file_path}': {e}", style="bold red"
                )
                continue
    return file_data


@click.command()
@click.option(
    "-s",
    "--search",
    is_flag=True,
    help="Search for prompts in the instructions folder.",
)
@click.option("-i", "--input", type=str, help="The name of the prompt to execute.")
@click.option(
    "--input_data", type=str, default=None, help="The input data to pass to the prompt."
)
def penny(search, input, input_data):
    """
    A CLI tool for executing prompts from the instructions folder using OpenAI's API.

    Args:
        search (bool): Flag to search for prompts.
        input (str): The name of the prompt to execute.
        input_data (str): The input data to pass to the prompt.
    """
    if not input_data:
        # If no input data is provided via command-line, try to read from stdin
        if not sys.stdin.isatty():
            input_data = sys.stdin.read().strip()
            console.print("Reading input data from stdin...", style="bold yellow")
        else:
            console.print("No input data provided and no data piped.", style="bold red")
            return

    if search:
        # Search for prompts in the instructions folder
        prompts = []
        for file in os.listdir("instructions"):
            if file.endswith(".txt"):
                prompts.append(file)
        if prompts:
            table = Table(title="Available Prompts")
            table.add_column("Prompt Name", style="bold cyan")
            for prompt in prompts:
                table.add_row(prompt)
            console.print(table)
        else:
            console.print(
                "No prompts found in the instructions folder.", style="bold red"
            )
    elif input:
        # Execute the specified prompt
        prompt_file = os.path.join("instructions", f"{input}.txt")
        console.print(f"Looking for prompt file at: {prompt_file}", style="bold yellow")
        if os.path.exists(prompt_file):
            with open(prompt_file, "r") as f:
                prompt_data = f.read()
            # Check if the placeholder {INPUT} is in the prompt data
            if "{INPUT}" in prompt_data:
                if input == "write_doc":
                    input_data = read_data(input_data)
                response = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_data.format(INPUT=input_data),
                        }
                    ],
                    max_tokens=2000,
                )
                console.print("### Response from OpenAI:", style="bold green")
                console.print(Markdown(response.content[0].text), style="purple")
                with open("response.md", "w") as f:
                    f.write(response.content[0].text)
            else:
                console.print(
                    f"Prompt file '{prompt_file}' does not contain the placeholder {{INPUT}}.",
                    style="bold red",
                )
        else:
            console.print(f"Prompt not found: {input}", style="bold red")
    else:
        console.print("Please provide either the -s or -i option.", style="bold yellow")


if __name__ == "__main__":
    penny()
