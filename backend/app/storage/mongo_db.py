from collections import defaultdict
from datetime import datetime
import pymongo
from pymongo.mongo_client import MongoClient
from app.config import MONGO_DB_KEY


class ChatDatabase:
    def __init__(self, uri):
        self.client = MongoClient(uri)
        self.db = self.client["chatHistory"]
        self.chat_collection = self.db["chat_messages"]

        # Create an index on the timestamp field
        self.chat_collection.create_index([("timestamp", pymongo.ASCENDING)])

    def add_message_to_db(self, message):
        try:
            self.chat_collection.insert_one(message)

        except Exception as e:
            print(e)

    def retrieve_chats_by_user(self, user_id):
        query = {"user_id": user_id}
        result = self.chat_collection.find(query).sort("timestamp", 1)

        chat_history = defaultdict(list)

        for message in result:
            conversation_id = message["conversation_id"]
            chat_history[conversation_id].append({
                "sender": message["sender"],
                "content": message["content"]
            })

        return chat_history


uri = f"mongodb+srv://TalyaFrancus:{MONGO_DB_KEY}@chathistory.e3406tw.mongodb.net/?retryWrites=true&w=majority"
print(uri)

chat_db = ChatDatabase(uri)

# Add a message to the database
message = {
    "user_id": "user123",
    "conversation_id": "first_chat",
    "sender": "user123",
    "content": "Hello, how are you?",
    "timestamp": datetime.utcnow()
}

chat_db.add_message_to_db(message)

user_id = "user123"
history = chat_db.retrieve_chats_by_user(user_id)
print(history)
