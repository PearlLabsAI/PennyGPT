import click
import os
import sys
import openai
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown


client = openai.OpenAI()
console = Console()


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
        print(f"prompts: {prompts}")
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
        console.print(
            f"Looking for prompt file at: {prompt_file}", style="bold yellow"
        )  # Debug output
        if os.path.exists(prompt_file):
            with open(prompt_file, "r") as f:
                prompt_data = f.read()
            console.print(
                f"## Executing prompt: {input} with input data:", style="bold blue"
            )
            console.print(f"{input_data}", style="italic")
            # Execute the prompt with the provided input data using OpenAI's API
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": prompt_data.format(INPUT=input_data),
                    }
                ],
                max_tokens=2000,
            )
            console.print("### Response from OpenAI:", style="bold green")
            console.print(Markdown(response.choices[0].message.content))
        else:
            console.print(f"Prompt not found: {input}", style="bold red")
    else:
        console.print("Please provide either the -s or -i option.", style="bold yellow")


if __name__ == "__main__":
    penny()
