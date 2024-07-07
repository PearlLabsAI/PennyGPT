# Penny

## Overview
Penny is a powerful Command Line Interface (CLI) tool for interacting with Large Language Models (LLMs) via OpenAI’s API. The tool allows users to execute predefined prompts stored in the `instructions` folder effortlessly.

**Key Features:**
- Execute prompts from the `instructions` folder.
- Search available prompts.
- Pass input data to prompts via command-line or stdin.

**Technology Stack:**
- Python
- OpenAI API
- Pystray
- Pillow
- Tk
- Pydantic

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
   - [Command-line Options](#command-line-options)
   - [Examples](#examples)
4. [Configuration](#configuration)
5. [Features](#features)
   - [Identify Features](#identify-features)
   - [Describe Features](#describe-features)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](#acknowledgements)
9. [Additional Sections](#additional-sections)

## Installation

**System Requirements:**
- Python 3.11 or higher

**Dependencies:**
- pystray
- Pillow
- tk
- pydantic>=2.7.0,<3.0.0

**Step-by-Step Installation:**
1. Clone the repository:
    ```bash
    git clone https://github.com/jblazick/penny.git
    cd penny
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Command-line Options
- `-s`, `--search`: Search for prompts in the `instructions` folder.
- `-i`, `--input`: Specify the name of the prompt to execute.
- `--input_data`: Provide input data to pass to the prompt.

### Examples

**Search for Prompts:**
```bash
python penny.py -s
```

**Execute a Prompt with Command-Line Input Data:**
```bash
penny -i example_prompt --input_data "Example input data"
```

**Execute a Prompt with Stdin Input Data:**
```bash
echo "Example input data" | penny -i example_prompt
```

## Configuration

### Environment Variables
| Variable Name | Description                 | Default Value |
|---------------|-----------------------------|---------------|
| `LLM_API_KEY` | OpenAI API key for authentication | None            |

**Example Configuration:**
```bash
export LLM_API_KEY="your_openai_api_key"
```

### Configuration Files
Place your configuration settings in a `.env` file in the project root directory:
```
LLM_API_KEY=your_openai_api_key
```

## Features

### Identify Features
- Execute predefined prompts
- Search available prompts
- Input data via CLI or stdin
- Support for environment variables

### Describe Features

#### Execute Prompts
Allows users to run instructions stored in the `instructions` folder.
- **Usage Example:**
    ```bash
    penny -i example_prompt --input_data "Example input data"
    ```
- **Benefit:** Simplifies interactions with LLMs by utilizing predefined prompts.

#### Search Prompts
Facilitates searching within the `instructions` folder.
- **Usage Example:**
    ```bash
    python penny.py -s
    ```
- **Benefit:** Quickly identifies available prompts.
  
## Contributing

**Guidelines:**
- Fork the project and create a new branch for your feature or bug fix.
- Ensure your code follows the existing style code guidelines and passes all tests.
- Submit a pull request and include a detailed description of your changes.

**Setting Up Development Environment:**
1. Clone the repository:
    ```bash
    git clone https://github.com/jblazick/penny.git
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

**Submitting Issues:**
- Open an issue through the GitHub issues page.
- Include steps to reproduce, expected behavior, and screenshots if applicable.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- OpenAI for the API and support.
- Contributors who helped improve the tool.

## Additional Sections

### FAQs
**Q:** Where can I find the `instructions` folder?
**A:** The `instructions` folder is located in the project root directory.

### Troubleshooting
- **Issue:** Cannot find prompts.
  - **Solution:** Ensure the `instructions` folder exists and contains prompt files.

### Roadmap
- Enhance search functionality with more filters.
- Add support for more LLMs.
- Improve user input validation and error handling.

By following these guidelines, this enhanced README aims to be user-friendly, comprehensive, and easy to navigate for users of any skill level.