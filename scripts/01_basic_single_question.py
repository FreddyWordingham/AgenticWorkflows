import argparse

from langchain_community.llms import Ollama
from rich.console import Console
from rich.markdown import Markdown


def parse_arguments():
    parser = argparse.ArgumentParser(description="Chat with an LLM model")
    parser.add_argument("model", type=str, help="The name of the model to use")
    parser.add_argument("question", type=str, help="The question to ask the model")
    args = parser.parse_args()
    return args.model, args.question


def chat_with(llm, prompt):
    return llm.invoke(prompt)


if __name__ == "__main__":
    # Read command line arguments
    model, question = parse_arguments()

    # Create a console object for formatting output
    console = Console()

    # Run the query
    llm = Ollama(model=model)
    response = chat_with(llm, question)

    # Print the response
    console.print(Markdown(response))
