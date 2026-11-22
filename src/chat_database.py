
import sqlite3

def get_connection(DATABASE_PATH):
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database(DATABASE_PATH):
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = get_connection(DATABASE_PATH)

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL DEFAULT 'New Chat',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (conversation_id)
            REFERENCES conversations(id)
            ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS
        idx_messages_conversation_id
        ON messages(conversation_id);
    """)

    connection.commit()
    connection.close()


def create_conversation(title="New Chat"):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO conversations (title) VALUES (?)",
        (title,)
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id


def save_message(conversation_id, role, content):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
        """,
        (conversation_id, role, content)
    )

    connection.execute(
        """
        UPDATE conversations
        SET updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (conversation_id,)
    )

    connection.commit()
    connection.close()


def get_messages(conversation_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT role, content, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    )

    messages = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return messages


def get_conversations():
    connection = get_connection()

    cursor = connection.execute(
        """
        SELECT *
        FROM conversations
        ORDER BY updated_at DESC
        """
    )

    conversations = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return conversations
