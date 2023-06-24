import requests
from typing import List, Dict
from app.models.api_models import OpenAIResponse, Status
from app.models.query import Query


class OpenAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.openai.com/v1/chat/completions'

    def generate_answer(self, history: str, query: Query) -> OpenAIResponse:
        messages_to_deliver = history + "\n user: " + query.query_content
        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }
        data = {
            "model": "gpt-3.5-turbo",
            'messages':  [{'role': 'user', 'content': messages_to_deliver}],
            "temperature": 0.8,
        }

        response = requests.post(self.endpoint, headers=headers, json=data)
        response_data = response.json()

        if response.ok:
            answer = response_data['choices'][0]['message']['content']
            return OpenAIResponse(status=Status.Ok, content=answer)
        else:
            error_message = response_data['error']
            return OpenAIResponse(status=Status.Failed, content=error_message)
