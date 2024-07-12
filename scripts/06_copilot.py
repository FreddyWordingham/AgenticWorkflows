from pprint import pprint
import os

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from rich.console import Console
from rich.markdown import Markdown

os.environ["OPENAI_API_KEY"] = "asdasda"


def read_file_to_string(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


markdown_path = "./koyo_database/README.md"
concatenated_content = read_file_to_string(markdown_path)


# Grader prompt
code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a coding assistant with expertise in a library that interacts with a database using a KoyoClient object.n
    Here is a the KoyoClient source code:  \n ------- \n  {context} \n ------- \n Answer the user
    question based on the above provided documentation. Ensure any code you provide can be executed \n
    with all required imports and variables defined. Structure your answer with a description of the code solution. \n
    Then list the imports. And finally list the functioning code block. Here is the user question:""",
        ),
        ("placeholder", "{messages}"),
    ]
)


# Data model
class code(BaseModel):
    """Code output"""

    prefix: str = Field(description="Description of the problem and approach")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    description = "Schema for code solutions to questions about LCEL."


llm_model = "gpt-4o"
llm = ChatOpenAI(temperature=0, model=llm_model)
code_gen_chain = code_gen_prompt | llm.with_structured_output(code)


# Test
question = "When was the last message sent?"
solution = code_gen_chain.invoke(
    {"context": concatenated_content, "messages": [("user", question)]}
)


# Format output
output = f"""
{solution.prefix}
```python
{solution.imports}
{solution.code}
```
{solution.description}
"""

# Create a console object for formatting output
console = Console()
console.print(Markdown(output))
