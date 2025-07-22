import sqlite3
import os

# Set up a persistent folder for DB
DB_FOLDER = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, 'chat_history.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question TEXT NOT NULL,
            response TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def verify_user(username, password_hash):
    user = get_user_by_username(username)
    if user and user[2] == password_hash:
        return user
    return None

def save_chat(user_id, question, response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (user_id, question, response) VALUES (?, ?, ?)", (user_id, question, response))
    conn.commit()
    conn.close()

def get_all_chats(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "user_id": row[1], "question": row[2], "response": row[3]} for row in rows]

def update_chat(chat_id, question, response):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE chat SET question = ?, response = ? WHERE id = ?", (question, response, chat_id))
    conn.commit()
    conn.close()

def delete_chat(user_id, chat_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if chat_id == 0:
        # Delete all chats for the given user
        cursor.execute("DELETE FROM chat WHERE user_id = ?", (user_id,))
    else:
        # Delete a specific chat for the given user, ensuring it belongs to them
        cursor.execute("DELETE FROM chat WHERE id = ? AND user_id = ?", (chat_id, user_id))
    conn.commit()
    conn.close()
