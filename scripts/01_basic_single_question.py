from typing import Tuple
import argparse

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from rich.console import Console
from rich.markdown import Markdown
from typeguard import typechecked


@typechecked
def parse_arguments() -> Tuple[str, str]:
    parser = argparse.ArgumentParser(description="Chat with an LLM model")
    parser.add_argument("model", type=str, help="The name of the model to use")
    parser.add_argument("question", type=str, help="The question to ask the model")
    args = parser.parse_args()
    return args.model, args.question


@typechecked
def chat_with(llm: Ollama, prompt: str) -> str:
    return llm.invoke(prompt)


if __name__ == "__main__":
    # Read command line arguments
    model, question = parse_arguments()

    # Create a console object for formatting output
    console = Console()

    # Define a template for the prompt
    template = """{question}"""
    prompt_template = PromptTemplate(template=template, input_variables=["question"])

    # Run the query
    llm = Ollama(model=model)
    prompt = prompt_template.format(question=question)
    response = chat_with(llm, prompt)

    # Print the response
    console.print(Markdown(response))
