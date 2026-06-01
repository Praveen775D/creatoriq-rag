from langgraph.graph import (
    StateGraph,
    END
)

from langgraph.checkpoint.memory import (
    MemorySaver
)

from app.rag.state import GraphState
from app.rag.nodes import (
    retrieve,
    generate
)


builder = StateGraph(GraphState)

# Nodes
builder.add_node(
    "retrieve",
    retrieve
)

builder.add_node(
    "generate",
    generate
)

# Flow
builder.set_entry_point(
    "retrieve"
)

builder.add_edge(
    "retrieve",
    "generate"
)

builder.add_edge(
    "generate",
    END
)

# Memory for multi-turn conversations
memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)