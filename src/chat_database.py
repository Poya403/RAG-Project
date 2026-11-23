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

        CREATE TABLE IF NOT EXISTS message_sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER NOT NULL,
            content TEXT NOT NULL,

            FOREIGN KEY (message_id)
            REFERENCES messages(id)
            ON DELETE CASCADE
        );

        CREATE INDEX IF NOT EXISTS
        idx_messages_conversation_id
        ON messages(conversation_id);

        CREATE INDEX IF NOT EXISTS
        idx_message_sources_message_id
        ON message_sources(message_id);
    """)

    connection.commit()
    connection.close()

def create_conversation(DATABASE_PATH, title="گفتگو جدید"):
    connection = get_connection(DATABASE_PATH)

    cursor = connection.execute(
        "INSERT INTO conversations (title) VALUES (?)",
        (title,)
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id

def delete_conversation(DATABASE_PATH, conversation_id):
    connection = get_connection(DATABASE_PATH)

    cursor = connection.execute(
        """
        DELETE FROM conversations
        WHERE id = ?
        """, (conversation_id,)
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0

def rename_conversation(DATABASE_PATH, conversation_id, new_title):
    connection = get_connection(DATABASE_PATH)

    cursor = connection.execute(
        """
        UPDATE conversations
        SET title = ?
        WHERE id = ?
        """,
        (new_title, conversation_id)
    )

    connection.commit()
    connection.close()

    return cursor.rowcount > 0

def save_message(DATABASE_PATH, conversation_id, role, content, sources=None):
    connection = get_connection(DATABASE_PATH)

    cursor = connection.execute(
        """
        INSERT INTO messages (conversation_id, role, content)
        VALUES (?, ?, ?)
        """,
        (conversation_id, role, content)
    )

    message_id = cursor.lastrowid

    if sources:
        for source in sources:
            connection.execute(
                """
                INSERT INTO message_sources (message_id, content)
                VALUES (?, ?)
                """,
                (message_id, source)
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

    return message_id

def get_messages(DATABASE_PATH, conversation_id):
    connection = get_connection(DATABASE_PATH)

    cursor = connection.execute(
        """
        SELECT id, role, content, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    )

    messages = [dict(row) for row in cursor.fetchall()]

    for message in messages:
        cursor = connection.execute(
            """
            SELECT content
            FROM message_sources
            WHERE message_id = ?
            ORDER BY id ASC
            """,
            (message["id"],)
        )

        message["sources"] = [row["content"] for row in cursor.fetchall()]

    connection.close()
    return messages

def get_conversations(DATABASE_PATH):
    connection = get_connection(DATABASE_PATH)

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
