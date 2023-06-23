import sqlite3
from typing import List


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
                            chat_id TEXT,
                            user_message TEXT,
                            chat_message TEXT)''')
        self.conn.commit()

    def add_message(self, user_id, chat_id, user_message, chat_message):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO chats (user_id, chat_id, user_message, chat_message) VALUES (?, ?, ?, ?)''',
                       (user_id, chat_id, user_message, chat_message))
        self.conn.commit()

    def get_user_messages_with_answers(self, user_id) -> str:
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT user_message, chat_message FROM chats WHERE user_id = ? ORDER BY id ASC LIMIT 6', (user_id,))
        rows = cursor.fetchall()
        history = ""
        number_of_qa = 0

        for user_message, chat_message in rows:
            combined_messages = "user-question:" + user_message + \
                "\n" + "AI-answer:" + chat_message + "\n \n "
            history = history + combined_messages
            number_of_qa = number_of_qa + 1

        return history, number_of_qa

    def delete_chat_history_by_user_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM chats WHERE user_id = ?', (user_id,))
        self.conn.commit()

    def delete_all_chat_history(self):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM chats')
        self.conn.commit()

    def delete_table(self):
        cursor = self.conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS chats")
        self.conn.commit()

    def print_DB(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM chats")
        print(cur.fetchall())
