# Agentic Workflows

Experimenting with agentic LLM workflows.

## Requirements

We'll use Ollama to retrieve and run the LLM models locally.
To install Ollama, visit https://ollama.com/ and follow the instructions.

To start the Ollama server, run the following command:

```bash
ollama run <model>
```

> For example, to run the `phi3` model, run `ollama run phi3`.

## Installation

Clone this repository, and set the current working directory to the root of the repository:

```bash
git clone https://github.com/FreddyWordingham/AgenticWorkflows.git
cd AgenticWorkflows
```

Then, use `Poetry` to install the required dependencies:

```bash
poetry env use python3.10
poetry install
```

## Usage

In one terminal, start a local model running:

```bash
ollama run <model>
```

Then, in another terminal, run the desired workflow passing the name of the model you selected in the last step:

```bash
poetry run python scripts/<workflow>.py --model <model>
```

> For example: `poetry run python scripts/chatbot.py --model phi3`.
