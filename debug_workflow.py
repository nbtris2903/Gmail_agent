from agent_graph import graph
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage


config = {
    "configurable": {
        "thread_id": "debug_session"
    }
}


while True:

    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    print("\n========== WORKFLOW ==========\n")

    previous_count = 0

    for state in graph.stream(
        {
            "messages": [
                ("user", user_input)
            ]
        },
        config=config,
        stream_mode="values"
    ):

        messages = state["messages"]

        # Chỉ hiển thị những message mới xuất hiện
        new_messages = messages[previous_count:]
        previous_count = len(messages)

        for message in new_messages:

            # ==========================================
            # USER MESSAGE
            # ==========================================

            if isinstance(message, HumanMessage):

                print("[USER]")
                print(message.content)
                print()

            # ==========================================
            # TOOL RESULT
            # ==========================================

            elif isinstance(message, ToolMessage):

                print("[TOOL RESULT]")
                print(f"Tool: {message.name}")

                # Không in toàn bộ body vì có thể rất dài
                content = str(message.content)

                if len(content) > 500:
                    content = content[:500] + "... [truncated]"

                print(content)
                print()

            # ==========================================
            # AGENT MESSAGE
            # ==========================================

            elif isinstance(message, AIMessage):

                # Agent đang yêu cầu gọi tool
                if message.tool_calls:

                    for tool_call in message.tool_calls:

                        print("[AGENT → TOOL]")
                        print(f"Tool: {tool_call['name']}")
                        print(f"Arguments: {tool_call['args']}")
                        print()

                # Agent trả lời cuối cùng
                elif message.content:

                    print("[AGENT FINAL]")

                    if isinstance(message.content, list):

                        for block in message.content:

                            if (
                                isinstance(block, dict)
                                and block.get("type") == "text"
                            ):
                                print(block["text"])

                    else:
                        print(message.content)

                    print()

    print("==============================")