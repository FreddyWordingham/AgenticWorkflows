from typing import Annotated, List, TypedDict
from typing_extensions import TypedDict

from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFacePipeline

# from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint import MemorySaver
from langgraph.graph import END, StateGraph, MessagesState
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_huggingface import ChatHuggingFace


# Tools
@tool
def search(query: str):
    """
    Look up the weather for a given location.
    """

    if "sf" in query.lower() or "san francisco" in query.lower():
        return ["It's 60 degrees and foggy."]
    return ["It's 90 degrees and sunny."]


if __name__ == "__main__":

    tools = [search]
    tool_node = ToolNode(tools)

    llm = HuggingFacePipeline.from_model_id(
        model_id="microsoft/Phi-3-mini-4k-instruct",
        task="text-generation",
        pipeline_kwargs=dict(
            max_new_tokens=512,
            do_sample=False,
            repetition_penalty=1.03,
        ),
    )
    chat_model = ChatHuggingFace(llm=llm).bind_tools(tools)

# Create a
