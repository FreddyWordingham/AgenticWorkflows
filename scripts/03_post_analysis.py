from operator import itemgetter
from typing import Tuple
import argparse

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
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

    # Model
    llm = Ollama(model=model)

    # Chains
    template_1 = """
    Answer the following question as briefly as possible:
    Question: {question}
    Answer:
    """
    prompt_template_1 = PromptTemplate(template=template_1, input_variables=["question"])
    chain_1 = prompt_template_1 | llm | StrOutputParser()

    template_2 = """
    First, analyse the reply: "{answer}" to the question: "{question}".
    Then, give me a rating out of five for how well the reply answers the question,
    consider only how scientifically accurate the reply is.
    Give only the numerical value, like "2/5" or "5/5".
    GIVE NO OTHER INFORMATION, CONTEXT OR EXPLANATION!
    Rating:
    """
    prompt_template_2 = PromptTemplate(template=template_2, input_variables=["question", "answer"])
    chain_2 = prompt_template_2 | llm | StrOutputParser()

    # Sequential Chain
    chain = {
        "question": itemgetter("question"),
        "answer": chain_1,
    } | RunnablePassthrough.assign(rating=chain_2)

    # Run
    result = chain.invoke({"question": question})

    # Format the results into the final output
    output = f"""
Q: {result.get("question")}

A: {result.get("answer")}

Rating: {result.get("rating")}
"""

    # Create a console object for formatting output
    console = Console()
    console.print(Markdown(output))