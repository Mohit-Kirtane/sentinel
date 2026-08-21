from app.core.llm import chat_complete, embed_text


class _FakeEmbeddings:
    def embed_query(self, text):
        assert text == "a person walks past the counter"
        return [0.1, 0.2, 0.3]


def test_embed_text_returns_the_embedding_vector():
    result = embed_text("a person walks past the counter", embeddings=_FakeEmbeddings())
    assert result == [0.1, 0.2, 0.3]


class _FakeResponse:
    content = "A person walks past the counter carrying a bag."


class _FakeLLM:
    def invoke(self, messages):
        assert messages == [("user", "describe what happens")]
        return _FakeResponse()


def test_chat_complete_returns_the_response_content():
    result = chat_complete([{"role": "user", "content": "describe what happens"}], llm=_FakeLLM())
    assert result == "A person walks past the counter carrying a bag."
