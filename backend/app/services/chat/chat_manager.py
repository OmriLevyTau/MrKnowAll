from typing import Dict, List, Tuple, Set

from app.models.query import Query
from app.param_tuning import MAX_NUM_OF_CHARS_IN_QUERY, MAX_NUM_OF_CHARS_IN_QUESTION, MAX_NUM_OF_WORDS_IN_QUERY
from app.storage.chat_history_db import ChatHistoryManager
from app.models.documents import VectorContextQuery
from app.param_tuning import SCORE_THRESHOLD
from app.storage.abstract_vector_storage import SEP


# create a connection to the local DB for saving the chat history
chat_history_manager = ChatHistoryManager("chat_history.db")
ASSISTANT = "assistant"
USER = "user"


def validate_query(query_request: Query) -> bool:
    """
    Validates a given Query to AI assistant in terms of its length and
    number of words.
    """
    query_content = query_request.get_query_content()
    words_num = len(query_content.split(" "))
    chars_num = len(query_content)

    if words_num > MAX_NUM_OF_WORDS_IN_QUERY or chars_num > MAX_NUM_OF_CHARS_IN_QUESTION:
        return False

    return True


def get_history_for_chat(user_id: str, query: Query) -> List[Tuple[str, str]]:
    """
    Given a user_id and a Query, get the short-term history of the chat.
    That is the last messages of the user and the system, adhering to the
    length restriction.

    :param user_id: str
    :param query: valid Query object
    :return: [("user", "q2"), ("assistant", "a2"), ("user", "q1"),("assistant", "a1")]
    """

    query_content = query.query_content
    query_content_len = len(query_content)

    # get the last 6 questions and answers
    history_rows, num_of_rows = chat_history_manager.get_user_messages_with_answers(
        user_id=user_id)

    # if this is the first time there is no history
    if num_of_rows < 1:
        return []

    returned_history_list = []

    used_characters = 0
    index = 0
    remained_chars_length = MAX_NUM_OF_CHARS_IN_QUERY - query_content_len
    # in the loop we add history messages only if the entire message we send to openAI API is less then 4096 chars
    while ((index < num_of_rows) and
           (remained_chars_length - used_characters -
            len(history_rows[index][0]) - len(history_rows[index][1])) >= 0):
        q, a = history_rows[index]
        returned_history_list.append((ASSISTANT, a))
        returned_history_list.append((USER, q))
        used_characters += len(q) + len(a)
        index = index + 1

    return returned_history_list[::-1]


def compose_context_response(map_doc_id_to_context: Dict[str, Dict[str, str]]):
    """
    :param map_doc_id_to_context: {doc1: {vec1: "vec1 content", vec2: "vec1 content"},...}
    :return: {doc1: "context of doc 1", ...}
    """

    result = dict()
    for doc_id, context_dict in map_doc_id_to_context.items():
        doc_sentences = [sentence for vec_id,
                         sentence in map_doc_id_to_context[doc_id].items()]
        doc_context = "\n".join(doc_sentences)
        result[doc_id] = doc_context
    return result

# TODO: add type hint of top_k_closest_vectors


def build_context_objects_for_top_k_closest_vectors(user_id: str, vectors) -> Tuple[Set, List[VectorContextQuery]]:
    """
        given vectors, build and return a list of VectorContextQuery and a unique set of the relevant references.

        :param user_id:
        :param vectors:

        :return: Tuple[Set,List[VectorContextQuery]]
        """
    references = set()
    context_query_list = []
    for vector_data in vectors:
        # every vector has its own context
        cur_vec_doc_id = vector_data.get('metadata').get('document_id')
        cur_vec_score = vector_data.get('score')
        # get context only for sentences that are relevant to the question
        if (cur_vec_score >= SCORE_THRESHOLD):
            references.add(cur_vec_doc_id)
            context_query = VectorContextQuery(
                user_id=user_id, document_id=cur_vec_doc_id, vector_id=vector_data.get(
                    'id')
            )
            context_query_list.append(context_query)

    return references, context_query_list

# TODO: add type hint of vectors


def extract_context_from_context_vectors(vectors) -> Dict[str, Dict[str, str]]:
    """
        given vectors, build and return a mapping from document_id to another mapping, from vector_id to it's content.

        :param vectors:

        :return: Dict[str, Dict[str, str]]
    """
    map_vec_id_to_context = {}
    map_doc_id_to_context = {}

    # we map every vector we have to all of its context sentences, and then we save this mapping inside another
    # map, from the document id to all the (context) vectors it has for this query.
    for i, key in enumerate(vectors):
        # vec is a key to dict
        res = vectors.get(key)
        vec_id = res.get("id").split(SEP)[0]
        context = res.get("metadata").get("original_content")
        map_vec_id_to_context[vec_id] = context
        cur_vec_doc_id = res.get("metadata").get("document_id")

        if cur_vec_doc_id not in map_doc_id_to_context:
            map_doc_id_to_context[cur_vec_doc_id] = map_vec_id_to_context
        else:
            map_doc_id_to_context[cur_vec_doc_id].update(
                map_vec_id_to_context)

    return map_doc_id_to_context


def build_all_context(doc_ids: List[str], map_doc_id_to_context: Dict[str, Dict[str, str]]) -> str:
    # for each document, we get the context of all the vectors that belongs to that document
    all_context = ""
    for doc_id in doc_ids:
        all_context = all_context + \
            "\nThe following context is coming from the document: " + doc_id + '\n'
        cur_doc_id_dict = map_doc_id_to_context[doc_id]

        vec_ids = list(cur_doc_id_dict)

        vec_ids.sort()
        for vec_id in vec_ids:
            all_context = all_context + cur_doc_id_dict[vec_id]
            all_context = all_context + "\n"

    return all_context
