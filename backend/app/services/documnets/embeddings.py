from typing import List

from sentence_transformers import SentenceTransformer
from app.param_tuning import EMBEDDING_MODEL, ENABLE_EMBEDDING_MULTIPROC

MAX_SEQ = 128
"""
    model will be initialized and loaded with the SentenceTransformer model only once, 
    upon the first import or execution of this code. 
    Subsequent calls to the get_embeddings function will reuse the already initialized model
"""
model = SentenceTransformer(EMBEDDING_MODEL)
model.max_seq_length = 128


def get_embeddings(sentences: List[str]) -> List[List[float]]:
    embeddings = model.encode(sentences)
    embeddings = [tensor.tolist() for tensor in embeddings]

    return embeddings
