from app.services.embeddings import get_embeddings
import pytest


def test_embeddings():

    sentences = [
        "I love to chat with you!",
        "This tool is really helpful.",
        "Can you provide me with some examples?"
    ]

    embeddings = get_embeddings(sentences)
    assert (len(embeddings) == 3)
    for vec in embeddings:
        assert (len(vec) == 384)
