from app.db.models import Segment

NO_MATCH_ANSWER = "Nothing in this video matches your question."

SYSTEM_PROMPT = (
    "You are answering questions about a security-camera video using only the "
    "timestamped scene descriptions provided below. Cite what you see plainly; "
    "do not invent details that aren't in the descriptions."
)


def build_answer(question: str, segments: list[Segment], chat_fn) -> dict:
    if not segments:
        return {"answer": NO_MATCH_ANSWER, "citations": []}

    context = "\n".join(f"[{s.start_ts}-{s.end_ts}s] {s.description}" for s in segments)
    prompt = f"{SYSTEM_PROMPT}\n\nScene descriptions:\n{context}\n\nQuestion: {question}"

    answer = chat_fn([{"role": "user", "content": prompt}])

    return {
        "answer": answer,
        "citations": [
            {"start_ts": float(s.start_ts), "end_ts": float(s.end_ts)} for s in segments
        ],
    }
