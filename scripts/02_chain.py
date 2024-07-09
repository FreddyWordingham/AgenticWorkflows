from operator import itemgetter
import argparse

from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from rich.console import Console
from rich.markdown import Markdown
from typeguard import typechecked


@typechecked
def parse_arguments() -> str:
    parser = argparse.ArgumentParser(description="Chat with an LLM model")
    parser.add_argument("model", type=str, help="The name of the model to use")
    args = parser.parse_args()
    return args.model


if __name__ == "__main__":
    # Read command line arguments
    model = parse_arguments()

    # Model
    llm = Ollama(model=model)

    # Chains
    template_1 = """
    How much is {a} + {b}?
    Answer with only the result of the sum, written in numerical form, without any padding.
    Result:
    """
    prompt_template_1 = PromptTemplate(template=template_1, input_variables=["a", "b"])
    chain_1 = prompt_template_1 | llm | StrOutputParser()

    template_2 = """
    How much is {a} multiplied by {c}?
    Answer with only the result of the sum, written in numerical form, without any padding.
    Result:
    """
    prompt_template_2 = PromptTemplate(template=template_2, input_variables=["a", "c"])
    chain_2 = prompt_template_2 | llm | StrOutputParser()

    # Sequential chain
    chain = {
        "a": itemgetter("a"),
        "b": itemgetter("b"),
        "c": chain_1,
    } | RunnablePassthrough.assign(d=chain_2)

    # Run
    result = chain.invoke({"a": 2, "b": 3})

    # Format results into final output
    output = f"""# Values
| variable | value |
| -------- | ----- |
| a | {result.get("a")} |
| b | {result.get("b")} |
| c | {result.get("c")} |
| d | {result.get("d")} |

# Results
{result.get("a")} + {result.get("b")} = {result.get("c")}

{result.get("a")} * {result.get("c")} = {result.get("d")}"""

    # Create a console object for formatting output
    console = Console()
    console.print(Markdown(output))
