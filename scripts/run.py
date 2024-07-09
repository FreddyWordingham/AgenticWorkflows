from pprint import pprint

from langchain_community.llms import Ollama


def chat_with(llm, prompt):
    return llm.invoke(prompt)


if __name__ == "__main__":
    print("Hello, world!")
    phi3_llm = Ollama(model="phi3")
    response = chat_with(phi3_llm, "tell me a joke")
    pprint(response)
