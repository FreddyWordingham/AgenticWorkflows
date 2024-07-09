from typing import Tuple
import argparse

from langchain_community.llms import Ollama
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
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


if __name__ == "__main__":
    # Read command line arguments
    model, question = parse_arguments()

    # Create a console object for formatting output
    console = Console()

    # Template
    template_1 = """{question}"""
    prompt_template_1 = PromptTemplate(
        template=template_1, input_variables=["question"]
    )

    template_2 = """
    First, analyse the reply: "{answer}" to the question: "{question}".
    Then, give me a rating out of five for how well the reply answers the question.
    Only use whole numbers, and do not include any other text or information in your reply.
    For example, return "3" if you think the reply is a 3 out of 5.
    """
    prompt_template_2 = PromptTemplate(
        template=template_2, input_variables=["question", "answer"]
    )

    # Model
    llm = Ollama(model=model)

    # # Chain
    chain_1 = (
        prompt_template_1
        | llm
        | {"answer": StrOutputParser(), "question": StrOutputParser()}
    )
    chain_2 = prompt_template_2 | llm | {"rating": StrOutputParser()}
    chain = chain_1 | chain_2

    # Run the query
    response = chain.invoke({"question": question})

    from pprint import pprint

    pprint(response)

    # # Print the response
    # console.print(Markdown(response.get("answer")))
    # console.print(Markdown(response.get("rating")))
