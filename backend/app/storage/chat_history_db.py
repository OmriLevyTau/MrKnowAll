import sqlite3


class ChatHistoryManager:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id TEXT,
                            message TEXT,
                            message_type TEXT)''')
        self.conn.commit()

    def add_message(self, user_id, message, message_type):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO chats (user_id, message, message_type) VALUES (?, ?, ?)''',
                       (user_id, message, message_type))
        self.conn.commit()

    def get_user_messages_with_answers(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT message, message_type FROM chats WHERE user_id = ? ORDER BY id DESC LIMIT 30', (user_id,))
        rows = cursor.fetchall()
        messages_with_answers = []

        for message, message_type in rows:
            if message_type == 'User':
                messages_with_answers.append("user: " + message + ' ')
            elif message_type == 'AI':
                messages_with_answers.append("AI: " + message + ' ')
        return ''.join(reversed(messages_with_answers))

    def delete_chat_history(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM chats')
        self.conn.commit()


# Example usage of ChatHistoryManager
# Create an instance of ChatHistoryManager
chat_manager = ChatHistoryManager("chat_history.db")

# Create the chat history table if it doesn't exist
chat_manager.create_table()

# Add some example messages
chat_manager.add_message("user1", "Hello", "User")
chat_manager.add_message("user1", "Hi there! How can I assist you?", "AI")
chat_manager.add_message("user1", "I have a question.", "User")

# Retrieve and display the chat history with answers for a specific user
user_id = "user1"
messages_with_answers = chat_manager.get_user_messages_with_answers(user_id)

print(messages_with_answers)

chat_manager.delete_chat_history()

# Disconnect from the database
chat_manager.disconnect()
