from langgraph.graph import (
    StateGraph,
    END
)

from app.rag.state import GraphState
from app.rag.nodes import (
    retrieve,
    generate
)


builder = StateGraph(
    GraphState
)

builder.add_node(
    "retrieve",
    retrieve
)

builder.add_node(
    "generate",
    generate
)

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

graph = builder.compile()