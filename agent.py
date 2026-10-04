from agent_graph import graph


# =========================================================
# CONVERSATION CONFIG
# =========================================================

config = {
    "configurable": {
        "thread_id": "personal_assistant"
    }
}


# =========================================================
# TERMINAL CHAT
# =========================================================

while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    result = graph.invoke(
        {
            "messages": [
                ("user", user_input)
            ]
        },
        config=config
    )

    final_message = result["messages"][-1]

    print("\nAgent:")

    if isinstance(final_message.content, list):

        for block in final_message.content:

            if isinstance(block, dict) and block.get("type") == "text":
                print(block["text"])

    else:
        print(final_message.content)