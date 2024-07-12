from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_community.llms import Ollama
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[List, add_messages]


def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


if __name__ == "__main__":

    # Model
    llm = Ollama(model="phi3")

    # Graph
    graph_builder = StateGraph(State)

    graph_builder.add_node("chatbot", chatbot)

    graph_builder.set_entry_point("chatbot")
    graph_builder.set_finish_point("chatbot")

    graph = graph_builder.compile()

    # Run
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        for event in graph.stream({"messages": ("user", user_input)}):
            for value in event.values():
                print("Assistant:", value["messages"][-1])
