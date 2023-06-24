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
        '''
        returns [(q1, a1), (q2, a2)]
        '''
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT user_message, chat_message FROM chats WHERE user_id = ? ORDER BY id DESC LIMIT 6', (user_id,))
        rows = cursor.fetchall()
        return rows, len(rows)


    def delete_chat_history_by_user_id(self, user_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM chats WHERE user_id = ?', (user_id,))
            self.conn.commit()
        except Exception as error:
            raise Exception("Failed deleting chat history for user: " + user_id)

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
