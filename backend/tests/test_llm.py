from app.core.llm import embed_text


class _FakeEmbeddingData:
    def __init__(self, embedding):
        self.embedding = embedding


class _FakeEmbeddingResponse:
    def __init__(self, embedding):
        self.data = [_FakeEmbeddingData(embedding)]


class _FakeEmbeddings:
    def create(self, **kwargs):
        assert kwargs["model"] == "text-embedding-004"
        assert kwargs["input"] == "a person walks past the counter"
        return _FakeEmbeddingResponse([0.1, 0.2, 0.3])


class _FakeClient:
    embeddings = _FakeEmbeddings()


def test_embed_text_returns_the_embedding_vector():
    result = embed_text("a person walks past the counter", client=_FakeClient())
    assert result == [0.1, 0.2, 0.3]
