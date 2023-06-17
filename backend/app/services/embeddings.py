from typing import List

from sentence_transformers import SentenceTransformer

from logging import getLogger
from time import time,perf_counter

MAX_SEQ = 128
"""
    model will be initialized and loaded with the SentenceTransformer model only once, 
    upon the first import or execution of this code. 
    Subsequent calls to the get_embeddings function will reuse the already initialized model
"""
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model.max_seq_length = 128

timer = perf_counter
Logger = getLogger(__name__)


def get_embeddings(sentences: List[str], log:bool = False) -> List[List[float]]:
    start_time = timer()
    embeddings = model.encode(sentences)
    embeddings =  [tensor.tolist() for tensor in embeddings]
    elapsed_time = timer()-start_time
    if log:
        Logger.debug("transforming %i sentences to vectors took %f seconds",len(sentences),elapsed_time)
    return embeddings
