from agent import react_search_agent

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

if __name__ == "__main__":
    messages = [
        "Je veux faire le résumé du repo Projet-AL2023 de ohamjoseph sur le période du 2023-04-07 au 2023-04-14"
    ]

    print_stream(react_search_agent.stream({"messages": messages}, stream_mode="values"))
    # result = react_search_agent.invoke({"messages": messages})
    # print(result["messages"][-1].content)
