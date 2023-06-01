
'''
    This class tests basic funcionaliy of pinecone vector database.
    As in their free plan, there's no way to create a multipile indices
    or namespaces, tests will run agains the production collection (!).
    As a consequence:
    - tests will be lean and test only critical behaviour
    - it'll be an "integration tests" in a sense they'll
      test some broader functionlaity then a unit test.
    - as a convention each vector inserted will have as a metadata:
      {"user_id": "test", "document_id": "test"} (among the others) 
'''
from typing import Generator, List

import numpy as np
import pytest

from app.models.documents import (DocumentMetaData, DocumentVectorChunk,
                                  VectorContextQuery)
from app.models.query import Query
from app.services.embeddings import get_embeddings
from app.storage.abstract_vector_storage import AbstractVectorStorage
from app.storage.vector_storage_providers.pinecone import PineconeVectorStorage

TARGET_SENTENCE = "Object-oriented programming allows for modular and efficient code development."
TARGET_EQUIVALENT_SENTENCE = "The use of object-oriented programming enables the development of code that is both interchangeable and effective"
MASKING_SENTENCES = [
    "Photography enthusiasts capture beautiful moments with their cameras",
    "The ocean waves crash against the sandy shore, creating a soothing sound",
    "Gardening requires patience and a green thumb to cultivate vibrant flowers",
    "In the world of fashion, designers create unique and stylish clothing",
    "Exploring new hiking trails can be a great way to connect with nature",
    "Music festivals bring together artists and fans for unforgettable performances",
    "Cooking delicious meals is an art form that requires creativity and skill",
    "The history of ancient civilizations fascinates archaeologists and historians",
    "Sports enthusiasts enjoy the thrill of competition and physical exertion",
    "Traveling to exotic destinations allows for cultural exploration and adventure"
    ]

GENERIC_SENTENCE = "Hi, I will assit you to test your vectorDB and I'm number "
CONTEXT_SENTNCES = [GENERIC_SENTENCE + str(i) for i in range(10)]

TEST_USER_ID = "test"
TEST_DOCUMENT_ID = "test"
TEST_DOCUMENT_METADATA = DocumentMetaData(user_id=TEST_USER_ID, document_id=TEST_DOCUMENT_ID)


@pytest.fixture
def pinecone_client() -> Generator[PineconeVectorStorage, None, None]:
    # Generator[YieldType, SendType, ReturnType]
    # type of values that can be sent into the generator
    # generator does not explicitly return any value
    connection = PineconeVectorStorage()
    yield connection

def clear_all(client) -> None:
    delete_response = client.index.delete(
        filter={
            "user_id": {"$eq": TEST_USER_ID},
        }
    )

def get_payload(
        sentences: List[str], 
        user_id=TEST_USER_ID, 
        doc_metadata=TEST_DOCUMENT_METADATA
        ) -> List[DocumentVectorChunk]:
    embeddings = get_embeddings(sentences)
    payload = AbstractVectorStorage.assemble_documents_vector_chunks(
        user_id=user_id, doc_metadata=doc_metadata,
        text_chunks=sentences, embeddings=embeddings
    )
    return payload


@pytest.fixture(autouse=True)
def setup_and_teardown(pinecone_client):
    '''
    Validates that no test data stored in the vector database. 
    '''
    # Will run before each test
    # save number of existing vectors
    # index.describe_index_stats()
    clear_all(pinecone_client)
    # test will run at this point
    yield
    # will run after the test
    clear_all(pinecone_client)
    # assert number of existing vectors.


@pytest.mark.asyncio
async def test_should_get_target_sentence(pinecone_client) -> None:
    '''
    in this test one "target sentence" and 10 different
    "masking sentences" are uploaded. This 10 "masking" sentences are 
    not realted to the target in any form.
    
    Then, it queries the database for a sentence it hasn't seen before
    which is semantically similar to the target sentence. Expectation is
    to be able to get the origianl target sentence as the top match and
    with a "high" score.
    '''
    # upload target setence and masking sentences
    text_chunks = MASKING_SENTENCES + [TARGET_SENTENCE]
    payload = get_payload(sentences=text_chunks)

    try:
        upload_response = await pinecone_client._upload(TEST_USER_ID, payload)
        assert upload_response is not None and upload_response.get("upserted_count") == len(text_chunks)

        # query target equivalent sentence
        query = Query(user_id=TEST_USER_ID, top_k=10 ,query_id=0, query_content=TARGET_EQUIVALENT_SENTENCE)
        query_response = await pinecone_client.query(user_id=TEST_USER_ID, query=query)

        assert (query_response is not None)
        matches = query_response.get("matches")
        assert len(matches)>0

        # validates some basic properties
        top_match = matches[0]
        assert top_match.get('id') == '10'+"@"+TEST_DOCUMENT_ID # as it was inserted last
        assert top_match.get('metadata').get('document_id') == 'test' # sanity check
        assert top_match.get('metadata').get('original_content') == TARGET_SENTENCE
        # Should be similar!
        assert (1-top_match.get('score')) < 0.5
    
    except Exception as error:
        print("Error in test: " + str(error))
        raise


@pytest.mark.asyncio
async def test_should_not_get_similar_sentences(pinecone_client) -> None:
    '''
    Similar to the previous test, but this time the target sentence
    is not uploaded. Expectation is that the top match will be 
    very different and with a "small" score.
    '''
    # upload target setence and masking sentences
    text_chunks = MASKING_SENTENCES
    payload = get_payload(sentences=text_chunks)

    try:
        upload_response = await pinecone_client._upload(TEST_USER_ID, payload)
        assert upload_response is not None and upload_response.get("upserted_count") == len(text_chunks)

        # query target equivalent sentence
        query = Query(user_id=TEST_USER_ID, top_k=10 ,query_id=0, query_content=TARGET_EQUIVALENT_SENTENCE)
        query_response = await pinecone_client.query(user_id=TEST_USER_ID, query=query)

        assert (query_response is not None)
        matches = query_response.get("matches")
        assert len(matches)>0

        top_match = matches[0]
        # should be different!
        assert (1-top_match.get('score')) > 0.5
    
    except Exception as error:
        print("Error in test: " + str(error))
        raise

@pytest.mark.asyncio
async def test_get_vector_context(pinecone_client) -> None:
    text_chunks = CONTEXT_SENTNCES
    payload = get_payload(sentences=text_chunks)
    try:
        # populate DB
        upload_response = await pinecone_client._upload(TEST_USER_ID, payload)
        assert upload_response is not None and upload_response.get("upserted_count") == len(text_chunks)

        # Try to query vector number 3 with default windows size of 2.
        expected_ids =  [str(j)+"@"+TEST_DOCUMENT_ID for j in range(1,6) if j != 3]
        context_query = VectorContextQuery(
            user_id=TEST_USER_ID,
            document_id=TEST_DOCUMENT_ID,
            vector_id="3"+"@"+TEST_DOCUMENT_ID
        )

        context_response = await pinecone_client.get_context(
            user_id=TEST_USER_ID,
            context_query=context_query
        )

        assert ((context_response is not None) and (context_response.get("vectors") is not None))
        vectors = context_response.get("vectors")
        assert (len(vectors)==4)

        for i,key in enumerate(vectors):
            # vec is a key to dict
            assert (key in expected_ids)
            res = vectors.get(key)
            assert(
                    (res is not None) and 
                    (res.get("metadata") is not None) and
                    (res.get("metadata").get("original_content") is not None)
                )
            context = res.get("metadata").get("original_content")
            assert context == CONTEXT_SENTNCES[int(key.split("@")[0])]
    
    except Exception as error:
        print("Error in test: " + str(error))
        raise


@pytest.mark.asyncio
async def test_batch_upload(pinecone_client):
    n = 310
    text_chunks = [GENERIC_SENTENCE+str(i) for i in range(n)]
    payload = get_payload(sentences=text_chunks)
    try:
        upload_response = await pinecone_client._upload(TEST_USER_ID, payload)
        assert (upload_response is not None) and (upload_response.get("upserted_count") == n)

        stats = await pinecone_client.get_stats()
        assert (stats is not None) and (stats["total_vector_count"] == n) 

    except Exception as error:
        print("Error in test: " + str(error))
        raise


@pytest.mark.asyncio
async def test_upload_multipile_documnets(pinecone_client):
    vec_n = 10
    doc_n = 10
    text_chunks = [
        [GENERIC_SENTENCE+str(i) for i in range(vec_n)]
        for j in range(doc_n)
    ]
    documents_metadata = [
        DocumentMetaData(
            user_id=TEST_USER_ID, 
            document_id=TEST_DOCUMENT_ID+"-"+str(i)
        ) for i in range(doc_n)
    ]

    payloads = [
        get_payload(text_chunks[i], 
                    user_id=TEST_USER_ID, 
                    doc_metadata=documents_metadata[i]
        ) for i in range(doc_n)
    ]

    try:
        for i in range(doc_n):
            upload_response = await pinecone_client._upload(TEST_USER_ID, payloads[i])
            assert (upload_response is not None) and (upload_response.get("upserted_count") == vec_n)
    except Exception as error:
        raise

    
    stats = await pinecone_client.get_stats()
    assert (stats is not None) and (stats["total_vector_count"] == doc_n*vec_n) 

    # validate there is distiction between documnets

    try:
        delete_response = await pinecone_client.delete(
            user_id=TEST_USER_ID, 
            document_id=documents_metadata[-1].get_document_id()
        )
    except Exception as error:
        raise

    stats = await pinecone_client.get_stats()
    assert (stats is not None) and (stats["total_vector_count"] == (doc_n-1)*vec_n)
