import requests
from typing import List, Dict, Tuple
from app.models.api_models import OpenAIResponse, Status
from app.models.query import Query
from app.services.chat.chat_manager import ASSISTANT, USER

from app.param_tuning import OPEN_AI_TEMPERATURE

ROLE = "role"
CONTENT = "content"
class OpenAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.openai.com/v1/chat/completions'
        self.system ={ROLE: "system", CONTENT: "You are an AI assistant that provide informative answers that are "
                                               "directly related to the given text and context. Avoid answering "
                                               "questions about the model or any irrelevant topics. Stay focused on "
                                               "the provided information."}

    def generate_answer(self, history: List[Tuple[str, str]], query: Query) -> OpenAIResponse:
        '''
        history: [q1, a1, q2, a2]
        '''

        messages = []
        messages.append(self.system)
        history_messages = OpenAIAPI.compose_openai_history(history)
        messages += history_messages
        user_msg = {ROLE: USER, CONTENT: query.query_content}
        messages.append(user_msg)

        """
        role: system: ----
        role: user: q3
        rolse: assistnat: answer3
        ...
        rolse: user: 
        
        """

        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }
        data = {
            "model": "gpt-3.5-turbo",
            'messages':  messages,
            "temperature": OPEN_AI_TEMPERATURE,
        }

        response = requests.post(self.endpoint, headers=headers, json=data)
        response_data = response.json()

        if response.ok:
            answer = response_data['choices'][0]['message']['content']
            return OpenAIResponse(status=Status.Ok, content=answer)
        else:
            error_message = response_data['error']
            return OpenAIResponse(status=Status.Failed, content=error_message)


    @staticmethod
    def compose_openai_history(history: List[Tuple[str, str]]):
        '''
        Arguments:
            history: [("user", "question"), ("assistant", "answer"),..]
        '''
        result = []
        for i, tup in enumerate(history):
            if (tup[0] == USER):
                result.append({ROLE: USER, CONTENT: tup[1]})
            if (tup[0] == ASSISTANT):
                result.append({ROLE: ASSISTANT, CONTENT: tup[1]})
        return result
