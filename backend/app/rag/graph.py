from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.rag.state import GraphState
from app.rag.nodes import retrieve, analyze, generate


builder = StateGraph(GraphState)

# ---------------- NODES ----------------
builder.add_node("retrieve", retrieve)
builder.add_node("analyze", analyze)
builder.add_node("generate", generate)

# ---------------- FLOW ----------------
builder.set_entry_point("retrieve")

builder.add_edge("retrieve", "analyze")
builder.add_edge("analyze", "generate")
builder.add_edge("generate", END)

# ---------------- MEMORY ----------------
memory = MemorySaver()

graph = builder.compile(checkpointer=memory)