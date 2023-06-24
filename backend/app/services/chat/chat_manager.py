from typing import Optional

from app.models.api_models import OpenAIResponse, Status, QueryResponse, QueryResponseType
from app.models.query import Query
from app.param_tuning import MAX_NUM_OF_CHARS_IN_QUERY, MAX_NUM_OF_CHARS_IN_QUESTION, MAX_NUM_OF_WORDS_IN_QUERY, \
    SCORE_THRESHOLD
from app.storage.chat_history_db import ChatHistoryManager

# create a connection to the local DB for saving the chat history
chat_history_manager = ChatHistoryManager("chat_history.db")

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


def get_history_for_chat(user_id: str, query: Query) -> str:
    '''
    Given a user_id and a Query, get the short-term history of the chat.
    That is the last messages of the user and the system, adhering to the
    length restriction.
    '''
    query_content = query.query_content
    query_content_len = len(query_content)
    returned_history = ""

    # get the last 6 questions and answers
    history_messages_combined, number_of_questions_and_answers = chat_history_manager.get_user_messages_with_answers(
        user_id=user_id)

    history_messages_list = history_messages_combined.split("user-question:")

    # if this is the first time there is no history
    if number_of_questions_and_answers < 1:
        return ""

    returned_history = history_messages_list[1]

    used_characters = 0 + len(returned_history)
    index = 2

    # in the loop we add history messages only if the entire message we send to openAI API is less then 4096 chars
    while (
            index < number_of_questions_and_answers and MAX_NUM_OF_CHARS_IN_QUERY - query_content_len - used_characters - len(
            history_messages_list[index]) >= 0):
        returned_history = returned_history + history_messages_list[index]
        used_characters = used_characters + len(history_messages_list[index])
        index = index + 1

    return returned_history



def return_query_response(query_content: str, response_type: str, e: Optional[Exception]) -> QueryResponse:

    if response_type == "TooLongQuery":
        without_API_communication_response = OpenAIResponse(
            status=Status.Ok,
            content='We apologize for the inconvenience, but to ensure a smoother experience, we kindly request that you limit your question to a maximum of 128 words and 512 characters. Please take a moment to edit your question accordingly. Your cooperation is greatly appreciated, and we thank you for your understanding!'
        )
        return QueryResponse(status=Status.Ok,
                             response_type=QueryResponseType.TooLongQuery,
                             query_content=query_content,
                             context='',
                             response=without_API_communication_response,
                             references=[])

    elif response_type == "NoMatchingVectors":
        without_API_communication_response = OpenAIResponse(
            status=Status.Ok, content='We are sorry, but it seems that there is no relevant sentences to your question in your files. You are more than welcome to ask a different question, or upload files which are relevant to your question')
        return QueryResponse(status=Status.Ok,
                             response_type=QueryResponseType.NoMatchingVectors,
                             query_content=query_content,
                             context='',
                             response=without_API_communication_response,
                             references=[])

    elif response_type == "Failed":
        return QueryResponse(status=Status.Failed,
                             response_type=QueryResponseType.Failed,
                             query_content=query_content,
                             context='',
                             response=OpenAIResponse(
                                 status=Status.Failed, content=str(e)
                             ),
                             references=[])
