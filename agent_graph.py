import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver

from gmail_tools import (
    get_latest_emails,
    search_emails,
    read_email
)


# =========================================================
# LOAD ENV
# =========================================================

load_dotenv()


# =========================================================
# LLM
# =========================================================



llm = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# =========================================================
# TOOLS
# =========================================================

tools = [
    get_latest_emails,
    search_emails,
    read_email
]

llm_with_tools = llm.bind_tools(tools)


# =========================================================
# AGENT NODE
# =========================================================

def agent_node(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# =========================================================
# BUILD GRAPH
# =========================================================

builder = StateGraph(MessagesState)

builder.add_node(
    "agent",
    agent_node
)

builder.add_node(
    "tools",
    ToolNode(tools)
)

builder.add_edge(
    START,
    "agent"
)

builder.add_conditional_edges(
    "agent",
    tools_condition
)

builder.add_edge(
    "tools",
    "agent"
)


# =========================================================
# SHORT-TERM MEMORY
# =========================================================

memory = InMemorySaver()

graph = builder.compile(
    checkpointer=memory
)