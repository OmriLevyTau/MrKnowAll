from typing import Dict, List

import pinecone
from app.config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX
from app.param_tuning import PINECONE_BATCH_SIZE
from app.models.documents import DocumentVectorChunk, VectorContextQuery
from app.models.query import Query
from app.storage.abstract_vector_storage import AbstractVectorStorage
from pinecone import Index

from app.storage.abstract_vector_storage import  SEP

# Note this values should be pre-configured by us.
# Only thing the client takes care of is maintaining a 
# dedicated Namespace in within this index for
# each user.

if not all([PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX]):
    raise Exception(''' 
            Pinecone connection details not found.
            PINECONE_API_KEY and PINECONE_ENVIRONMENT environment variables must be set.
        ''')

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)


class PineconeVectorStorage(AbstractVectorStorage):

    def __init__(self) -> None:
        self._index = PineconeVectorStorage._get_index()

    @property
    def index(self) -> Index:
        return self._index  # type: ignore

    @staticmethod
    def _get_index():
        if PINECONE_INDEX not in pinecone.list_indexes():
            raise ValueError(f"Pinecone Index does not exists: {PINECONE_INDEX}")
        try:
            index = pinecone.Index(PINECONE_INDEX)
            return index
        except Exception as e:
            print(f"PINECONE: Error in connecting to pinecone index: {PINECONE_INDEX}: " + str(e))

    async def _upload(self, user_id: str, payload: List[DocumentVectorChunk]):
        """
        A method for uploading vectors into pinecone. Vectors will be inserted into the existing
        index, in a dedicated Namespace for that particular user. If such  namespace doesn't exist, 
        it is created implicitly.

        Args:
            user_id (str): uniquely identifies a user.
                           Will be used if namespace will get available again.
                           Meanwhile, it's part of the DocumentVectorChunkMetadata.
            payload (List[DocumentVectorChunk]): see parent class for reference

        Returns:
            str: document_id if successful, otherwise None
        """
        batch_size = PINECONE_BATCH_SIZE
        upserted_count = 0
        for i in range(0, len(payload), batch_size):
            objects_to_insert = []
            for j in range(i, min(i + batch_size, len(payload))):
                doc_vec_chunk = payload[j].dict()
                obj = (
                    doc_vec_chunk.get("vector_id"),
                    doc_vec_chunk.get("embedding"),
                    doc_vec_chunk.get("metadata")
                )
                objects_to_insert.append(obj)
            try:
                upserted_count += self.index.upsert(vectors=objects_to_insert)["upserted_count"]
            except Exception as error:
                print(
                    f"Failed to upsert vectors into pinecone. upserted {upserted_count} out of {len(payload)} vectors: " + str(error))
                raise

        return {"upserted_count": upserted_count}

    async def delete(self, user_id: str, document_id: str) -> Dict:
        """
        Given a user_id and a document_id, delete all vectors
        associated with this user and document.

        Returns:
            Dict: _description_
        """
        try:
            delete_response = self.index.delete(
                filter={
                    "user_id": {"$eq": user_id},
                    "document_id": {"$eq": document_id}
                },
            )
        except Exception as error:
            print(f"Failed to delete {document_id} " + str(error))
            raise

        # TODO: validate which object is delete_response
        return delete_response

    async def _query(self, user_id: str, query: Query):

        top = 3
        if query.top_k:
            top = query.top_k

        try:
            query_response = self.index.query(
                vector=query.embedding,
                top_k=top,
                filter={
                    "user_id": {"$eq": user_id}
                },
                include_metadata=True
            )
        except Exception as error:
            print("Failed to perform query: " + str(error))
            raise
        # TODO: assemble QueryResult from query_response
        return query_response

    async def get_stats(self):
        return self.index.describe_index_stats()

    async def get_context_for_list(self, user_id: str, context_query_list: List[VectorContextQuery]):
        target_vec_ids = []
        window_sizes = []
        docs_ids = []
        ids_windows = []
        for context_query in context_query_list:
            target_vec_id = int(context_query.get_vector_id().split(SEP)[0])
            target_vec_ids.append(target_vec_id)
            window_size = context_query.get_context_window()
            window_sizes.append(window_size)
            doc_id = context_query.get_document_id()
            docs_ids.append(doc_id)
            ids_windows.append([(str(i) + SEP + user_id + SEP + doc_id) for i in
                      range(target_vec_id - window_size, target_vec_id + window_size + 1)])

        flat_ids = [id for sublist in ids_windows for id in sublist]

        try:
            context_response = self.index.fetch(ids=flat_ids)
        except Exception as error:
            print("Failed to fetch ids: " + str(error))
            raise error

        return context_response


    async def get_context(self, user_id: str, context_query: VectorContextQuery):
        """
        refer superclass for details.

        8{~}user_id{~}doc_id
        5-9{~}user_id{~}doc_id

        """

        target_vec_id = int(context_query.get_vector_id().split(SEP)[0])
        window_size = context_query.get_context_window()
        doc_id = context_query.get_document_id()
        ids_window = [(str(i) + SEP + user_id + SEP + doc_id) for i in
                      range(target_vec_id - window_size, target_vec_id + window_size + 1)
                      ]
        try:
            context_response = self.index.fetch(ids=ids_window)
        except Exception as error:
            print("Failed to fetch ids: " + str(error))
            raise error

        return context_response
