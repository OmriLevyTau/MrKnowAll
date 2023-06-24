from typing import Dict, List

from app.models.query import Query
from app.param_tuning import MAX_NUM_OF_CHARS_IN_QUERY, MAX_NUM_OF_CHARS_IN_QUESTION, MAX_NUM_OF_WORDS_IN_QUERY
from app.storage.chat_history_db import ChatHistoryManager

# create a connection to the local DB for saving the chat history
chat_history_manager = ChatHistoryManager("chat_history.db")
ASSISTANT = "assistant"
USER = "user"


def validate_query(query_request: Query) -> bool:
    '''
    Validates a given Query to AI assistant in terms of its length and
    number of words.
    '''
    query_content = query_request.get_query_content()
    words_num = len(query_content.split(" "))
    chars_num = len(query_content)

    if words_num > MAX_NUM_OF_WORDS_IN_QUERY or chars_num > MAX_NUM_OF_CHARS_IN_QUESTION:
        return False

    return True


def get_history_for_chat(user_id: str, query: Query) -> List:
    '''
    Given a user_id and a Query, get the short-term history of the chat.
    That is the last messages of the user and the system, adhering to the
    length restriction.
    '''
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
    '''
    Arguments:
        map_doc_id_to_context: {doc1: {vec1: "vec1 content", vec2: "vec1 content"},...}
    Returns:
        {doc1: "context of doc 1", ...}
    '''
    result = dict()
    for doc_id, context_dict in map_doc_id_to_context.items():
        doc_sentences = [sentence for vec_id, sentence in map_doc_id_to_context[doc_id].items()]
        doc_context = "\n".join(doc_sentences)
        result[doc_id] = doc_context
    return result

