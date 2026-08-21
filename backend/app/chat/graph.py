from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.chat.answer import NO_MATCH_ANSWER, build_answer
from app.chat.retrieval import retrieve_segments
from app.db.models import Segment


class ChatState(TypedDict):
    video_id: str
    question: str
    segments: list[Segment]
    answer: str
    citations: list[dict]


def build_chat_graph(repo, embed_fn, chat_fn, k: int, similarity_threshold: float):
    def retrieve_node(state: ChatState) -> dict:
        segments = retrieve_segments(
            state["video_id"],
            state["question"],
            repo=repo,
            embed_fn=embed_fn,
            k=k,
            similarity_threshold=similarity_threshold,
        )
        return {"segments": segments}

    def should_generate(state: ChatState) -> str:
        return "generate" if state["segments"] else "no_match"

    def generate_node(state: ChatState) -> dict:
        result = build_answer(state["question"], state["segments"], chat_fn=chat_fn)
        return {"answer": result["answer"], "citations": result["citations"]}

    def no_match_node(state: ChatState) -> dict:
        return {"answer": NO_MATCH_ANSWER, "citations": []}

    graph = StateGraph(ChatState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("generate", generate_node)
    graph.add_node("no_match", no_match_node)

    graph.set_entry_point("retrieve")
    graph.add_conditional_edges(
        "retrieve", should_generate, {"generate": "generate", "no_match": "no_match"}
    )
    graph.add_edge("generate", END)
    graph.add_edge("no_match", END)

    return graph.compile()
