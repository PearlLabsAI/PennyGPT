# Penny

Penny is a CLI tool for working with Large Language Models (LLMs) using OpenAI's API. It allows users to execute predefined prompts stored in the `instructions` folder.

## Features

- Execute prompts from the `instructions` folder.
- Search for available prompts.
- Pass input data to prompts via command-line or stdin.

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

### Command-line Options

- `-s`, `--search`: Search for prompts in the `instructions` folder.
- `-i`, `--input`: The name of the prompt to execute.
- `--input_data`: The input data to pass to the prompt.

### Examples

#### Search for Prompts

To search for prompts in the `instructions` folder, use the `-s` or `--search` flag:

```
python penny.py -s
```

#### Execute a Prompt

```bash
penny -i example_prompt --input_data "Example input data"
```

You can also pass input data via stdin:

```bash
echo "Example input data" | penny -i example_prompt
```

## Project Structure

- `src/`: Contains the main source code for the CLI tool.
- `instructions/`: Contains the prompt files.
- `penny.egg-info/`: Contains metadata about the project.
- `requirements.txt`: Lists the dependencies required for the project.
- `setup.py`: Script for setting up the project.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

Joseph Blazick - [joe.blazick@yahoo.com](mailto:joe.blazick@yahoo.com)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
