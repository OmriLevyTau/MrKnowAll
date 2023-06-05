import requests

from app.models.api_models import OpenAIResponse, Status
from app.models.query import Query


class OpenAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.openai.com/v1/chat/completions'

    def generate_answer(self, query: Query) -> OpenAIResponse:
        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }
        data = {
            "model": "gpt-3.5-turbo",
            'messages': [{'role': 'user', 'content': query.query_content}],
            "temperature": 1,
        }

        response = requests.post(self.endpoint, headers=headers, json=data)
        response_data = response.json()

        if response.ok:
            answer = response_data['choices'][0]['message']['content']
            return OpenAIResponse(status=Status.Ok, content=answer)
        else:
            error_message = response_data['error']
            return OpenAIResponse(status=Status.Failed, content=error_message)
